import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import random
from flask_mail import Mail, Message
from sqlalchemy import func
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key_change_this_in_production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickdesk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/profile_pics')
app.config['ATTACHMENT_FOLDER'] = os.path.join(app.root_path, 'static/attachments')

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'shaikalthaf1768@gmail.com'
app.config['MAIL_PASSWORD'] = 'qtbh kzbd fpuy rcgi'

mail = Mail(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ATTACHMENT_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("You don't have permission to view this page.")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def agent_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ('admin', 'support_agent'):
            flash("You don't have permission to perform this action.")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    email_id = db.Column(db.String(120), unique=True, nullable=True)
    mobile_number = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    role = db.Column(db.String(20), default='end_user')
    profile_image = db.Column(db.String(255), default='default_profile.png')
    upgrade_request_pending = db.Column(db.Boolean, default=False)
    
    residential_address = db.Column(db.String(255), nullable=True)
    education_details = db.Column(db.Text, nullable=True)
    occupation_details = db.Column(db.String(100), nullable=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    tickets = db.relationship('Ticket', backref='author', lazy=True, foreign_keys='[Ticket.user_id]')
    assigned_tickets = db.relationship('Ticket', backref='assignee', lazy=True, foreign_keys='[Ticket.assigned_to_id]')
    comments = db.relationship('Comment', backref='commenter', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UpgradeRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='upgrade_requests', lazy=True)
    status = db.Column(db.String(20), default='pending')
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    tickets = db.relationship('Ticket', backref='category', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='open')
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    comments = db.relationship('Comment', backref='ticket', lazy=True, order_by='Comment.created_at')
    attachments = db.relationship('Attachment', backref='ticket', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('landing_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = request.form.get('name')
        mobile_number = request.form.get('mobile_number')
        email_id = request.form.get('email_id')
        gender = request.form.get('gender')
        profile_image = request.files.get('profile_image')
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
        if User.query.filter_by(email_id=email_id).first():
            flash('Email already registered.')
            return redirect(url_for('register'))
        if session.get('email_verified') != email_id:
            flash('Please verify your email address with OTP before registering.')
            return redirect(url_for('register'))
        image_filename = 'default_profile.png'
        if profile_image and profile_image.filename != '':
            filename = secure_filename(profile_image.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_image.save(file_path)
            image_filename = filename
        new_user = User(
            username=username,
            name=name,
            email_id=email_id,
            mobile_number=mobile_number,
            gender=gender,
            profile_image=image_filename
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session.pop('email_verified', None)
        session.pop('otp_data', None)
        flash('Registration successful. You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/send-otp', methods=['POST'])
def send_otp():
    email = request.form.get('email')
    if User.query.filter_by(email_id=email).first():
        return jsonify({'status': 'error', 'message': 'Email is already registered.'})
    otp = str(random.randint(100000, 999999))
    session['otp_data'] = {'email': email, 'otp': otp}
    print(f"\n--- DEBUG: OTP for {email} is: {otp} ---\n")
    return jsonify({'status': 'success', 'message': 'OTP sent (printed to console).'})

@app.route('/verify-otp-ajax', methods=['POST'])
def verify_otp_ajax():
    email = request.form.get('email')
    user_otp = request.form.get('otp')
    otp_data = session.get('otp_data')
    print(f"\n--- DEBUG VERIFY OTP ---")
    print(f"Session OTP Data: {otp_data}")
    print(f"User entered OTP: {user_otp}")
    print(f"-------------------------\n")
    if not otp_data or otp_data.get('email') != email or otp_data.get('otp') != user_otp:
        return jsonify({'status': 'error', 'message': 'Invalid OTP.'})
    session['email_verified'] = email
    return jsonify({'status': 'success', 'message': 'OTP verified successfully.'})

@app.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    categories = Category.query.all()

    if current_user.role == 'admin':
        tickets = Ticket.query.all()
        users = User.query.all()
        pending_requests = UpgradeRequest.query.filter_by(status='pending').all()
        
        category_ticket_counts = db.session.query(Category.name, func.count(Ticket.id)).join(Ticket).group_by(Category.name).all()
        status_ticket_counts = db.session.query(Ticket.status, func.count(Ticket.id)).group_by(Ticket.status).all()
        
        category_labels = [c[0] for c in category_ticket_counts]
        category_data = [c[1] for c in category_ticket_counts]
        
        status_labels = [s[0].title() for s in status_ticket_counts]
        status_data = [s[1] for s in status_ticket_counts]

        return render_template('admin_dashboard.html', 
                               tickets=tickets, 
                               users=users, 
                               pending_requests=pending_requests,
                               category_labels=category_labels,
                               category_data=category_data,
                               status_labels=status_labels,
                               status_data=status_data)
    elif current_user.role == 'support_agent':
        query = Ticket.query
        
        # Filtering logic for agents
        status = request.args.get('status')
        if status:
            query = query.filter(Ticket.status == status)

        search_query = request.args.get('search')
        if search_query:
            query = query.filter(
                (Ticket.subject.ilike(f'%{search_query}%')) |
                (Ticket.description.ilike(f'%{search_query}%'))
            )
            
        # Separate queries for assigned and unassigned tickets
        assigned_tickets_count = query.filter(Ticket.assigned_to_id == current_user.id).count()
        unassigned_tickets_count = query.filter(Ticket.assigned_to_id.is_(None)).count()
        
        # Main query for the table, showing all tickets for agents
        all_tickets = query.order_by(Ticket.created_at.desc()).all()
        
        # Get data for the status chart
        status_ticket_counts = db.session.query(Ticket.status, func.count(Ticket.id)).group_by(Ticket.status).all()
        status_labels = [s[0].title() for s in status_ticket_counts]
        status_data = [s[1] for s in status_ticket_counts]

        return render_template('agent_dashboard.html', 
                               all_tickets=all_tickets, 
                               assigned_tickets_count=assigned_tickets_count,
                               unassigned_tickets_count=unassigned_tickets_count,
                               status_labels=status_labels,
                               status_data=status_data,
                               search_query=search_query,
                               status=status)
    else:
        query = Ticket.query.filter_by(user_id=current_user.id)
        show_open = request.args.get('show_open', 'off') == 'on'
        category_id = request.args.get('category')
        status = request.args.get('status')
        search_query = request.args.get('search')
        sort_by = request.args.get('sort_by')
        if show_open:
            query = query.filter(Ticket.status == 'open')
        if category_id:
            query = query.filter(Ticket.category_id == category_id)
        if status:
            query = query.filter(Ticket.status == status)
        if search_query:
            query = query.filter(
                (Ticket.subject.ilike(f'%{search_query}%')) |
                (Ticket.description.ilike(f'%{search_query}%'))
            )
        if sort_by == 'most_comments':
            query = query.join(Comment).group_by(Ticket.id).order_by(func.count(Comment.id).desc())
        elif sort_by == 'most_votes':
            query = query.order_by(Ticket.upvotes.desc())
        else:
            query = query.order_by(Ticket.created_at.desc())
        tickets = query.paginate(page=page, per_page=per_page, error_out=False)
        notifications = session.get('notifications', [])
        return render_template(
            'user_dashboard.html', 
            tickets=tickets, 
            categories=categories,
            search_query=search_query,
            show_open=show_open,
            category_id=category_id,
            status=status,
            sort_by=sort_by
        )

@app.route('/ask_question', methods=['GET', 'POST'])
@login_required
def ask_question():
    categories = Category.query.all()
    if request.method == 'POST':
        subject = request.form.get('subject')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        new_ticket = Ticket(subject=subject, description=description, user_id=current_user.id, category_id=category_id)
        db.session.add(new_ticket)
        db.session.commit()
        
        files = request.files.getlist('attachment[]')
        for file in files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['ATTACHMENT_FOLDER'], filename)
                file.save(file_path)
                
                new_attachment = Attachment(filename=filename, ticket_id=new_ticket.id)
                db.session.add(new_attachment)
        db.session.commit()

        flash('Your ticket has been submitted!')
        return redirect(url_for('dashboard'))
    return render_template('ask_question.html', categories=categories)

@app.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_details(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    notifications = session.get('notifications', [])
    session['notifications'] = [n for n in notifications if n['ticket_id'] != ticket_id]
    if current_user.role not in ('admin', 'support_agent') and ticket.user_id != current_user.id:
        flash("You do not have permission to view this ticket.")
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        if 'comment_content' in request.form:
            comment_content = request.form.get('comment_content')
            if comment_content:
                new_comment = Comment(content=comment_content, user_id=current_user.id, ticket_id=ticket.id)
                db.session.add(new_comment)
                db.session.commit()
                flash("Comment added successfully.")
                if current_user.role in ('admin', 'support_agent') and ticket.user_id != current_user.id:
                    notifications = session.get('notifications', [])
                    notifications.append({
                        'ticket_id': ticket.id,
                        'message': f'A support agent has replied to your ticket "{ticket.subject}".'
                    })
                    session['notifications'] = notifications
        elif 'new_status' in request.form and current_user.role in ('admin', 'support_agent'):
            new_status = request.form.get('new_status')
            ticket.status = new_status
            db.session.commit()
            flash(f"Ticket status updated to '{new_status.title()}'.")
        elif 'assign_to_me' in request.form and current_user.role in ('admin', 'support_agent'):
            ticket.assigned_to_id = current_user.id
            db.session.commit()
            flash(f"Ticket assigned to you.")
        return redirect(url_for('ticket_details', ticket_id=ticket.id))
    return render_template('ticket_details.html', ticket=ticket)

@app.route('/ticket/<int:ticket_id>/vote/<action>')
@login_required
def vote_ticket(ticket_id, action):
    ticket = Ticket.query.get_or_404(ticket_id)
    if action == 'upvote':
        ticket.upvotes += 1
    elif action == 'downvote':
        ticket.downvotes += 1
    db.session.commit()
    flash(f"Your vote has been recorded.")
    return redirect(url_for('dashboard'))

@app.route('/admin/categories', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_categories():
    if request.method == 'POST':
        category_name = request.form.get('name')
        if category_name:
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added successfully!')
        else:
            flash('Category name cannot be empty.')
        return redirect(url_for('manage_categories'))
    categories = Category.query.all()
    return render_template('category_management.html', categories=categories)

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_role = request.form.get('new_role')
        user = User.query.get(user_id)
        if user:
            user.role = new_role
            db.session.commit()
            flash(f"Role for user '{user.username}' updated to '{new_role}'.")
        else:
            flash("User not found.")
        return redirect(url_for('manage_users'))
    users = User.query.all()
    return render_template('user_management.html', users=users)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    current_user.name = request.form.get('name')
    current_user.mobile_number = request.form.get('mobile_number')
    current_user.gender = request.form.get('gender')
    current_user.residential_address = request.form.get('residential_address')
    current_user.education_details = request.form.get('education_details')
    current_user.occupation_details = request.form.get('occupation_details')
    db.session.commit()
    flash('Profile updated successfully!')
    return redirect(url_for('profile'))

@app.route('/profile/request_upgrade', methods=['POST'])
@login_required
def request_upgrade():
    if current_user.role == 'end_user' and not current_user.upgrade_request_pending:
        new_request = UpgradeRequest(user_id=current_user.id)
        current_user.upgrade_request_pending = True
        db.session.add(new_request)
        db.session.commit()
        flash("Your upgrade request has been sent to the admin.")
    else:
        flash("You cannot request an upgrade at this time.")
    return redirect(url_for('profile'))

@app.route('/admin/manage_requests/<int:request_id>/<action>', methods=['POST'])
@login_required
@admin_required
def manage_requests(request_id, action):
    upgrade_request = UpgradeRequest.query.get_or_404(request_id)
    user = User.query.get(upgrade_request.user_id)
    
    if action == 'accept':
        user.role = 'support_agent'
        upgrade_request.status = 'accepted'
        user.upgrade_request_pending = False
        flash(f"Upgrade request for {user.username} accepted. Role changed to support agent.")
    elif action == 'reject':
        upgrade_request.status = 'rejected'
        user.upgrade_request_pending = False
        flash(f"Upgrade request for {user.username} rejected.")
    
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('notifications', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

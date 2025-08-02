from app import app, db, User, Category
from werkzeug.security import generate_password_hash

with app.app_context():
    # Check if admin user exists, create if not
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin = User(username='admin', role='admin')
        admin.set_password('adminpassword')
        db.session.add(admin)
        print("Admin user created with username 'admin' and password 'adminpassword'")
    else:
        print("Admin user already exists.")

    # Check if categories exist, create if not
    if not Category.query.first():
        categories = ['Technical Support', 'Billing', 'General Inquiry']
        for name in categories:
            new_category = Category(name=name)
            db.session.add(new_category)
        print(f"Default categories created: {categories}")
    else:
        print("Categories already exist.")

    db.session.commit()
    print("Database seeding complete.")
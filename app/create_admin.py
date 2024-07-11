# create_admin.py
from app import create_app, db, bcrypt
from data_models import Staff

app = create_app()

with app.app_context():
    db.create_all()
    admin_password = 'admin_password'
    hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
    
    admin_user = Staff(
        s_name='admin',
        s_email='admin@example.com',
        s_password=hashed_password,
        is_admin=True,
        is_approved=True,
        s_role='admin',
        s_contact='9878787889'
    )
    db.session.add(admin_user)
    db.session.commit()

print("Admin user created successfully")
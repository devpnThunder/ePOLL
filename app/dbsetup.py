from .extensions import db
from models import Role, generate_password_hash, User
from datetime import datetime

#=================================================================#
# Create all Database Tables
#=================================================================#
# Create all database tables
def setup_database(app):
    """
    Set up the database and create initial roles.
    """
    with app.app_context():
        db.create_all()    
        # Check if roles and users already exist
        if not Role.query.first():
            # Initialize roles
            super = Role(name='Super', created_at=datetime.now(), updated_at=datetime.now())
            db.session.add(super)
            db.session.commit()

            user = User(firstname="Super", lastname="Admin", email='superadmin@mail.com', password=generate_password_hash('SuperAdmin@123.?'), 
                        date_registered=datetime.now(), updated_at=datetime.now(), roles=[super])
            db.session.add(user)
            db.session.commit()

            print('Database initialized!')
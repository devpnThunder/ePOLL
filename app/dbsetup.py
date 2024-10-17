from app.extensions import db
from app.models import Permission, Role, generate_password_hash, UserStatus, User
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
            # Create Permissions
            create_permission = Permission(name='Create')
            read_permission = Permission(name='Read')
            update_permission = Permission(name='Update')
            delete_permission = Permission(name='Delete')

            db.session.add_all([create_permission, read_permission, update_permission, delete_permission])
            db.session.commit()
            print("Permissions created successfully!")

            # Initialize roles and assigns 'Super' role with all permissions
            super_role = Role(name='Super', description='Super admin role', permissions=([delete_permission, update_permission, read_permission, create_permission]))
            # super_role.permissions.extend([create_permission, read_permission, update_permission, delete_permission])
            db.session.add(super_role)
            db.session.commit()

            # Create default user and assign super role
            user = User(email='superadmin@mail.com', password=generate_password_hash('SuperAdmin@123.?'), 
                        status=UserStatus.ACTIVE, created_at=datetime.now(), roles=[super_role])
            db.session.add(user)
            db.session.commit()

            print('Database initialized with default permissions, role and user!')
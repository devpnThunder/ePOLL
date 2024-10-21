from app.extensions import db
from app.models import Permission, Role, RolePermission, generate_password_hash, UserStatus, User, UserRole, County, Constituency
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
            create_permission = Permission(name="Create")
            read_permission = Permission(name="Read")
            update_permission = Permission(name="Update")
            delete_permission = Permission(name="Delete")
            vote_permission = Permission(name="Vote")

            db.session.add_all([create_permission, read_permission, update_permission, delete_permission, vote_permission])
            db.session.commit()
            print("Permissions created successfully!")

            # Create Roles
            super_role = Role(name="Super", description="Super admin role")
            super_role.permissions.extend([create_permission, read_permission, update_permission, delete_permission])
            voter_role = Role(name="Voter", description="Voter role")
            # voter_role.permissions.extend([voter_role])
            db.session.add_all([super_role, voter_role])
            db.session.commit()
            print("Super role created and permissions assigned successfully!")

            # Assign Voter Role Permission
            voter_role_permission = RolePermission(role_id=voter_role.id, permission_id=vote_permission.id)

            db.session.add(voter_role_permission)
            db.session.commit()
            print("Role permissions assigned successfully!")

            # Create default user and assign super role
            super_user = User(email="superadmin@mail.com", status=UserStatus.ACTIVE, created_at=datetime.now())
            super_user.set_password("SuperMan@123.?")
            db.session.add(super_user)
            db.session.commit()
            print("Super user created successfully!")

            # Assign the User to Super Role
            user_role = UserRole(user_id=super_user.id, role_id=super_role.id)
            db.session.add(user_role)
            db.session.commit()
            print("Super user assigned super role successfully!")

            # Load Counties to the database
            county1 = County(code=1, name="Mombasa", created_at=datetime.now()) 
            county2 = County(code=2, name="Kwale", created_at=datetime.now())
            county3 = County(code=3, name="Kilifi", created_at=datetime.now())
            county4 = County(code=4, name="Tana River", created_at=datetime.now())
            county5 = County(code=5, name="Lamu", created_at=datetime.now())
            county6 = County(code=6, name="Taita Taveta", created_at=datetime.now())
            county7 = County(code=7, name="Garissa", created_at=datetime.now())
            county8 = County(code=8, name="Wajir", created_at=datetime.now())
            county9 = County(code=9, name="Mandera", created_at=datetime.now())
            county10 = County(code=10, name="Marsabit", created_at=datetime.now())
            county11 = County(code=11, name="Isiolo", created_at=datetime.now()) 
            county12 = County(code=12, name="Meru", created_at=datetime.now())
            county13 = County(code=13, name="Tharaka Nithi", created_at=datetime.now())
            county14 = County(code=14, name="Embu", created_at=datetime.now())
            county15 = County(code=15, name="Kitui", created_at=datetime.now())
            county16 = County(code=16, name="Machakos", created_at=datetime.now())
            county17 = County(code=17, name="Makueni", created_at=datetime.now())
            county18 = County(code=18, name="Nyandarua", created_at=datetime.now())
            county19 = County(code=19, name="Nyeri", created_at=datetime.now())
            county20 = County(code=20, name="Kirinyaga", created_at=datetime.now())
            county21 = County(code=21, name="Murang'a", created_at=datetime.now()) 
            county22 = County(code=22, name="Kiambu", created_at=datetime.now())
            county23 = County(code=23, name="Turkana", created_at=datetime.now())
            county24 = County(code=24, name="West Pokot", created_at=datetime.now())
            county25 = County(code=25, name="Samburu", created_at=datetime.now())
            county26 = County(code=26, name="Trans Nzoia", created_at=datetime.now())
            county27 = County(code=27, name="Uasin Gishu", created_at=datetime.now())
            county28 = County(code=28, name="Elgeyo Marakwet", created_at=datetime.now())
            county29 = County(code=29, name="Nandi", created_at=datetime.now())
            county30 = County(code=30, name="Baringo", created_at=datetime.now())
            county31 = County(code=31, name="Laikipia", created_at=datetime.now()) 
            county32 = County(code=32, name="Nakuru", created_at=datetime.now())
            county33 = County(code=33, name="Narok", created_at=datetime.now())
            county34 = County(code=34, name="Kajiado", created_at=datetime.now())
            county35 = County(code=35, name="Kericho", created_at=datetime.now())
            county36 = County(code=36, name="Bomet", created_at=datetime.now())
            county37 = County(code=37, name="Kakamega", created_at=datetime.now())
            county38 = County(code=38, name="Vihiga", created_at=datetime.now())
            county39 = County(code=39, name="Bungoma", created_at=datetime.now())
            county40 = County(code=40, name="Busia", created_at=datetime.now())
            county41 = County(code=41, name="Siaya", created_at=datetime.now()) 
            county42 = County(code=42, name="Kisumu", created_at=datetime.now())
            county43 = County(code=43, name="Homa Bay", created_at=datetime.now())
            county44 = County(code=44, name="Migori", created_at=datetime.now())
            county45 = County(code=45, name="Kisii", created_at=datetime.now())
            county46 = County(code=46, name="Nyamira", created_at=datetime.now())
            county47 = County(code=47, name="Nairobi", created_at=datetime.now())

            db.session.add_all([county1, county2, county3, county4, county5, county6, county7, county8, county9, county10,
                                county11, county12, county13, county14, county15, county16, county17, county18, county19, county20,
                                county21, county22, county23, county24, county25, county26, county27, county28, county29, county30,
                                county31, county32, county33, county34, county35, county36, county37, county38, county39, county40,
                                county41, county42, county43, county44, county45, county46, county47])
            db.session.commit()
            print("Counties added successfully!")

            # Create Constituencies
            nrb1 = Constituency(county_id=county47.id, name="Westlands", created_at=datetime.now())
            nrb2 = Constituency(county_id=county47.id, name="Dagoretti North", created_at=datetime.now())
            nrb3 = Constituency(county_id=county47.id, name="Dagoretti South", created_at=datetime.now())
            nrb4 = Constituency(county_id=county47.id, name="Lang'ata", created_at=datetime.now())
            nrb5 = Constituency(county_id=county47.id, name="Kibra", created_at=datetime.now())
            nrb6 = Constituency(county_id=county47.id, name="Roysambu", created_at=datetime.now())
            nrb7 = Constituency(county_id=county47.id, name="Kasarani", created_at=datetime.now())
            nrb8 = Constituency(county_id=county47.id, name="Ruaraka", created_at=datetime.now())
            nrb9 = Constituency(county_id=county47.id, name="Embakasi South", created_at=datetime.now())
            nrb10 = Constituency(county_id=county47.id, name="Embakasi North", created_at=datetime.now())
            nrb11 = Constituency(county_id=county47.id, name="Embakasi Central", created_at=datetime.now())
            nrb12 = Constituency(county_id=county47.id, name="Embakasi East", created_at=datetime.now())
            nrb13 = Constituency(county_id=county47.id, name="Embakasi West", created_at=datetime.now())
            nrb14 = Constituency(county_id=county47.id, name="Makadara", created_at=datetime.now())
            nrb15 = Constituency(county_id=county47.id, name="Kamukunji", created_at=datetime.now())
            nrb16 = Constituency(county_id=county47.id, name="Starehe", created_at=datetime.now())
            nrb17 = Constituency(county_id=county47.id, name="Mathare", created_at=datetime.now())

            db.session.add_all([nrb1, nrb2, nrb3, nrb4, nrb5, nrb6, nrb7, nrb8, nrb9, nrb10,
                                nrb11, nrb12, nrb13, nrb14, nrb15, nrb16, nrb17])
            db.session.commit()
            print("Costituencies added successfully!")

            print('Database initialized successfully!')
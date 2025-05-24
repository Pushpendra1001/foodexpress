from run import app, db
from models import User, Category, MenuItem
from werkzeug.security import generate_password_hash
import os

def create_default_images():
    """Create default images folder and add placeholder images if they don't exist"""
    img_dir = os.path.join(app.static_folder, 'img', 'menu')
    os.makedirs(img_dir, exist_ok=True)
    
    
    default_img = os.path.join(app.static_folder, 'img', 'default-food.jpg')
    if not os.path.exists(default_img):
        
        try:
            import shutil
            source = os.path.join(app.static_folder, 'img', 'logo.png')
            if os.path.exists(source):
                shutil.copy(source, default_img)
            print(f"Default image created at {default_img}")
        except Exception as e:
            print(f"Could not create default image: {e}")
    
    
    food_images = ['burger.jpg', 'pizza.jpg', 'fries.jpg', 'cola.jpg', 'cake.jpg']
    
    
    for img in food_images:
        img_path = os.path.join(img_dir, img)
        if not os.path.exists(img_path):
            try:
                
                shutil.copy(default_img, img_path)
                print(f"Created placeholder for {img}")
            except Exception as e:
                print(f"Could not create {img}: {e}")

def init_db():
    with app.app_context():
        print("Creating default images...")
        create_default_images()
        
        print("Creating database tables...")
        
        db.create_all()
        print("Tables created successfully!")
        
        
        print("Adding categories...")
        if Category.query.count() == 0:
            categories = [
                Category(name='Main Dishes'),
                Category(name='Sides'),
                Category(name='Beverages'),
                Category(name='Desserts')
            ]
            db.session.add_all(categories)
            db.session.commit()
            print("Categories added successfully!")
        else:
            print("Categories already exist, skipping")
        
        
        print("Adding menu items...")
        if MenuItem.query.count() == 0:
            menu_items = [
                MenuItem(
                    name='Classic Burger',
                    description='Juicy beef patty with fresh vegetables',
                    price=9.99,
                    image_url='burger.jpg',
                    category_id=1,
                    available=True
                ),
                MenuItem(
                    name='Pizza',
                    description='Fresh pizza with tomatoes and cheese',
                    price=12.99,
                    image_url='pizza.jpg',
                    category_id=1,
                    available=True
                ),
                MenuItem(
                    name='French Fries',
                    description='Crispy golden fries with seasoning',
                    price=3.99,
                    image_url='fries.jpg',
                    category_id=2,
                    available=True
                ),
                MenuItem(
                    name='Cola',
                    description='Refreshing cola drink',
                    price=1.99,
                    image_url='cola.jpg',
                    category_id=3,
                    available=True
                ),
                MenuItem(
                    name='Chocolate Cake',
                    description='Decadent chocolate cake with frosting',
                    price=5.99,
                    image_url='cake.jpg',
                    category_id=4,
                    available=True
                )
            ]
            db.session.add_all(menu_items)
            db.session.commit()
            print("Menu items added successfully!")
        else:
            print("Menu items already exist, skipping")
        
        
        print("Setting up admin user...")
        admin = User.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@gmail.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True,
                address='123 Admin St',
                contact='1234567890'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists!")
        
        print("Database initialization completed successfully!")

if __name__ == '__main__':
    init_db()
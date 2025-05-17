from run import db
from models import User, Cuisine, Restaurant, MenuItem


admin = User(name='Admin', email='admin@example.com', is_admin=True)
admin.set_password('admin123')
db.session.add(admin)


cuisines = ['Italian', 'Indian', 'Chinese', 'Mexican']
for cuisine_name in cuisines:
    cuisine = Cuisine(name=cuisine_name)
    db.session.add(cuisine)

db.session.commit()


restaurant = Restaurant(
    name='Sample Restaurant',
    description='A great place to eat',
    rating=4.5,
    delivery_fee=5.00,
    image_url='https://via.placeholder.com/300',
    cuisine_id=1
)
db.session.add(restaurant)
db.session.commit()


items = [
    {
        'name': 'Pizza Margherita',
        'description': 'Classic Italian pizza',
        'price': 12.99,
        'image_url': 'https://via.placeholder.com/300',
        'restaurant_id': 1
    },
    {
        'name': 'Pasta Carbonara',
        'description': 'Creamy pasta dish',
        'price': 14.99,
        'image_url': 'https://via.placeholder.com/300',
        'restaurant_id': 1
    }
]

for item_data in items:
    item = MenuItem(**item_data)
    db.session.add(item)

db.session.commit()
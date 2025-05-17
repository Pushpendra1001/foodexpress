from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import login_required, current_user, login_user, logout_user  # Add logout_user here
from flask_wtf.csrf import generate_csrf, CSRFProtect  # Add CSRFProtect import
from run import app, db
from models import User, MenuItem, Order, Category, CartItem, OrderItem
from forms import LoginForm, RegistrationForm, CheckoutForm
from functools import wraps
import os
from werkzeug.utils import secure_filename
from datetime import datetime

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Admin decorator function
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need to be an administrator to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def utility_processor():
    def get_categories():
        return Category.query.all()
    return dict(categories=get_categories())

# Landing Page
@app.route('/')
def index():
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('q', '')
    
    items_query = MenuItem.query
    
    if category_id:
        items_query = items_query.filter_by(category_id=category_id)
    if search_query:
        items_query = items_query.filter(MenuItem.name.ilike(f'%{search_query}%'))
    
    items = items_query.all()
    categories = Category.query.all()
    return render_template('index.html', items=items, categories=categories)

# Item Details Page
@app.route('/item/<int:id>')
def item_details(id):
    item = MenuItem.query.get_or_404(id)
    related_items = MenuItem.query.filter(
        MenuItem.category_id == item.category_id,
        MenuItem.id != item.id
    ).limit(4).all()
    
    can_add_to_cart = current_user.is_authenticated
    
    if not can_add_to_cart:
        flash('Please login to add items to your cart', 'info')
    
    # Use generate_csrf() directly instead of csrf.generate_csrf()
    return render_template('product_details.html', 
                         item=item, 
                         related_items=related_items,
                         can_add_to_cart=can_add_to_cart)

# Cart Routes
@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(item.menu_item.price * item.quantity for item in cart_items)
    delivery_fee = 5.00
    total = subtotal + delivery_fee
    return render_template('cart.html', 
                         cart_items=cart_items,
                         subtotal=subtotal,
                         delivery_fee=delivery_fee,
                         total=total)

@app.route('/cart/add/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    item = MenuItem.query.get_or_404(item_id)
    quantity = int(request.form.get('quantity', 1))
    
    cart_item = CartItem.query.filter_by(user_id=current_user.id, menu_item_id=item_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, menu_item_id=item_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Item added to cart', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    try:
        cart_item = CartItem.query.filter_by(user_id=current_user.id, id=item_id).first_or_404()
        action = request.form.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                db.session.delete(cart_item)
        
        db.session.commit()
        return redirect(url_for('cart'))
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating cart: {str(e)}")
        flash('An error occurred while updating your cart.', 'danger')
        return redirect(url_for('cart'))

@app.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/empty', methods=['POST'])
@login_required
def empty_cart():
    try:
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('Cart emptied successfully!', 'success')
        return redirect(url_for('cart'))
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error emptying cart: {str(e)}")
        flash('An error occurred while emptying your cart.', 'danger')
        return redirect(url_for('cart'))

# Checkout
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart'))

    subtotal = sum(item.menu_item.price * item.quantity for item in cart_items)
    form = CheckoutForm()

    if form.validate_on_submit():
        try:
            # Calculate delivery fee based on option
            delivery_fee = {
                'express': 5.00,
                'standard': 2.99,
                'pickup': 0.00
            }.get(form.delivery_option.data, 2.99)

            total = subtotal + delivery_fee

            # Create new order
            order = Order(
                user_id=current_user.id,
                delivery_option=form.delivery_option.data,
                delivery_address=form.address.data,
                contact=form.contact.data,
                total=total,
                status='pending'
            )
            db.session.add(order)
            db.session.flush()
            
            # Create order items
            for cart_item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=cart_item.menu_item_id,
                    quantity=cart_item.quantity,
                    price=cart_item.menu_item.price
                )
                db.session.add(order_item)

            # Clear cart
            CartItem.query.filter_by(user_id=current_user.id).delete()
            
            db.session.commit()
            flash('Order placed successfully!', 'success')
            return redirect(url_for('order_confirmation', order_id=order.id))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Checkout error: {str(e)}')
            flash(f'An error occurred while processing your order: {str(e)}', 'danger')

    # Calculate initial delivery fee for GET request
    delivery_fee = 2.99  # Default delivery fee
    total = subtotal + delivery_fee

    return render_template('checkout.html', 
                         form=form,
                         cart_items=cart_items,
                         subtotal=subtotal,
                         delivery_fee=delivery_fee,
                         total=total)

# Authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)  # Updated path

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            address=form.address.data,
            contact=form.contact.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)  # Updated path

@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Admin Routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    items = MenuItem.query.all()
    categories = Category.query.all()
    orders = Order.query.all()
    users = User.query.all()
    
    return render_template('admin/dashboard.html', 
                         items=items, 
                         categories=categories, 
                         orders=orders,
                         users=users)

# Update order status route
@app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status')
    if status in ['pending', 'processing', 'completed', 'cancelled']:
        order.status = status
        db.session.commit()
        flash(f'Order #{order.id} status updated to {status}.', 'success')
    return redirect(url_for('admin_dashboard'))

# Update item availability
@app.route('/admin/items/<int:item_id>/availability', methods=['POST'])
@login_required
@admin_required
def update_item_availability(item_id):
    item = MenuItem.query.get_or_404(item_id)
    data = request.get_json()
    if 'available' in data:
        item.available = data['available']
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

# Delete item route
@app.route('/admin/items/<int:item_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

# Delete category route
@app.route('/admin/categories/<int:category_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    # Check if category has menu items
    if category.menu_items:
        # Option: Delete all menu items in this category
        for item in category.menu_items:
            db.session.delete(item)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/add-item', methods=['POST'])
@login_required
@admin_required
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        price = float(request.form.get('price'))
        category_id = int(request.form.get('category_id'))
        available = 'available' in request.form
        
        # Handle image upload
        image = request.files.get('image')
        image_url = 'default-food.jpg'  # Default image
        
        if image and image.filename:
            # Generate a secure filename with timestamp
            filename = secure_filename(image.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            image_url = f"{timestamp}-{filename}"
            
            # Save the image
            img_path = os.path.join(app.static_folder, 'img', 'menu', image_url)
            image.save(img_path)
        
        # Create new menu item
        item = MenuItem(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            image_url=image_url,
            available=available
        )
        
        db.session.add(item)
        db.session.commit()
        
        flash('Menu item added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit-item', methods=['POST'])
@login_required
@admin_required
def edit_item():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        item = MenuItem.query.get_or_404(item_id)
        
        # Update item details
        item.name = request.form.get('name')
        item.description = request.form.get('description', '')
        item.price = float(request.form.get('price'))
        item.category_id = int(request.form.get('category_id'))
        item.available = 'available' in request.form
        
        # Handle image upload
        image = request.files.get('image')
        if image and image.filename:
            # Generate a secure filename with timestamp
            filename = secure_filename(image.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            image_url = f"{timestamp}-{filename}"
            
            # Save the image
            img_path = os.path.join(app.static_folder, 'img', 'menu', image_url)
            image.save(img_path)
            
            # Update image URL
            item.image_url = image_url
        
        db.session.commit()
        
        flash('Menu item updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/add-category', methods=['POST'])
@login_required
@admin_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        
        # Create new category
        category = Category(name=name)
        
        db.session.add(category)
        db.session.commit()
        
        flash('Category added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit-category', methods=['POST'])
@login_required
@admin_required
def edit_category():
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        category = Category.query.get_or_404(category_id)
        
        # Update category name
        category.name = request.form.get('name')
        
        db.session.commit()
        
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

# Profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# Category Items
@app.route('/category/<int:category_id>')
def category_items(category_id):
    category = Category.query.get_or_404(category_id)
    items = MenuItem.query.filter_by(category_id=category_id).all()
    return render_template('category_items.html', category=category, items=items)

@app.route('/menu')
def menu():
    categories = Category.query.all()
    return render_template('menu.html', categories=categories)

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    # Special handling for missing images
    path = request.path
    if path.startswith('/static/img/'):
        # Return a default image instead
        return redirect(url_for('static', filename='img/default-food.jpg'))
    return render_template('error.html', error=404), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error=500), 500

@app.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Security check - only allow users to see their own orders (or admin)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    # Calculate delivery fee based on option
    delivery_fee = {
        'express': 5.00,
        'standard': 2.99,
        'pickup': 0.00
    }.get(order.delivery_option, 2.99)
    
    return render_template('order_confirmation.html', 
                         order=order,
                         delivery_fee=delivery_fee)

@app.teardown_appcontext
def cleanup(resp_or_exc):
    db.session.remove()

# Add this function to properly close sessions
@app.teardown_request
def session_cleanup(exception=None):
    db.session.close()
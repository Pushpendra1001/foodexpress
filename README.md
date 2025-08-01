```markdown
# 🍔 Food Express

**Food Express** is a web-based food ordering system that allows users to browse menu items,
 add them to a cart, and place orders with various delivery options. The application supports user
 authentication, an admin panel for menu management, and real-time order tracking.

---

## 🚀 Features

### 👨‍🍳 Customer Features
- Browse menu items by category
- Add items to cart 🛒
- Adjust item quantities in cart
- Place orders with delivery options 🚚
- View order history and order status 📦

### 🛠️ Admin Features
- Add, edit, or remove menu items
- Manage food categories 🍽️
- View and update order statuses

---

## 🧰 Project Structure

```bash
📁 FoodExpress/
│
├── run.py             # Application entry point
├── models.py          # Database models
├── views.py           # Route handlers
├── auth.py            # Authentication functions
├── forms.py           # Form definitions
├── database.sql       # Database schema and sample data
├── init_db.py         # Database initialization script for add admin account
├── templates/         # HTML templates
└── static/            # CSS, JavaScript, and images
```

---

## 🛠️ Setup Instructions

### 1. 🧪 Create a Virtual Environment (Optional but Recommended)

Before installing dependencies, it's recommended to create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

- On Windows:
  ```bash
  venv\Scripts\activate
  ```


### 2. 📦 Database Setup

You have to set up the database First:

#### Part 1: Using the SQL script
1. Create a MySQL database named `foodexpress`.
2. Run the `database.sql` script to set up all tables and insert sample data:
   in mysql workbench excute every Query make sure every query is successfully execute

#### Part 2: Using the Python script
1. Run the initialization script to create the database and add an admin user:
   ```bash
   python init_db.py
   ```

---

### 3. ⚙️ Environment Configuration

Create a `.env` file in the project root and add your database credentials:

```env
DB_USERNAME=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=foodexpress
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your_secret_key
```

---

### 4. 📥 Install Dependencies

Make sure you have Python and `pip` installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

---

### 5. ▶️ Run the Application

Start the application server:

```bash
python run.py
```

Then open your browser and navigate to: [http://localhost:5000](http://localhost:5000)

---

## 👤 User Accounts

### 🔐 Admin Users

There is one pre-configured admin account:

- **Username:** `admin`
- **Email:** `admin@gmail.com`
- **Password:** `admin123`

> 🛑 Admin has full access to all system features.

### 🙋‍♀️ Regular Users

To create a normal user account, simply go to the **Register** page and sign up.

---

Enjoy ordering with **Food Express**! 🍕🍟🥗
```

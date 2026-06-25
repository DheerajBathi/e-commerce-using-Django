# AuraShop - Premium Django E-Commerce Platform

AuraShop is a modern, responsive, and visually premium e-commerce storefront built with **Python** and **Django**. It is designed with a sleek space-dark theme, featuring smooth micro-animations, glassmorphism panel overlays, and dynamic cart operations.

---

## Key Features

- **Premium UI & Design System:** Tailored dark interface utilizing customized Outfit & Plus Jakarta typography, subtle gradient accents, and responsive card layouts.
- **Interactive Product Catalog:** Browse listings with instant category filtering, query-based search, and price/newest sorting controls.
- **Dynamic Session Cart (AJAX-Enabled):** Modify items and quantities instantly using dynamic JavaScript. Price sub-totals, shipping charges, and total global bag badges calculate in real time without refreshing the page.
- **Secure Simulated Checkout:** Includes checkout stock validation, automated inventory deduction, shipping form collection, and transaction success receipt confirmation.
- **Product Review System:** Real-time feedback console with star-rating UI forms.
- **Robust Admin Dashboard:** Out-of-the-box management dashboard to manage categories, stock status, reviews, and track customer orders.

---

## Tech Stack

- **Backend:** Python 3.10+, Django 5.0+
- **Database:** SQLite (Relational, development ready)
- **Frontend:** HTML5, CSS3 (Vanilla Custom Variable System), JavaScript (ES6 Fetch APIs)
- **Icons:** FontAwesome CDN Integration

---

## Project Architecture

```text
e-commerce/
│
├── ecommerce/                # Project Root Configuration
│   ├── settings.py           # Template engines, apps, and static/media registers
│   ├── urls.py               # Global routing URL mapping
│   └── ...
│
├── store/                    # E-commerce core application
│   ├── models.py             # Schema (Category, Product, Order, OrderItem, Review)
│   ├── views.py              # Storefront listing, cart updates, checkout controllers
│   ├── urls.py               # App-specific routes
│   └── context_processors.py # Global active cart count context injector
│
├── static/css/               # Layout assets
│   └── style.css             # Dark theme design system & animations
│
├── templates/                # HTML layout templates
│   ├── base.html             # Shell framework containing global navbar & headers
│   └── store/                # Views (store, detail, cart, checkout, success)
│
├── populate_db.py            # Idempotent database seeder script
├── setup.bat                 # One-click Windows virtual environment initializer
├── run.bat                   # One-click Windows server loader
└── requirements.txt          # Python package dependency registry
```

---

## Installation & Setup Guide

Ensure you have **Python 3.10+** and **Git** installed on your system.

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/DheerajBathi/e-commerce-using-Django.git
cd e-commerce-using-Django
```

### 2. Setup and Launch

#### Option A: Windows Quick Start (Recommended)
We have included automated batch files to compile your environment instantly.

1. **Initialize and Seed Database:**
   Double-click `setup.bat` (or execute in PowerShell):
   ```powershell
   .\setup.bat
   ```
   *This command creates a virtual environment, installs requirements, sets up the SQLite database, seeds premium mockup products, and prompts you to register an Administrator Superuser account.*

2. **Boot the Local Server:**
   Double-click `run.bat` (or execute in PowerShell):
   ```powershell
   .\run.bat
   ```

3. **Access AuraShop:**
   Open your browser and navigate to:
   - Store Frontpage: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

#### Option B: Manual Setup (Linux / macOS / manual Windows)
If you prefer configuring the environment manually, run the following commands sequentially:

1. **Create and Activate Virtual Environment:**
   ```bash
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows Command Prompt
   python -m venv venv
   call venv\Scripts\activate
   ```

2. **Install Package Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Perform Database Migrations:**
   ```bash
   python manage.py makemigrations store
   python manage.py migrate
   ```

4. **Seed Mock Products & Reviews:**
   ```bash
   python populate_db.py
   ```

5. **Create Superuser Account (Optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start Django Server:**
   ```bash
   python manage.py runserver
   ```
   *View the app in your browser at `http://127.0.0.1:8000/`.*

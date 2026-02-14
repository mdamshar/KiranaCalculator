# 🛒 Kirana Hisaab - Grocery Store Calculator

A modern, user-friendly Django web application designed for Kirana (grocery) store owners to quickly calculate bills, generate receipts, and manage customer records.

![Django](https://img.shields.io/badge/Django-4.1-green.svg)
![Python](https://img.shields.io/badge/Python-3.10.6-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🧾 Receipt Generation
- **Dynamic Product Entry**: Add multiple products with separate name and price inputs
- **Add More Button**: Dynamically add unlimited product rows
- **Auto Calculation**: Automatic total calculation
- **Clean Receipt Display**: Professional receipt format with itemized products

### 📱 Receipt Sharing
- **WhatsApp Integration**: Send receipts directly via WhatsApp
- **SMS Support**: Share receipts via SMS
- **Formatted Messages**: Clean, professional receipt format

### 👥 Customer Management
- **View All Customers**: Complete list of all customer receipts
- **Search Functionality**: Find customers by name (case-insensitive)
- **Date Filtering**: Filter receipts by date range (from/to dates)
- **Delete Receipts**: Remove unwanted receipts with confirmation dialog
- **Detailed View**: Individual receipt pages with full information

### 📞 Contact Page
- **Developer Profile**: Professional portfolio with photo and details
- **Multiple Contact Methods**: Email, Phone, WhatsApp, Location
- **Embedded Google Maps**: Interactive map showing location
- **Services Showcase**: Display of all offered services
- **Social Links**: Quick access to WhatsApp and email

### 🎨 Modern UI/UX
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Gradient Backgrounds**: Beautiful purple and blue gradients
- **Smooth Animations**: Hover effects and transitions
- **Card-Based Layouts**: Clean, modern card designs
- **Professional Typography**: Easy-to-read fonts and spacing

## 🚀 Quick Start

### Prerequisites
- Python 3.10.6 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd kiranahisaab
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv virtual
virtual\Scripts\activate

# Linux/Mac
python3 -m venv virtual
source virtual/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Collect static files**
```bash
python manage.py collectstatic
```

6. **Start the development server**
```bash
python manage.py runserver
```

7. **Open your browser**
```
http://127.0.0.1:8000/
```

## 📁 Project Structure

```
kiranahisaab/
├── kiranacalc/                 # Main application
│   ├── migrations/             # Database migrations
│   ├── static/                 # Static files (CSS, images)
│   │   ├── style.css          # Main calculator page styles
│   │   ├── all.css            # All customers page styles
│   │   ├── detail.css         # Detail page styles
│   │   ├── contact.css        # Contact page styles
│   │   └── myPhoto.png        # Profile photo
│   ├── templates/             # HTML templates
│   │   ├── base.html          # Calculator & receipt page
│   │   ├── all.html           # All customers list
│   │   ├── detail.html        # Individual receipt view
│   │   └── contact.html       # Contact/profile page
│   ├── models.py              # Database models
│   ├── views.py               # View logic
│   ├── urls.py                # URL routing
│   └── admin.py               # Admin configuration
├── kiranahisaab/              # Project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 💻 Usage

### Creating a Receipt

1. Navigate to the homepage
2. Enter customer name
3. Add product name and price for each item
4. Click "Add More" to add additional products
5. Click "Generate Receipt" to create the receipt
6. Optionally send the receipt via WhatsApp or SMS

### Viewing All Customers

1. Click "View All Customers" button
2. Use search box to find specific customers
3. Use date filters to filter by date range
4. Click "View" to see detailed receipt
5. Click "Delete" to remove a receipt (with confirmation)

### Viewing Individual Receipt

1. From the All Customers page, click "View" on any customer
2. See complete receipt details with all items
3. View purchase date and amount

## 🗄️ Database Schema

### calc Model
- `sno` (AutoField): Primary key
- `name` (CharField): Customer name
- `slug` (SlugField): URL-friendly unique identifier
- `amount` (IntegerField): Total bill amount
- `items` (TextField): Comma-separated product list
- `created_at` (DateTimeField): Receipt creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

## 🎨 Customization

### Changing Colors
Edit the CSS files in `kiranacalc/static/`:
- `style.css`: Main calculator page
- `contact.css`: Contact page
- `all.css`: Customer list page

### Updating Profile Information
Edit `kiranacalc/templates/contact.html` and update:
- Name, photo, contact details
- Services offered
- Social media links
- Location coordinates

### Modifying Receipt Format
Edit the `formatReceiptMessage()` function in `base.html` to customize WhatsApp/SMS message format.

## 🚀 Deployment

### Option 1: PythonAnywhere
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code
3. Create virtual environment
4. Configure WSGI file
5. Set ALLOWED_HOSTS in settings.py
6. Collect static files
7. Reload web app

### Option 2: Render
1. Create `build.sh` script
2. Push to GitHub
3. Connect to Render
4. Deploy automatically

### Option 3: Railway
1. Create `Procfile`
2. Push to GitHub
3. Deploy from Railway dashboard

See [Deployment Guide](#deployment) section above for detailed instructions.

## 🔒 Security Notes

Before deploying to production:

1. **Update settings.py**:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = 'your-secret-key'  # Use environment variable
```

2. **Use environment variables** for sensitive data
3. **Enable HTTPS** with SSL certificates
4. **Use PostgreSQL** instead of SQLite in production
5. **Set secure cookies**:
```python
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

## 🐛 Troubleshooting

### Issue: Static files not loading
```bash
python manage.py collectstatic
```

### Issue: Database errors
```bash
python manage.py migrate
```

### Issue: Port already in use
```bash
python manage.py runserver 8080
```

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

**Md Amshar**
- 📧 Email: amsharjlk@gmail.com
- 📱 Phone: +91-9060419628
- 💬 WhatsApp: [Chat Now](https://wa.me/919060419628)
- 📍 Location: Jamui, Bihar

## 🙏 Acknowledgments

- Django Framework
- Font Awesome Icons (via emoji)
- Google Maps Embed API

## 📈 Future Enhancements

- [ ] PDF receipt generation
- [ ] Email receipt functionality
- [ ] Multi-user support with authentication
- [ ] Inventory management
- [ ] Sales analytics and reports
- [ ] Print receipt functionality
- [ ] Customer loyalty program
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Made with ❤️ by Md Amshar** | © 2026 All Rights Reserved

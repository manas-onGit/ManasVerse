# ManasVerse - Django eCommerce Project

ManasVerse is a fully functional eCommerce web application built with **Django** and **Bootstrap**. It features a clean UI, dynamic product listings, shopping cart, user login/signup, and more.

---

## 🚀 Features

- ✅ Home page with responsive carousel
- ✅ Product listing with filters, search, and sort
- ✅ Product detail page
- ✅ Add to cart (session-based, no login required)
- ✅ Cart management (increase, decrease, remove)
- ✅ User login & signup
- ✅ Admin panel (Django default)
- ✅ Clean and responsive UI using Bootstrap + Custom CSS

---

## 🧰 Tech Stack

- Backend: Django (Python)
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite (default Django DB)
- Version Control: Git & GitHub

---

## 💻 How to Run Locally

```bash
git clone https://github.com/manas-onGit/ManasVerse.git
cd ManasVerse
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

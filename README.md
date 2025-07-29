# 🛒 E-Commerce Backend - ProDev BE

A scalable, secure, and high-performance backend system for an e-commerce platform. This project simulates a real-world backend architecture, handling product management, user authentication, and providing robust APIs with filtering, sorting, and pagination capabilities.

---

## 🚀 Features

- ✅ **User Authentication**  
  - Secure JWT-based login and registration  
  - Role-based user management (admin, customer)

- 📦 **Product Management**  
  - CRUD APIs for products and categories  
  - Image upload support (optional)

- 🔍 **Advanced Product API**  
  - Filtering by category  
  - Sorting by price  
  - Pagination for large datasets

- 📄 **API Documentation**  
  - Interactive Swagger/OpenAPI docs

- ⚙️ **Database Optimization**  
  - Indexing for high-performance queries  
  - Relational schema using PostgreSQL

---

## 🧑‍💻 Tech Stack

| Tool                               | Usage                             |
|------------------------------------|-----------------------------------|
| Django                             | Web framework                     |
| Django REST Framework              | API development                   |
| PostgreSQL                         | Relational database               |
| djangorestframework-simplejwt      | JWT Authentication                |
| drf-yasg                           | Swagger/OpenAPI documentation     |
| Docker (optional)                  | Containerized deployment          |

---

## 📁 Project Structure

```
ecommerce-backend/
├── ecommerce/              # Django project settings
├── store/                  # App for product & category models and APIs
├── users/                  # App for user authentication and management
├── requirements.txt        # Python dependencies
├── manage.py
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ecommerce-backend.git
cd ecommerce-backend
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/ecommerce
REDIS_URL=redis://localhost:6379
```

### 4. Apply migrations and create superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

---

## 🔐 Authentication

JWT-based authentication using [`djangorestframework-simplejwt`](https://django-rest-framework-simplejwt.readthedocs.io/).

### Obtain Token

```http
POST /api/token/
Content-Type: application/json

{
  "username": "your-username",
  "password": "your-password"
}
```

Use the access token in Authorization headers:

```http
Authorization: Bearer <your_access_token>
```

---

## 📚 API Documentation

Interactive Swagger documentation available at:

```
http://localhost:8000/api/docs/
```

---

## ✅ Available Endpoints

### Authentication

* `POST /api/token/` – Obtain JWT access & refresh tokens
* `POST /api/token/refresh/` – Refresh the access token
* `POST /api/register/` – Register a new user

### Products

* `GET /api/products/` – List products (filtering, sorting, pagination)
* `POST /api/products/` – Create a new product (admin only)
* `GET /api/products/<id>/` – Retrieve a product
* `PUT /api/products/<id>/` – Update a product (admin only)
* `DELETE /api/products/<id>/` – Delete a product (admin only)

### Categories

* `GET /api/categories/` – List categories
* `POST /api/categories/` – Create a category (admin only)
* `GET /api/categories/<id>/` – Retrieve a category
* `PUT /api/categories/<id>/` – Update a category (admin only)
* `DELETE /api/categories/<id>/` – Delete a category (admin only)

---

## ⚡ Query Features

### Filtering

```http
GET /api/products/?category=electronics
```

### Sorting

```http
GET /api/products/?ordering=price
GET /api/products/?ordering=-price   # Descending
```

### Pagination (PageNumber)

```http
GET /api/products/?page=2&page_size=10
```

---

## 📈 Performance Optimizations

* **Database Indexing** on `price` and `category` fields
* **Query optimizations** using `select_related()` and `prefetch_related()`
* **Redis caching** for frequent read endpoints (optional)

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 🔄 Git Commit Conventions

Use the following prefixes in commit messages:

* `feat:` New feature
* `fix:` Bug fix
* `docs:` Documentation only
* `style:` Code formatting
* `refactor:` Code change without feature or fix
* `perf:` Performance improvements

---

## 📤 Deployment

1. Ensure PostgreSQL and Redis are running on the server.
2. Set environment variables in the production environment.
3. Use a WSGI server (e.g., Gunicorn) behind a reverse proxy (e.g., Nginx).
4. Optionally deploy with Docker and Docker Compose.
5. CI/CD pipelines (GitHub Actions) can automate tests and deployment.

---

## 🧑‍💼 Author

**Kamal**  
Aspiring Back-End Developer  
[Portfolio](https://yourwebsite.com)

---

## 📄 License

This project is licensed under the MIT License.
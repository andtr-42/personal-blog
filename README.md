# Personal Blog

A robust, highly available RESTful API backend for a Markdown-based personal blog website. Built with Django and designed to handle read-heavy traffic with sub-200ms latency while ensuring stricit data durability for blog post content. 

## Tech Stack

* **Backend:** Django
* **Frontend:** HTMX
* **Databse:** PostgreSQL
* **Authentication:** Simple JWT
* **Caching/Task Queue:** Redis
* **Documentation:** Swagger/OpenAPI


## System Architecture & Constraints 

* **Primary Focus:** High Availability and Low Latency.
* **Target Scale:** Up to 10k Daily Active Users (DAU).
* **Latency Goal:** Less than 200ms for read operations.
* **Data Durability:** Strict. Core text content (posts/comments) must be durable and no data loss should occur. Eventual consistency is accepted only for non-critical metrics (e.g., view counts)

## Key Features

* **JWT Authentication:** Secure sign-up and login flows.
* **Role-Based Access Control:** Strict seperation between `Admin` (Writers) and `Readers`.
* **Markdown Support:** Full support for Markdown formatting in blog posts.
* **Full-Text Search:** Optimized querying for post titles and contents. 

## Core Entities

* **Users (Reader/Writer):** Handles authentication and permissions.
* **Post:** The core blog content, authored by Admins.
* **Comment:** User-generated interactions tied to specific posts.  

## API Reference

### Authentication
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `POST` | `/v1/auth/register` | Register a new reader account | Public |
| `POST` | `/v1/auth/login` | Authenticate and receive JWT tokens | Public |

### Posts
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/v1/posts/` | List posts (Supports `?page=`, `&limit=`, `&search=`) | Public |
| `GET` | `/v1/posts/{post_id}` | Retrieve a specific post | Public |
| `POST` | `/v1/posts/` | Create a new Markdown post | **Admin** |
| `PUT` | `/v1/posts/{post_id}` | Update an existing post | **Admin** |
| `DELETE` | `/v1/posts/{post_id}` | Delete a post | **Admin** |

### Comments
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/v1/posts/{post_id}/comments/` | List all comments for a post | Public |
| `GET` | `/v1/comments/{comment_id}` | Retrieve a specific comment | Public |
| `POST` | `/v1/posts/{post_id}/comments/`| Add a comment to a post | **Reader** |
| `PUT` | `/v1/comments/{comment_id}` | Update a comment | **Reader** (Author only) |
| `DELETE` | `/v1/comments/{comment_id}` | Delete a comment | **Reader** (Author only) |

## 🚀 Local Setup & Installation

*(Provide step-by-step instructions here on how another developer can run your project)*

```bash
# 1. Clone the repository

git clone https://github.com/andtr-42/personal-blog.git
cd personal-blog

# 2. Create a virtual environment

python -m venv venv
source venv/bin/activate  

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env

# 5. Run database migrations
python manage.py migrate

# 6. Start the development server
python manage.py runserver

```

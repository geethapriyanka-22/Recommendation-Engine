# 🛒 NovaMart — AI-Powered E-Commerce Platform

A production-style, full-stack e-commerce application with AI-powered semantic search and product recommendations. Built with FastAPI, PostgreSQL + pgvector, and React.

## Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.12, FastAPI, SQLAlchemy (Async), Pydantic v2, Alembic |
| **Database** | PostgreSQL 16 + pgvector (unified relational + vector storage) |
| **AI** | SentenceTransformers (`all-MiniLM-L6-v2`), Hybrid Search, Product Recommendations |
| **Auth** | JWT (HS256), bcrypt, Role-Based Access Control |
| **Frontend** | React 18, Vite, Modern CSS (Glassmorphism, Dark Mode) |
| **DevOps** | Docker, Docker Compose, Multi-stage Builds |

## Features

- 🔐 **JWT Authentication** with refresh tokens and RBAC (customer / seller / admin)
- 🛍️ **Full Shopping Flow** — browse, search, cart, checkout, order tracking
- 🤖 **AI Semantic Search** — natural language product search via vector embeddings
- 💡 **Product Recommendations** — "similar products" powered by cosine similarity
- 📊 **Admin Dashboard** — order management, user management, stats
- 🎨 **Premium UI** — glassmorphism, micro-animations, dark/light theme
- 🏭 **Synthetic Data Engine** — generates 150+ realistic products, reviews, orders

## Quick Start

```bash
# 1. Clone and configure
cp .env.example .env

# 2. Build and start all services
docker-compose up --build -d

# 3. Access the application
#    Frontend:  http://localhost:5173
#    API Docs:  http://localhost:8000/docs
#    Database:  localhost:5432
```

## Default Accounts (after seeding)

| Role | Email | Password |
|---|---|---|
| Admin | `admin@novamart.com` | `Admin123!` |
| Seller | `seller@novamart.com` | `Seller123!` |
| Customer | `customer@novamart.com` | `Customer123!` |

## Project Structure

```
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── app/
│   │   ├── api/v1/          # Route handlers
│   │   ├── core/            # Config, DB, Auth, Dependencies
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic request/response models
│   │   ├── services/        # Business logic layer
│   │   └── generator/       # Synthetic data engine
│   ├── alembic/             # Database migrations
│   └── Dockerfile
└── frontend/
    ├── src/
    │   ├── components/      # Reusable UI components
    │   ├── pages/           # Route pages
    │   ├── context/         # React context providers
    │   └── styles/          # CSS design system
    └── Dockerfile
```

## Architecture

```
Request → FastAPI Router → Service Layer → Repository/ORM → PostgreSQL
                                ↕
                        Vector Service → pgvector (HNSW index)
                                ↕
                        SentenceTransformers (local embeddings)
```

## License

MIT

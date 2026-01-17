# 🏋️ GymBuddy

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![React Native](https://img.shields.io/badge/React%20Native-0.73-blueviolet.svg)](https://reactnative.dev/)
[![Expo](https://img.shields.io/badge/Expo-SDK%2050-white.svg)](https://expo.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **"Strava meets Meetup for gym enthusiasts"**

A social fitness app that bridges the gap between solo gym routines and group motivation. Find workout partners, schedule sessions together, and stay accountable with friends.

<p align="center">
  <img src="docs/images/app-preview.png" alt="GymBuddy App Preview" width="600">
</p>

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [🎯 Vision](wiki/Vision.md) | The idea behind GymBuddy |
| [✨ Features](wiki/Features.md) | Feature guide with visual examples |
| [🗺️ Roadmap](wiki/Roadmap.md) | Development timeline & future plans |
| [🏗️ Architecture](wiki/Architecture.md) | Technical design & decisions |
| [📱 User Guide](wiki/User-Guide.md) | How to use the app |
| [🔌 API Reference](wiki/API-Reference.md) | REST API documentation |

---

## ✨ Features

### Core (MVP) ✅
- 🔐 **Authentication** - Email/password registration with JWT
- 👤 **Profiles** - Bio, training level, privacy settings
- 👥 **Friends & Groups** - Connect and organize
- 🏢 **Gyms** - Search, save favorites, add custom locations
- 📅 **Sessions** - Create, join, RSVP, check-in
- 💪 **Exercises** - Plan workouts with sets/reps
- 📨 **Invites** - Invite friends to sessions

### Coming Soon 🚧
- 🔔 Push notifications
- 💬 Session chat
- 📊 Progress tracking
- 🏆 Achievements & streaks

---

## 🏗️ Architecture

```
GymBuddy/
├── backend/          # FastAPI Python backend
│   ├── app/          # Application code
│   ├── alembic/      # Database migrations
│   └── tests/        # Pytest test suite
├── mobile/           # React Native app (iOS/Android)
│   └── src/          # App source code
├── infra/            # AWS CDK infrastructure
├── wiki/             # Documentation
└── postman/          # API collection
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.11+ / FastAPI / SQLAlchemy 2.0 / asyncpg |
| **Database** | PostgreSQL 15 |
| **Mobile** | React Native / Expo SDK 50 / TypeScript |
| **State** | Zustand / React Query |
| **Auth** | JWT (python-jose / passlib) |
| **Cloud** | AWS (ECS Fargate, RDS, ALB) via CDK |

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/ahmedul/GymBuddy.git
cd GymBuddy

# Start all services
docker compose up -d

# Run database migrations
docker compose exec api alembic upgrade head

# API is now running at http://localhost:8000
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql+asyncpg://gymbuddy:gymbuddy@localhost:5433/gymbuddy"
export SECRET_KEY="your-secret-key"

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

**Mobile:**
```bash
cd mobile
npm install
npx expo start
```

---

## 🧪 Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

---

## 📖 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Postman Collection**: [postman/GymBuddy.postman_collection.json](postman/GymBuddy.postman_collection.json)

---

## 🗺️ Roadmap

| Phase | Timeline | Focus |
|-------|----------|-------|
| **Phase 1** ✅ | Q4 2025 - Q1 2026 | MVP - Core features |
| **Phase 2** 🚧 | Q2 2026 | Enhanced Social - Notifications, Feed, Chat |
| **Phase 3** 📋 | Q3 2026 | Smart Features - Progress, Achievements |
| **Phase 4** 📋 | Q4 2026 | Scale - Premium, Analytics, Partnerships |

See the full [Roadmap](wiki/Roadmap.md) for details.

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

- **GitHub**: [github.com/ahmedul/GymBuddy](https://github.com/ahmedul/GymBuddy)
- **Issues**: [Report bugs or request features](https://github.com/ahmedul/GymBuddy/issues)

---

<p align="center">
  Made with 💪 by the GymBuddy Team
</p>

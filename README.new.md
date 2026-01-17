# 🏋️ GymBuddy

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React Native](https://img.shields.io/badge/React%20Native-Expo%20SDK%2050-61DAFB?logo=react)](https://expo.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://docs.docker.com/compose/)
[![Tests](https://img.shields.io/badge/Tests-99%20Passing-brightgreen?logo=pytest)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **"Strava meets Meetup for gym enthusiasts"** - A social fitness app that bridges the gap between solo gym routines and group motivation.

<p align="center">
  <img src="docs/images/hero-mockup.png" alt="GymBuddy App Preview" width="800">
</p>

## 📖 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Roadmap](#-roadmap)
- [Documentation](#-documentation)
- [Contributing](#-contributing)

## ✨ Features

### 🎯 Core Features (MVP)

| Feature | Description | Status |
|---------|-------------|--------|
| 🔐 **Authentication** | Email/password login with JWT tokens | ✅ Complete |
| 👤 **User Profiles** | Customizable profiles with fitness goals | ✅ Complete |
| 👥 **Friends System** | Send/accept friend requests, view activity | ✅ Complete |
| 🏢 **Gym Discovery** | Search gyms by name/location, save favorites | ✅ Complete |
| 📅 **Workout Sessions** | Create, join, and manage group workouts | ✅ Complete |
| 💪 **Exercise Plans** | Add exercises with sets, reps, and notes | ✅ Complete |
| 📨 **Session Invites** | Invite friends and groups to workouts | ✅ Complete |
| 👥 **Workout Groups** | Create and manage workout communities | ✅ Complete |

### 📱 User Experience

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER JOURNEY                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   📱 Download App     →    🔐 Create Account    →    👤 Setup Profile│
│                                                                      │
│        ↓                         ↓                        ↓          │
│                                                                      │
│   🏢 Find Gyms        →    👥 Add Friends       →    📅 Create Session│
│                                                                      │
│        ↓                         ↓                        ↓          │
│                                                                      │
│   📨 Invite Buddies   →    💪 Workout Together  →    ⭐ Track Progress│
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 📸 Screenshots

> 📚 **Full visual documentation**: [docs/FEATURES.md](docs/FEATURES.md)

### App Screens Overview

| Feed | Session Details | Create Session |
|:----:|:---------------:|:--------------:|
| ![Feed](docs/images/screen-feed.png) | ![Session](docs/images/screen-session.png) | ![Create](docs/images/screen-create.png) |
| View friends' workouts | RSVP and see participants | Schedule new workouts |

| Find Gyms | Friends | Profile |
|:---------:|:-------:|:-------:|
| ![Gyms](docs/images/screen-gyms.png) | ![Friends](docs/images/screen-friends.png) | ![Profile](docs/images/screen-profile.png) |
| Search nearby gyms | Manage connections | Edit your profile |

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MOBILE CLIENTS                               │
│                    iOS & Android (React Native)                      │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │ HTTPS/JWT
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AWS Application Load Balancer                     │
│                         (SSL Termination)                            │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       ECS FARGATE CLUSTER                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    FastAPI Backend                             │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │  │
│  │  │  Auth   │ │  Users  │ │ Sessions│ │  Gyms   │ │ Social  │  │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AMAZON RDS POSTGRESQL                           │
│                    (Multi-AZ, Auto-backup)                          │
└─────────────────────────────────────────────────────────────────────┘
```

## 🛠 Tech Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Backend** | FastAPI | 0.109 | Async REST API |
| **ORM** | SQLAlchemy | 2.0 | Database operations |
| **Database** | PostgreSQL | 15 | Persistent storage |
| **Mobile** | React Native | Expo SDK 50 | Cross-platform app |
| **State** | Zustand + React Query | Latest | Client state management |
| **Auth** | JWT | python-jose | Token authentication |
| **Infra** | AWS CDK | TypeScript | Infrastructure as Code |
| **Container** | Docker | Compose | Local development |

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for mobile development)
- Git

### 1️⃣ Clone & Start

```bash
# Clone the repository
git clone https://github.com/ahmedul/GymBuddy.git
cd GymBuddy

# Start all services
docker compose up -d

# Run database migrations
docker compose exec api alembic upgrade head

# ✅ API running at http://localhost:8000
```

### 2️⃣ Test the API

```bash
# Health check
curl http://localhost:8000/health

# Open Swagger UI
open http://localhost:8000/docs
```

### 3️⃣ Run Mobile App

```bash
cd mobile
npm install
npx expo start
```

### 4️⃣ Run Tests

```bash
docker compose exec api pytest tests/ -v
# ✅ 99 tests passing
```

## 📚 API Documentation

### Interactive Docs

| Tool | URL | Description |
|------|-----|-------------|
| Swagger UI | http://localhost:8000/docs | Interactive API explorer |
| ReDoc | http://localhost:8000/redoc | API reference |
| Postman | [postman/GymBuddy.postman_collection.json](postman/GymBuddy.postman_collection.json) | Import for testing |

### Key Endpoints

```
Authentication
├── POST   /api/v1/auth/register     # Create account
├── POST   /api/v1/auth/login        # Get JWT token
└── GET    /api/v1/auth/me           # Current user

Users
├── GET    /api/v1/users/me          # My profile
├── PATCH  /api/v1/users/me          # Update profile
└── GET    /api/v1/users/{id}        # View user

Social
├── GET    /api/v1/friends           # List friends
├── POST   /api/v1/friends/request   # Send request
├── POST   /api/v1/friends/requests/{id}/accept
├── GET    /api/v1/groups            # My groups
└── POST   /api/v1/groups            # Create group

Gyms
├── GET    /api/v1/gyms              # Search gyms
├── POST   /api/v1/gyms              # Add custom gym
├── GET    /api/v1/gyms/favorites    # My favorites
└── POST   /api/v1/gyms/favorites/{id}

Sessions
├── GET    /api/v1/sessions          # Session feed
├── POST   /api/v1/sessions          # Create session
├── POST   /api/v1/sessions/{id}/join
├── POST   /api/v1/sessions/{id}/exercises
└── POST   /api/v1/sessions/{id}/invite
```

## 📁 Project Structure

```
GymBuddy/
├── 📂 backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── api/v1/            # API routes (auth, users, sessions, gyms, social)
│   │   ├── core/              # Config, security, dependencies
│   │   ├── crud/              # Database operations
│   │   ├── models/            # SQLAlchemy models
│   │   └── schemas/           # Pydantic schemas
│   ├── tests/                 # Pytest test suite (99 tests)
│   ├── alembic/               # Database migrations
│   └── requirements.txt
│
├── 📂 mobile/                  # React Native Expo app
│   ├── src/
│   │   ├── api/               # API client
│   │   ├── hooks/             # React Query hooks
│   │   ├── navigation/        # Navigation config
│   │   ├── screens/           # App screens
│   │   └── store/             # Zustand store
│   └── package.json
│
├── 📂 infra/                   # AWS CDK infrastructure
│   └── lib/                   # Stack definitions
│
├── 📂 docs/                    # Documentation & wiki
│   ├── FEATURES.md            # Feature documentation
│   ├── ROADMAP.md             # Detailed roadmap
│   └── images/                # Screenshots & diagrams
│
├── 📂 postman/                 # API testing collection
├── docker-compose.yml          # Local development
└── README.md
```

## 🗺 Roadmap

> 📋 **Detailed roadmap**: [docs/ROADMAP.md](docs/ROADMAP.md)

### Phase 1: MVP ✅ (Complete)
- [x] User authentication (JWT)
- [x] User profiles & settings
- [x] Friend system
- [x] Workout groups
- [x] Gym search & favorites
- [x] Session management
- [x] Exercise planning
- [x] Session invites

### Phase 2: Social Enhancement 🚧 (Q2 2026)
- [ ] Push notifications
- [ ] In-app messaging
- [ ] Activity feed with likes/comments
- [ ] Session photos & media
- [ ] Streak tracking

### Phase 3: Smart Features 📋 (Q3 2026)
- [ ] Workout templates/routines
- [ ] Progress analytics
- [ ] Achievement badges
- [ ] AI workout recommendations
- [ ] Calendar integration

### Phase 4: Growth 🚀 (Q4 2026)
- [ ] Public gym database (Google Places)
- [ ] Trainer profiles
- [ ] Premium subscriptions
- [ ] Corporate wellness programs
- [ ] API for third-party integrations

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [docs/FEATURES.md](docs/FEATURES.md) | Visual feature guide with screenshots |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Detailed project roadmap |
| [docs/API.md](docs/API.md) | API reference documentation |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | Contribution guidelines |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment guide |

## 🤝 Contributing

We welcome contributions! See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

```bash
# Fork, clone, and create a branch
git checkout -b feature/amazing-feature

# Make changes and run tests
docker compose exec api pytest tests/

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Open a Pull Request
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <b>Built with 💪 for fitness enthusiasts everywhere</b>
  <br><br>
  <a href="https://github.com/ahmedul/GymBuddy/stargazers">⭐ Star us on GitHub</a>
  ·
  <a href="https://github.com/ahmedul/GymBuddy/issues">🐛 Report Bug</a>
  ·
  <a href="https://github.com/ahmedul/GymBuddy/issues">💡 Request Feature</a>
</p>

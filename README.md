# GymBuddy - Social Fitness App

A social fitness app that bridges the gap between solo gym routines and group motivation.

## Architecture

```
├── backend/          # FastAPI Python backend
├── mobile/           # React Native app (iOS/Android)
└── infra/            # AWS CDK infrastructure
```

## Tech Stack

- **Backend**: Python 3.11+ / FastAPI / SQLAlchemy / PostgreSQL
- **Mobile**: React Native / Expo / TypeScript
- **Auth**: AWS Cognito (OAuth + email/password)
- **Cloud**: AWS (ECS Fargate, RDS, S3, CloudFront)

## MVP Features

1. **Accounts & Identity** - OAuth, profiles, privacy settings
2. **Friends & Groups** - Add friends, create groups
3. **Gyms & Locations** - Search, save favorites
4. **Session Announcements** - Create, join, RSVP to sessions
5. **Exercise Plans** - Add exercises to sessions

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Mobile
```bash
cd mobile
npm install
npx expo start
```

## API Documentation

Once running: http://localhost:8000/docs

# 📚 API Reference

> Complete API documentation for GymBuddy backend.

## Base URL

```
Development: http://localhost:8000
Production:  https://api.gymbuddy.app
```

## Authentication

All protected endpoints require a JWT bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

### Get Token

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secretpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/auth/register` | Create new account | ❌ |
| `POST` | `/api/v1/auth/login` | Get access token | ❌ |
| `GET` | `/api/v1/auth/me` | Get current user | ✅ |

### Users

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/users/me` | Get my profile | ✅ |
| `PATCH` | `/api/v1/users/me` | Update my profile | ✅ |
| `GET` | `/api/v1/users/{user_id}` | Get user by ID | ✅ |

### Friends

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/friends` | List my friends | ✅ |
| `POST` | `/api/v1/friends/request` | Send friend request | ✅ |
| `GET` | `/api/v1/friends/requests` | List pending requests | ✅ |
| `POST` | `/api/v1/friends/requests/{id}/accept` | Accept request | ✅ |
| `POST` | `/api/v1/friends/requests/{id}/reject` | Reject request | ✅ |
| `DELETE` | `/api/v1/friends/{user_id}` | Unfriend user | ✅ |

### Groups

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/groups` | List my groups | ✅ |
| `POST` | `/api/v1/groups` | Create group | ✅ |
| `GET` | `/api/v1/groups/{id}` | Get group details | ✅ |
| `PATCH` | `/api/v1/groups/{id}` | Update group | ✅ |
| `DELETE` | `/api/v1/groups/{id}` | Delete group | ✅ |
| `POST` | `/api/v1/groups/{id}/join` | Join group | ✅ |
| `POST` | `/api/v1/groups/{id}/leave` | Leave group | ✅ |
| `POST` | `/api/v1/groups/{id}/members` | Add member | ✅ |
| `DELETE` | `/api/v1/groups/{id}/members/{user_id}` | Remove member | ✅ |

### Gyms

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/gyms` | Search gyms | ✅ |
| `POST` | `/api/v1/gyms` | Create gym | ✅ |
| `GET` | `/api/v1/gyms/{id}` | Get gym details | ✅ |
| `GET` | `/api/v1/gyms/favorites` | List favorite gyms | ✅ |
| `POST` | `/api/v1/gyms/favorites/{id}` | Add to favorites | ✅ |
| `DELETE` | `/api/v1/gyms/favorites/{id}` | Remove from favorites | ✅ |

### Sessions

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/sessions` | List sessions (feed) | ✅ |
| `POST` | `/api/v1/sessions` | Create session | ✅ |
| `GET` | `/api/v1/sessions/{id}` | Get session details | ✅ |
| `PATCH` | `/api/v1/sessions/{id}` | Update session | ✅ |
| `DELETE` | `/api/v1/sessions/{id}` | Delete session | ✅ |
| `POST` | `/api/v1/sessions/{id}/join` | Join session | ✅ |
| `POST` | `/api/v1/sessions/{id}/leave` | Leave session | ✅ |
| `GET` | `/api/v1/sessions/{id}/exercises` | List exercises | ✅ |
| `POST` | `/api/v1/sessions/{id}/exercises` | Add exercise | ✅ |
| `PATCH` | `/api/v1/sessions/{id}/exercises/{ex_id}` | Update exercise | ✅ |
| `DELETE` | `/api/v1/sessions/{id}/exercises/{ex_id}` | Delete exercise | ✅ |
| `POST` | `/api/v1/sessions/{id}/invite` | Send invitations | ✅ |

---

## Request/Response Examples

### Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Smith"
}
```

**Response (201):**
```json
{
  "id": "uuid-here",
  "email": "john@example.com",
  "full_name": "John Smith",
  "created_at": "2026-01-15T10:30:00Z"
}
```

### Create Session

```http
POST /api/v1/sessions
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Leg Day Session",
  "description": "Heavy squats and lunges",
  "gym_id": "gym-uuid",
  "scheduled_at": "2026-01-16T06:00:00Z",
  "duration_minutes": 90,
  "max_participants": 8
}
```

**Response (201):**
```json
{
  "id": "session-uuid",
  "title": "Leg Day Session",
  "description": "Heavy squats and lunges",
  "gym": {
    "id": "gym-uuid",
    "name": "LA Fitness"
  },
  "organizer": {
    "id": "user-uuid",
    "full_name": "John Smith"
  },
  "scheduled_at": "2026-01-16T06:00:00Z",
  "duration_minutes": 90,
  "max_participants": 8,
  "participant_count": 1,
  "created_at": "2026-01-15T10:30:00Z"
}
```

### Add Exercise

```http
POST /api/v1/sessions/{session_id}/exercises
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Barbell Squats",
  "sets": 4,
  "reps": "8-10",
  "weight": "185 lbs",
  "notes": "Focus on depth",
  "order": 1
}
```

### Send Invitations

```http
POST /api/v1/sessions/{session_id}/invite
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_ids": ["user-1-uuid", "user-2-uuid"],
  "group_ids": ["group-uuid"],
  "message": "Let's crush leg day together! 💪"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Rate Limiting

| Tier | Requests/Minute | Burst |
|------|-----------------|-------|
| Free | 60 | 100 |
| Premium | 300 | 500 |
| API Partner | 1000 | 2000 |

Rate limit headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642012800
```

---

## Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

<p align="center">
  <a href="README.md">← Back to README</a>
</p>

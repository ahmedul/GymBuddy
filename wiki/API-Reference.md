# 🔌 API Reference

Complete REST API documentation for GymBuddy.

**Base URL:** `http://localhost:8000/api/v1` (development)

---

## Authentication

All protected endpoints require a Bearer token:

```
Authorization: Bearer <access_token>
```

---

## Endpoints

### Auth

#### Register
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "training_level": "beginner",
  "visibility": "private",
  "is_verified": false,
  "created_at": "2026-01-17T12:00:00Z"
}
```

---

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded
```

**Request Body:**
```
username=user@example.com&password=SecurePass123!
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "photo_url": null,
  "bio": null,
  "training_level": "beginner",
  "visibility": "private",
  "is_verified": false,
  "created_at": "2026-01-17T12:00:00Z"
}
```

---

### Users

#### Get My Profile
```http
GET /users/me
Authorization: Bearer <token>
```

---

#### Update My Profile
```http
PATCH /users/me
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "John D.",
  "bio": "Fitness enthusiast",
  "training_level": "intermediate",
  "visibility": "friends"
}
```

---

#### Get User Profile
```http
GET /users/{user_id}
Authorization: Bearer <token>
```

**Response:** `200 OK` (public response - limited fields)
```json
{
  "id": "uuid",
  "name": "John Doe",
  "photo_url": null,
  "bio": "Fitness enthusiast",
  "training_level": "intermediate"
}
```

---

### Friends

#### Send Friend Request
```http
POST /friends/request
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "addressee_id": "user-uuid"
}
```

---

#### List Friends
```http
GET /friends
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
[
  {
    "user": {
      "id": "uuid",
      "name": "Jane Doe",
      "photo_url": null
    },
    "friendship_id": "uuid",
    "since": "2026-01-15T10:00:00Z"
  }
]
```

---

#### List Pending Requests
```http
GET /friends/requests
Authorization: Bearer <token>
```

---

#### Accept Friend Request
```http
POST /friends/requests/{friendship_id}/accept
Authorization: Bearer <token>
```

---

#### Decline Friend Request
```http
POST /friends/requests/{friendship_id}/decline
Authorization: Bearer <token>
```

---

### Groups

#### Create Group
```http
POST /groups
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "Morning Lifters",
  "description": "6AM crew at Iron Paradise",
  "is_public": false
}
```

---

#### List My Groups
```http
GET /groups
Authorization: Bearer <token>
```

---

#### Get Group
```http
GET /groups/{group_id}
Authorization: Bearer <token>
```

---

#### Update Group
```http
PATCH /groups/{group_id}
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "Updated Name",
  "description": "New description"
}
```

---

### Gyms

#### Search Gyms
```http
GET /gyms?q=iron&lat=40.7128&lon=-74.0060&radius=10
```

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| q | string | Search query |
| lat | float | Latitude |
| lon | float | Longitude |
| radius | float | Radius in km (default: 10) |

---

#### Create Gym
```http
POST /gyms
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "My Home Gym",
  "address": "123 Main St, City",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

---

#### Get Gym
```http
GET /gyms/{gym_id}
```

---

#### List Favorite Gyms
```http
GET /gyms/favorites
Authorization: Bearer <token>
```

---

#### Add Gym to Favorites
```http
POST /gyms/favorites/{gym_id}
Authorization: Bearer <token>
```

**Response:** `204 No Content`

---

#### Remove Gym from Favorites
```http
DELETE /gyms/favorites/{gym_id}
Authorization: Bearer <token>
```

---

### Sessions

#### Get Session Feed
```http
GET /sessions?include_public=true
Authorization: Bearer <token>
```

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| from_date | datetime | Start date filter |
| to_date | datetime | End date filter |
| include_public | bool | Include public sessions |

---

#### Create Session
```http
POST /sessions
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Morning Chest Day",
  "description": "Focus on bench press",
  "gym_id": "gym-uuid",
  "scheduled_at": "2026-01-20T07:00:00Z",
  "duration_minutes": 90,
  "visibility": "friends",
  "max_participants": 6,
  "exercises": [
    {
      "name": "Bench Press",
      "sets": 4,
      "reps": "8-10",
      "order": 1
    }
  ]
}
```

---

#### Get Session
```http
GET /sessions/{session_id}
Authorization: Bearer <token>
```

---

#### Update Session
```http
PATCH /sessions/{session_id}
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "max_participants": 8
}
```

---

#### Delete Session
```http
DELETE /sessions/{session_id}
Authorization: Bearer <token>
```

---

#### Join Session
```http
POST /sessions/{session_id}/join
Authorization: Bearer <token>
```

---

#### Leave Session
```http
POST /sessions/{session_id}/leave
Authorization: Bearer <token>
```

---

#### Update RSVP
```http
POST /sessions/{session_id}/rsvp
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "status": "going"  // "going", "maybe", "not_going"
}
```

---

#### Check In
```http
POST /sessions/{session_id}/check-in
Authorization: Bearer <token>
```

---

#### Invite Users
```http
POST /sessions/{session_id}/invite
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "user_ids": ["uuid1", "uuid2"],
  "message": "Join us for this workout!"
}
```

---

#### Add Exercise
```http
POST /sessions/{session_id}/exercises
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "Lat Pulldown",
  "sets": 3,
  "reps": "12-15",
  "notes": "Wide grip",
  "order": 2
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
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
  "detail": "Only the creator can update this session"
}
```

### 404 Not Found
```json
{
  "detail": "Session not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## Data Types

### Training Level
```
"beginner" | "intermediate" | "advanced"
```

### Profile Visibility
```
"public" | "friends" | "private"
```

### Session Visibility
```
"public" | "friends" | "private" | "group"
```

### RSVP Status
```
"going" | "maybe" | "not_going" | "invited"
```

### Friendship Status
```
"pending" | "accepted" | "declined" | "blocked"
```

---

## Postman Collection

Import the [Postman Collection](../postman/GymBuddy.postman_collection.json) for easy testing.

---

*For interactive docs, visit `/docs` when running the API locally.*

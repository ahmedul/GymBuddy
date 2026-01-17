# 🤝 Contributing to GymBuddy

Thank you for your interest in contributing to GymBuddy! This guide will help you get started.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what's best for the community
- Show empathy towards others

---

## Getting Started

### Find Something to Work On

1. **Good First Issues**: Look for issues labeled `good-first-issue`
2. **Bug Fixes**: Check issues labeled `bug`
3. **Feature Requests**: Review `enhancement` labels
4. **Documentation**: Help improve docs with `documentation` label

### Before You Start

1. Check if an issue already exists
2. Comment on the issue to claim it
3. Wait for maintainer assignment
4. Fork the repository

---

## Development Setup

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Git

### Clone & Setup

```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/GymBuddy.git
cd GymBuddy

# Add upstream remote
git remote add upstream https://github.com/ahmedul/GymBuddy.git

# Start development environment
docker compose up -d

# Run migrations
docker compose exec api alembic upgrade head

# Verify setup
curl http://localhost:8000/health
```

### Mobile Development

```bash
cd mobile
npm install
npx expo start
```

---

## Making Changes

### Create a Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/description` | `feature/push-notifications` |
| Bug Fix | `fix/description` | `fix/login-validation` |
| Docs | `docs/description` | `docs/api-examples` |
| Refactor | `refactor/description` | `refactor/auth-module` |

### Commit Messages

Use conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```bash
git commit -m "feat(sessions): add exercise reordering"
git commit -m "fix(auth): handle expired token refresh"
git commit -m "docs(api): add session examples"
```

---

## Pull Request Process

### Before Submitting

1. **Run Tests**
   ```bash
   docker compose exec api pytest tests/ -v
   ```

2. **Check Linting**
   ```bash
   # Python
   docker compose exec api ruff check app/
   
   # TypeScript
   cd mobile && npm run lint
   ```

3. **Update Documentation** if needed

4. **Sync with Main**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### Submit PR

1. Push your branch
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open Pull Request on GitHub

3. Fill out the PR template:
   - **Description**: What does this PR do?
   - **Related Issue**: Closes #123
   - **Type**: Feature / Bug Fix / Docs
   - **Testing**: How was this tested?
   - **Screenshots**: If UI changes

### PR Review

- Maintainers will review within 48 hours
- Address feedback with additional commits
- Once approved, maintainers will merge

---

## Coding Standards

### Python (Backend)

```python
# Follow PEP 8
# Use type hints
async def create_session(
    db: AsyncSession,
    session_data: SessionCreate,
    user_id: UUID
) -> Session:
    """Create a new workout session."""
    ...

# Use async/await consistently
# Document public functions
# Keep functions focused and small
```

### TypeScript (Mobile)

```typescript
// Use functional components with hooks
const SessionCard: React.FC<SessionCardProps> = ({ session }) => {
  const [isLoading, setIsLoading] = useState(false);
  
  // ...
};

// Use proper TypeScript types
interface Session {
  id: string;
  title: string;
  scheduledAt: Date;
}

// Prefer named exports
export { SessionCard };
```

### File Organization

```
# Backend
app/
├── api/v1/        # API routes
├── core/          # Config, security
├── crud/          # Database operations
├── models/        # SQLAlchemy models
└── schemas/       # Pydantic schemas

# Mobile
src/
├── api/           # API client
├── components/    # Reusable components
├── hooks/         # Custom hooks
├── navigation/    # Navigation config
├── screens/       # Screen components
└── store/         # State management
```

---

## Testing

### Backend Tests

```bash
# Run all tests
docker compose exec api pytest tests/ -v

# Run specific test file
docker compose exec api pytest tests/test_sessions.py -v

# Run with coverage
docker compose exec api pytest tests/ --cov=app --cov-report=html

# Run specific test
docker compose exec api pytest tests/test_auth.py::test_login -v
```

### Writing Tests

```python
# tests/test_sessions.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_create_session(async_client, mock_user, mock_gym):
    """Test creating a workout session."""
    with patch("app.crud.session.create_session") as mock_create:
        mock_create.return_value = mock_session
        
        response = await async_client.post(
            "/api/v1/sessions",
            json={
                "title": "Leg Day",
                "gym_id": str(mock_gym.id),
                "scheduled_at": "2026-01-16T06:00:00Z"
            }
        )
        
        assert response.status_code == 201
        assert response.json()["title"] == "Leg Day"
```

### Test Coverage

We aim for >90% test coverage. Check coverage report:

```bash
docker compose exec api pytest tests/ --cov=app --cov-report=term-missing
```

---

## Questions?

- Open a [Discussion](https://github.com/ahmedul/GymBuddy/discussions)
- Check existing issues and PRs
- Join our community chat

---

Thank you for contributing! 💪

<p align="center">
  <a href="README.md">← Back to README</a>
</p>

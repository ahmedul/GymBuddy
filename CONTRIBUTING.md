# Contributing to GymBuddy

Thank you for your interest in contributing to GymBuddy! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. Be kind, constructive, and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- Git

### Local Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/GymBuddy.git
   cd GymBuddy
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the mobile app**
   ```bash
   cd mobile
   npm install
   ```

4. **Start services with Docker**
   ```bash
   docker compose up -d
   ```

## Development Workflow

### Branch Naming

- `feature/` - New features (e.g., `feature/group-workouts`)
- `fix/` - Bug fixes (e.g., `fix/login-validation`)
- `docs/` - Documentation updates (e.g., `docs/api-reference`)
- `refactor/` - Code refactoring (e.g., `refactor/auth-service`)

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(sessions): add recurring session support
fix(auth): resolve token refresh race condition
docs(api): update session endpoints documentation
```

## Pull Request Process

1. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make your changes** and commit with clear messages

3. **Run tests locally**
   ```bash
   # Backend tests
   cd backend && pytest tests/ -v

   # Mobile type check
   cd mobile && npx tsc --noEmit
   ```

4. **Push your branch**
   ```bash
   git push origin feature/your-feature
   ```

5. **Open a Pull Request** against `main` branch

6. **Address review feedback** and ensure CI passes

7. **Merge** once approved (squash merge preferred)

## Coding Standards

### Python (Backend)

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function signatures
- Maximum line length: 120 characters
- Use `ruff` for linting

```python
# Good
async def get_user_sessions(
    user_id: str,
    db: AsyncSession,
    limit: int = 10
) -> list[Session]:
    """Fetch sessions for a user."""
    ...

# Bad
async def get_sessions(id, db):
    ...
```

### TypeScript (Mobile)

- Use TypeScript strict mode
- Prefer functional components with hooks
- Use meaningful variable names
- Document complex logic with comments

```typescript
// Good
const handleSessionJoin = async (sessionId: string): Promise<void> => {
  try {
    await joinSession(sessionId);
    showSuccessToast('Joined session!');
  } catch (error) {
    showErrorToast('Failed to join session');
  }
};

// Bad
const join = async (id) => { ... }
```

### API Design

- Use RESTful conventions
- Version all endpoints (`/api/v1/...`)
- Return consistent response formats
- Document with OpenAPI/Swagger

## Testing Guidelines

### Backend Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

Test structure:
```python
class TestFeatureName:
    """Test group description."""
    
    def test_specific_scenario(self, fixture):
        """Test should describe expected behavior."""
        # Arrange
        ...
        # Act
        result = function_under_test()
        # Assert
        assert result == expected
```

### Mobile Tests

```bash
# Type checking
npx tsc --noEmit

# Run tests (when implemented)
npm test
```

## Project Structure

```
GymBuddy/
├── backend/           # FastAPI backend
│   ├── app/           # Application code
│   ├── tests/         # Pytest tests
│   └── alembic/       # Database migrations
├── mobile/            # React Native app
│   └── src/           # Source code
├── infra/             # AWS CDK infrastructure
└── docs/              # Documentation
```

## Questions?

- Open an [Issue](https://github.com/ahmedul/GymBuddy/issues) for bugs or features
- Start a [Discussion](https://github.com/ahmedul/GymBuddy/discussions) for questions

Thank you for contributing! 🏋️

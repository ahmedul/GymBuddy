# 🏃 GymBuddy Weekly Sprint Plan

> **Start Date:** January 18, 2026  
> **Goal:** Ship v1.1 with push notifications, email verification, and mobile polish

---

## 📅 Week 1: Jan 18-24 — Push Notifications Setup

| Day | Task | Time | Status |
|-----|------|------|--------|
| Sat 18 | Set up Expo Push Notifications service | 1-2h | ⬜ |
| Sun 19 | Create notification tokens table + API endpoint | 1h | ⬜ |
| Mon 20 | Backend: Send push on session invite | 1h | ⬜ |
| Tue 21 | Backend: Send push on friend request | 1h | ⬜ |
| Wed 22 | Mobile: Handle incoming notifications | 1h | ⬜ |
| Thu 23 | Mobile: Notification preferences screen | 1h | ⬜ |
| Fri 24 | Test end-to-end, fix bugs | 1h | ⬜ |

**Deliverable:** Push notifications working for invites & friend requests

---

## 📅 Week 2: Jan 25-31 — Email Verification & Password Reset

| Day | Task | Time | Status |
|-----|------|------|--------|
| Sat 25 | Set up email service (SendGrid/SES) | 1-2h | ⬜ |
| Sun 26 | Email templates: verification, password reset | 1h | ⬜ |
| Mon 27 | Backend: Email verification flow | 1h | ⬜ |
| Tue 28 | Backend: Password reset flow | 1h | ⬜ |
| Wed 29 | Mobile: Verification prompt screen | 1h | ⬜ |
| Thu 30 | Mobile: Forgot password screen | 1h | ⬜ |
| Fri 31 | Test flows, handle edge cases | 1h | ⬜ |

**Deliverable:** Users can verify email and reset password

---

## 📅 Week 3: Feb 1-7 — Mobile Polish & UX

| Day | Task | Time | Status |
|-----|------|------|--------|
| Sat 1 | Loading states & skeleton screens | 1h | ⬜ |
| Sun 2 | Error handling & retry logic | 1h | ⬜ |
| Mon 3 | Pull-to-refresh on all lists | 30m | ⬜ |
| Tue 4 | Empty states with illustrations | 1h | ⬜ |
| Wed 5 | Form validation feedback | 1h | ⬜ |
| Thu 6 | Haptic feedback & animations | 1h | ⬜ |
| Fri 7 | Test on iOS + Android | 1h | ⬜ |

**Deliverable:** Polished mobile app experience

---

## 📅 Week 4: Feb 8-14 — Recurring Sessions

| Day | Task | Time | Status |
|-----|------|------|--------|
| Sat 8 | Database: recurrence pattern schema | 1h | ⬜ |
| Sun 9 | Backend: Create recurring session API | 1-2h | ⬜ |
| Mon 10 | Backend: Generate session instances | 1h | ⬜ |
| Tue 11 | Backend: Edit single vs all occurrences | 1h | ⬜ |
| Wed 12 | Mobile: Recurrence picker UI | 1h | ⬜ |
| Thu 13 | Mobile: Display recurring indicator | 30m | ⬜ |
| Fri 14 | Test weekly/biweekly/monthly patterns | 1h | ⬜ |

**Deliverable:** Users can create recurring workout sessions

---

## 📅 Week 5: Feb 15-21 — Session Chat

| Day | Task | Time | Status |
|-----|------|------|--------|
| Sat 15 | Database: messages table schema | 1h | ⬜ |
| Sun 16 | Backend: Send/get messages API | 1h | ⬜ |
| Mon 17 | Backend: WebSocket setup for real-time | 2h | ⬜ |
| Tue 18 | Mobile: Chat UI component | 1-2h | ⬜ |
| Wed 19 | Mobile: Connect to WebSocket | 1h | ⬜ |
| Thu 20 | Mobile: Message notifications | 1h | ⬜ |
| Fri 21 | Test multi-user chat | 1h | ⬜ |

**Deliverable:** Participants can chat within a session

---

## 📅 Week 6: Feb 22-28 — Testing & v1.1 Release

| Day | Task | Time | Status |
|-----|------|------|--------|
| Sat 22 | Write integration tests for new features | 2h | ⬜ |
| Sun 23 | Fix any failing tests | 1h | ⬜ |
| Mon 24 | Update API documentation | 1h | ⬜ |
| Tue 25 | Update wiki & user guide | 1h | ⬜ |
| Wed 26 | Build production mobile app | 1h | ⬜ |
| Thu 27 | Deploy backend to AWS | 1h | ⬜ |
| Fri 28 | 🚀 **Release v1.1** | - | ⬜ |

**Deliverable:** v1.1 released to production!

---

## ✅ Completed Sprints

### Week 0: Jan 11-17 ✅
- [x] MVP backend complete
- [x] MVP mobile screens
- [x] GitHub repo setup
- [x] CI/CD pipelines
- [x] Pytest test suite (99 tests)
- [x] Wiki documentation
- [x] Postman collection

---

## 📝 Daily Routine

```
1. Check SPRINT.md for today's task
2. Create a feature branch
3. Implement the task
4. Write/update tests
5. Commit with clear message
6. Push and create PR (if ready)
7. Mark task ✅ in SPRINT.md
```

---

## 🎯 v1.1 Feature Summary

| Feature | Priority | Status |
|---------|----------|--------|
| Push Notifications | High | ⬜ Week 1 |
| Email Verification | High | ⬜ Week 2 |
| Password Reset | High | ⬜ Week 2 |
| Mobile Polish | Medium | ⬜ Week 3 |
| Recurring Sessions | Medium | ⬜ Week 4 |
| Session Chat | Medium | ⬜ Week 5 |

---

*Update this file daily as you complete tasks!*

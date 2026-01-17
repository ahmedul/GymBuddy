# 📋 GitHub Issues - Ready to Create

Go to: https://github.com/ahmedul/GymBuddy/issues/new

Copy each issue below and paste into GitHub.

---

## Week 1: Push Notifications (Jan 18-24)

### Issue 1.1
**Title:** `[Week 1] Set up Expo Push Notifications service`

**Body:**
```markdown
## 📋 Story
Set up the foundation for push notifications in the mobile app.

## ✅ Acceptance Criteria
- [ ] Install `expo-notifications` package
- [ ] Configure app.json with notification settings
- [ ] Request notification permissions on app launch
- [ ] Get and store Expo push token
- [ ] Test receiving a test notification

## 📁 Files to modify
- `mobile/package.json`
- `mobile/app.json`
- `mobile/App.tsx`
- `mobile/src/services/notifications.ts` (new)

## ⏱️ Estimate: 1-2 hours
## 📅 Due: Jan 18, 2026
```

---

### Issue 1.2
**Title:** `[Week 1] Backend: Notification tokens table & API`

**Body:**
```markdown
## 📋 Story
Create database table to store user push tokens and API endpoint to register them.

## ✅ Acceptance Criteria
- [ ] Create `notification_tokens` table migration
- [ ] Create NotificationToken model
- [ ] POST `/api/v1/notifications/token` - register token
- [ ] DELETE `/api/v1/notifications/token` - unregister token
- [ ] Associate tokens with user accounts

## 📁 Files to modify
- `backend/alembic/versions/002_notification_tokens.py` (new)
- `backend/app/models/notification.py` (new)
- `backend/app/api/v1/notifications.py` (new)
- `backend/app/schemas/notification.py` (new)

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 19, 2026
```

---

### Issue 1.3
**Title:** `[Week 1] Backend: Send push on session invite`

**Body:**
```markdown
## 📋 Story
When a user is invited to a session, send them a push notification.

## ✅ Acceptance Criteria
- [ ] Create notification service with Expo push API
- [ ] Trigger notification when session invite created
- [ ] Include session title and inviter name in notification
- [ ] Handle failed/invalid tokens gracefully

## 📁 Files to modify
- `backend/app/services/push.py` (new)
- `backend/app/api/v1/sessions.py` (modify invite endpoint)

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 20, 2026
```

---

### Issue 1.4
**Title:** `[Week 1] Backend: Send push on friend request`

**Body:**
```markdown
## 📋 Story
When a user receives a friend request, send them a push notification.

## ✅ Acceptance Criteria
- [ ] Trigger notification on friend request creation
- [ ] Include requester name in notification
- [ ] Don't send if user has disabled friend notifications

## 📁 Files to modify
- `backend/app/api/v1/social.py` (modify friend request endpoint)
- `backend/app/services/push.py`

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 21, 2026
```

---

### Issue 1.5
**Title:** `[Week 1] Mobile: Handle incoming notifications`

**Body:**
```markdown
## 📋 Story
Handle push notifications when the app is in foreground, background, or closed.

## ✅ Acceptance Criteria
- [ ] Show in-app notification when app is open
- [ ] Navigate to relevant screen when notification tapped
- [ ] Handle notification data payload
- [ ] Update UI when notification received (e.g., badge count)

## 📁 Files to modify
- `mobile/src/services/notifications.ts`
- `mobile/App.tsx`
- `mobile/src/navigation/RootNavigator.tsx`

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 22, 2026
```

---

### Issue 1.6
**Title:** `[Week 1] Mobile: Notification preferences screen`

**Body:**
```markdown
## 📋 Story
Allow users to enable/disable different types of notifications.

## ✅ Acceptance Criteria
- [ ] Create NotificationSettingsScreen
- [ ] Toggle for session invites
- [ ] Toggle for friend requests
- [ ] Toggle for session reminders
- [ ] Persist settings to backend

## 📁 Files to modify
- `mobile/src/screens/settings/NotificationSettingsScreen.tsx` (new)
- `mobile/src/navigation/MainNavigator.tsx`
- `backend/app/models/user.py` (add notification prefs)

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 23, 2026
```

---

### Issue 1.7
**Title:** `[Week 1] Test push notifications end-to-end`

**Body:**
```markdown
## 📋 Story
Test the complete notification flow and fix any bugs.

## ✅ Acceptance Criteria
- [ ] Test invite notification on physical device
- [ ] Test friend request notification
- [ ] Test notification tap navigation
- [ ] Test with app in background/closed
- [ ] Verify token cleanup on logout

## 📁 Files to modify
- Various bug fixes

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 24, 2026
```

---

## Week 2: Email Verification & Password Reset (Jan 25-31)

### Issue 2.1
**Title:** `[Week 2] Set up email service (SendGrid/SES)`

**Body:**
```markdown
## 📋 Story
Configure email sending service for transactional emails.

## ✅ Acceptance Criteria
- [ ] Choose email provider (SendGrid or AWS SES)
- [ ] Set up account and API keys
- [ ] Create email service in backend
- [ ] Test sending a simple email
- [ ] Add config to environment variables

## 📁 Files to modify
- `backend/app/services/email.py` (new)
- `backend/app/core/config.py`
- `backend/requirements.txt`

## ⏱️ Estimate: 1-2 hours
## 📅 Due: Jan 25, 2026
```

---

### Issue 2.2
**Title:** `[Week 2] Email templates: verification & password reset`

**Body:**
```markdown
## 📋 Story
Create HTML email templates for verification and password reset.

## ✅ Acceptance Criteria
- [ ] Create email verification template
- [ ] Create password reset template
- [ ] Include GymBuddy branding
- [ ] Mobile-responsive design
- [ ] Test email rendering

## 📁 Files to modify
- `backend/app/templates/email_verification.html` (new)
- `backend/app/templates/password_reset.html` (new)
- `backend/app/services/email.py`

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 26, 2026
```

---

### Issue 2.3
**Title:** `[Week 2] Backend: Email verification flow`

**Body:**
```markdown
## 📋 Story
Implement complete email verification flow.

## ✅ Acceptance Criteria
- [ ] Generate verification token on registration
- [ ] Send verification email
- [ ] GET `/api/v1/auth/verify/{token}` endpoint
- [ ] Mark user as verified
- [ ] Resend verification endpoint

## 📁 Files to modify
- `backend/app/api/v1/auth.py`
- `backend/app/models/user.py`
- `backend/app/services/email.py`

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 27, 2026
```

---

### Issue 2.4
**Title:** `[Week 2] Backend: Password reset flow`

**Body:**
```markdown
## 📋 Story
Implement complete password reset flow.

## ✅ Acceptance Criteria
- [ ] POST `/api/v1/auth/forgot-password` - send reset email
- [ ] POST `/api/v1/auth/reset-password` - reset with token
- [ ] Token expiration (1 hour)
- [ ] Invalidate token after use
- [ ] Rate limiting on forgot-password

## 📁 Files to modify
- `backend/app/api/v1/auth.py`
- `backend/app/models/user.py` (reset token field)
- `backend/app/services/email.py`

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 28, 2026
```

---

### Issue 2.5
**Title:** `[Week 2] Mobile: Verification prompt screen`

**Body:**
```markdown
## 📋 Story
Show verification prompt for unverified users.

## ✅ Acceptance Criteria
- [ ] Show banner for unverified users
- [ ] Verification pending screen
- [ ] Resend verification button
- [ ] Success confirmation

## 📁 Files to modify
- `mobile/src/screens/auth/VerifyEmailScreen.tsx` (new)
- `mobile/src/components/VerificationBanner.tsx` (new)

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 29, 2026
```

---

### Issue 2.6
**Title:** `[Week 2] Mobile: Forgot password screen`

**Body:**
```markdown
## 📋 Story
Create forgot password flow in mobile app.

## ✅ Acceptance Criteria
- [ ] ForgotPasswordScreen with email input
- [ ] ResetPasswordScreen with new password
- [ ] Success/error handling
- [ ] Link from login screen

## 📁 Files to modify
- `mobile/src/screens/auth/ForgotPasswordScreen.tsx` (new)
- `mobile/src/screens/auth/ResetPasswordScreen.tsx` (new)
- `mobile/src/screens/auth/LoginScreen.tsx`

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 30, 2026
```

---

### Issue 2.7
**Title:** `[Week 2] Test email flows end-to-end`

**Body:**
```markdown
## 📋 Story
Test complete email verification and password reset flows.

## ✅ Acceptance Criteria
- [ ] Test registration → verification email
- [ ] Test verification link
- [ ] Test forgot password flow
- [ ] Test password reset
- [ ] Test expired token handling

## 📁 Files to modify
- Bug fixes as needed

## ⏱️ Estimate: 1 hour
## 📅 Due: Jan 31, 2026
```

---

## Quick Create Commands

If your GitHub CLI gets updated, you can use these commands:

```bash
# Week 1
gh issue create -t "[Week 1] Set up Expo Push Notifications" -l "week-1" -b "..."
gh issue create -t "[Week 1] Backend: Notification tokens API" -l "week-1" -b "..."

# etc.
```

---

## Project Board Setup

1. Go to: https://github.com/ahmedul/GymBuddy/projects
2. Click "New project"
3. Choose "Board" template
4. Name it "GymBuddy v1.1 Sprint"
5. Create columns: `Backlog`, `This Week`, `In Progress`, `Done`
6. Add all issues to the board

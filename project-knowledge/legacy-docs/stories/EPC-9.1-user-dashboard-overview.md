# User Story DA.1: User Dashboard Overview

**Epic:** Dashboard & Analytics  
**Story ID:** DA.1  
**Priority:** High  
**Status:** Draft  
**Owner:** Product Owner (PO)

---

## Description

As a **registered user**,  
I want to **see a comprehensive overview of my profile status and recent activities**,  
So that **I can quickly understand my progress and access key platform features**.

---

## Acceptance Criteria

1. Dashboard header includes:
   - User's name and profile picture/avatar
   - Current gamification points and level
   - Quick access to settings and logout
   - Notification indicator with count

2. Profile completion section:
   - Visual progress bar showing completion percentage
   - List of incomplete profile sections with quick links
   - Profile approval status indicator
   - Last profile update timestamp
   - "Complete Profile" call-to-action button

3. Recent activity summary:
   - Last 5-10 activities (job logs, profile updates, fit scores)
   - Activity timestamps and descriptions
   - Quick links to related content
   - "View All Activity" link

4. Quick access widgets:
   - "Log New Job" button
   - "Generate Resume" button
   - "View Fit Scores" button
   - "Update Profile" button
   - "View Artifacts" button

5. Gamification display:
   - Current points and level
   - Recent achievements and badges
   - Progress toward next level
   - Points earned this week/month
   - "View All Achievements" link

6. AI usage and token tracking:
   - Total AI services used (resumes, fit scores, messages)
   - Token consumption breakdown by feature
   - Profile creation token usage
   - AI usage this week/month
   - Remaining quota/limits (if applicable)
   - "View Detailed AI Usage" link

7. Upcoming tasks and reminders:
   - Profile completion reminders
   - Job application follow-ups
   - Skill gap resolution suggestions
   - Weekly progress check-ins
   - Custom user-set reminders

8. Dashboard layout:
   - Responsive design for all devices
   - Collapsible sections for customization
   - Real-time data updates
   - Loading states for data fetching
   - Error handling for failed data loads

---

## Definition of Done

- Dashboard loads within 3 seconds with all data
- All widgets display accurate, real-time information
- Quick access buttons work correctly
- Profile completion status is accurate
- Gamification data is properly integrated
- AI usage and token tracking is accurate and up-to-date
- Dashboard is fully responsive
- Error states are handled gracefully
- Integration with all core features is complete

---

## Dependencies

- Authentication system (Epic 7)
- Profile intake flow (Epic 1)
- Job discovery and logging system
- Gamification engine
- AI usage tracking system
- Token consumption monitoring
- Notification system
- Data aggregation service 
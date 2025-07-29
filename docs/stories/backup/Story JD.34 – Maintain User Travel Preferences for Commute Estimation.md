### User Story JD.34 – Maintain User Travel Preferences for Commute Estimation

**As a** user  
**I want** the system to remember and use my preferred method of travel  
**So that** commute time estimates for job locations are accurate and meaningful to me

---

**Description:**  
Commute duration can vary significantly depending on whether the user travels by car, public transport, or another method. To provide relevant commute time insights, the platform must maintain a travel preference per user profile. This preference should be used by default in job commute estimates but allow for override during job logging or browsing.

---

**Acceptance Criteria:**
- [ ] User profile includes a `preferred_commute_mode` setting (e.g., car, public transport)
- [ ] Commute time estimation uses this setting as default
- [ ] Users can override commute mode per job log
- [ ] Override does not affect global profile setting
- [ ] Commute estimates displayed in the job summary view reflect selected mode
- [ ] Commute estimation modules support location-to-location time queries based on selected mode
- [ ] If no preference is set, system uses a default (e.g., car) and prompts user to set their mode

---

**Dependencies:**
- Profile schema update to include commute preferences
- Commute time estimation service with support for multiple transport modes
- UI controls for commute mode selection and override

---

**Priority:** Medium  
**Tags:** location-awareness, commute-estimation, user-preferences, profile-enhancement

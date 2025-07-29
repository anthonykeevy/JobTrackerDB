### User Story JD.28 – Respect Travel Mode Preferences in Commute Estimates

**As a** job seeker  
**I want** the system to calculate commute times using my preferred method of travel  
**So that** commute estimates are relevant and aligned with how I travel

---

**Description:**  
Commute time is only useful if it reflects a realistic scenario. This story ensures users can define how they travel (e.g., car, public transport, cycling), and that the system uses this preference to calculate commute time from their location to the job location.

---

**Acceptance Criteria:**
- [ ] Users can set a default commute mode in their profile (e.g., driving, public transport, walking)
- [ ] System stores travel mode preference and updates estimates accordingly
- [ ] When estimating commute time, the system uses the chosen mode of transport
- [ ] Commute method and estimate are shown in the job log view
- [ ] Users can override the commute mode per job if desired
- [ ] Commute service API supports multi-mode routing options

---

**Dependencies:**
- User profile settings
- Routing service capable of multi-modal commute time estimation
- Commute metadata fields in job record
- Job detail UI update for commute method display and override

---

**Priority:** Medium  
**Tags:** commute-mode, user-preference, location-aware, job-relevance, UX

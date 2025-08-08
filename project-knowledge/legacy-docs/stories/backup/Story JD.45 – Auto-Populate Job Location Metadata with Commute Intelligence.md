### User Story JD.45 – Auto-Populate Job Location Metadata with Commute Intelligence

**Epic:** Job Discovery and Logging for Profile Matching  
**Priority:** Medium  
**Status:** Ready for Dev  
**Type:** Feature  

**Story:**  
As a system,  
I want to automatically populate job location details and compute estimated commute time using user preferences,  
So that users can quickly understand feasibility and time commitment involved with applying to a job.

---

**Acceptance Criteria:**
- [ ] Extract job location(s) from the job description and/or structured metadata from job boards.
- [ ] Use the user’s home address or selected commuting base to calculate estimated commute time.
- [ ] Use preferred travel mode (car, public transport) for route and duration estimation.
- [ ] Display commute estimate (e.g., “Approx. 35 min by train”) next to job listing and in the job details view.
- [ ] Allow users to edit or override detected location or travel preferences.
- [ ] Track how location awareness influences fit score or job interest.
- [ ] Log metadata quality for commute estimations to improve accuracy over time.

---

**Dependencies:**
- Job data parser
- User commute preference schema
- Mapping and travel time estimation API (e.g., Google Maps, OpenRouteService)
- Job display and filtering logic integration

---

**Tags:** job-location, commute-estimation, user-preferences, job-discovery, travel-mode

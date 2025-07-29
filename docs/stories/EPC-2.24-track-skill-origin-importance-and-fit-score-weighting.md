### User Story JD.24 – Track Skill Origin, Importance, and Fit Score Weighting

**As a** system  
**I want** to track which text fragments in the job description led to specific skill inferences  
**So that** I can explain fit score results clearly and version job descriptions accurately

---

**Description:**  
This story enables skill-level traceability during job analysis. Each inferred skill should link back to the exact section of the job description that prompted it. Additionally, AI should classify skills by priority (e.g., required, preferred, optional), and these levels influence the weighting during fit scoring. This will ensure future edits or alternate versions of the job can be detected and scored accurately.

---

**Acceptance Criteria:**
- [ ] Each extracted skill includes a reference to the source sentence or paragraph in the job description
- [ ] Skills are labeled with importance tiers: Required, Preferred, Optional
- [ ] Required skills contribute more weight to the fit score than lower-tiered skills
- [ ] A job version change is triggered when skill text or tiering changes materially
- [ ] Skill traceability is viewable by users reviewing their fit score explanation
- [ ] Users can suggest corrections if a skill was inferred from incorrect context

---

**Dependencies:**
- AI/NLP pipeline for skill extraction and contextual traceability
- Skill-tier scoring logic in the Fit Score engine
- JobVersion comparison logic based on skill source changes
- UI interface to display matched skills and source text

---

**Priority:** High  
**Tags:** skill-inference, fit-score-weighting, traceability, job-versioning, AI-transparency

# JobTrackerDB

# 1. Introduction

This Architecture Vision outlines the strategic direction for an AI-Powered Resume and Job Tracker Platform, designed to streamline job applications for job seekers, enhance recruitment efficiency, and provide operational value through tracking employee skills and contributions. The platform leverages AI to offer personalized resume optimization, job matching, application tracking, and internal talent discovery, integrating gamification into frontend and backend systems. This document aligns with TOGAF’s ADM Phase A to establish a clear stakeholder vision and guide subsequent architecture development.

# 2. Scope

The platform serves:

* **Job Seekers**: Individuals from entry-level to executive roles.
* **Employers/Recruiters**: Organizations seeking efficient candidate sourcing.
* **Companies (Operational Use)**: Organizations aiming for better staff understanding through profile updates.
* **Geographic Scope**: Initially Australia; global scope in future phases.
* **Functional Scope**: Resume creation, AI-driven optimization, job matching, application tracking, and analytics. Internal talent management deferred post-MVP.
* **Exclusions**: No direct job placement services or staffing agency functions.

# 3. Stakeholders and Concerns

* **Job Seekers**: Competitive resumes, job tracking, gamified engagement.
* **Employers/Recruiters**: Efficient AI-driven candidate matching.
* **Companies (Operational Teams)**: Accurate employee profiles, future internal staffing.
* **Platform Developer (You)**: Robust, scalable, secure platform managed through extended hours, local MVP hosting, and eventual cloud migration.
* **Future Investors**: Market viability, subscriber growth, continuous usage.

# 4. Business Goals and Drivers

* **Enhance User Experience**: AI-driven interface with gamified engagement.
* **Improve Hiring Efficiency**: Faster candidate screening.
* **Market Differentiation**: Comprehensive automated resume optimization and predictive job matching.
* **Scalability and Compliance**: Global scalability post-MVP, compliance starting with Australia.
* **Revenue Generation**: \$10/month subscription; target 1000 subscribers within 3 months post-release.

**Business Drivers**: Growing demand for AI tools, automation needs, privacy, and ethical AI considerations.

# 5. Architecture Principles

* **User-Centric Design**: Start with user journeys, intuitive interfaces.
* **Hybrid Monolithic-Microservices**: Central monolithic platform with supporting microservices.
* **Custom MCP Interface**: A dedicated internal MCP service will act as a structured interface between the application and the SQL database. This service will handle all database logic, logging, validation, and permission control, and will be designed to support future clients like mobile apps or internal analytics tools.
* **Developer Experience**: Early CI/CD via GitHub Actions.
* **Security and Privacy**: Australian compliance initially, baseline global standards.
* **Interoperability**: Robust third-party API integration with manual contingency fallback.
* **AI Ethics**: Transparent, unbiased algorithms, user-driven artifact approval with usefulness scoring.
* **Gamification**: Engagement metrics and progress tracking.
* **Cost-Conscious Engineering**: Initial local hosting; Azure migration planned post-MVP.
* **Evolutionary Design**: Flexible architecture for future scalability.

# 6. Vision Statement

The platform revolutionizes career advancement and organizational talent management, initially in Australia, leveraging NLP, ML, and gamification to deliver personalized, secure, scalable services. Localization strategies align with Australia initially, scaling globally post-MVP.

# 7. Value Proposition

* **Job Seekers**: AI-driven profile creation and job application tracking.
* **Employers**: AI-powered screening (post-MVP).
* **Companies**: Operational analytics (post-MVP).
* **Business**: Subscription-based revenue, clear user metrics and KPIs (e.g., Monthly Active Users).

# 8. Constraints and Assumptions

**Constraints**:

* Solo developer, 3-month MVP timeline.
* Initial budget constraints, local MVP hosting.
* International data privacy compliance starting with Australia.
* Reliance on third-party API robustness with manual contingency.

**Assumptions**:

* Stable internet post-MVP.
* Market demand for AI tools.
* OpenAI APIs for NLP and ML; no self-training initially.

# 9. High-Level Architecture Model

* Frontend, backend, structured SQL database (`JobTrackerDB`).
* Custom MCP service providing a robust, centralized API interface to `JobTrackerDB`.
* OpenAI API integrations with detailed logging of user and token costs.
* Gamification elements integrated with usage tracking.
* Backup and recovery strategy in place, including local database backups and planned Azure backups.

# 10. Risks and Mitigation

* **Solo Developer Overwhelm**: Defined thresholds for external assistance.
* **AI Bias**: User feedback mechanisms for continuous improvement.
* **Data Privacy**: Encryption and compliance from MVP onwards.
* **Scalability**: Defined triggers for Azure migration based on usage.

# 11. Local Development Setup (For Cursor & BMAD Agents)

## Tech Stack

* **Frontend**: React.js + Tailwind CSS
* **Backend**: FastAPI (Python 3.10+)
* **Database**: SQL Server (local setup with structured schema)
* **Custom MCP Service**: Internal Python-based REST API layer to mediate all DB operations
* **CI/CD**: GitHub Actions
* **Environment Management**: `.env` files for credentials, local and staging config

## Folder Structure

```
project-root/
├── frontend/
│   ├── src/
│   ├── public/
│   └── ...
├── backend/
│   ├── app/
│   │   ├── api/  (FastAPI routes)
│   │   ├── core/ (config, auth)
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── mcp/  (Custom MCP service for SQL DB)
│   │   ├── endpoints/
│   │   ├── db/
│   │   └── logging.py
│   ├── tests/
│   └── requirements.txt
├── database/
│   └── init.sql
├── .env
└── docker-compose.yml (optional)
```

## Local Environment Setup

1. **Clone the repo and create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Run local SQL Server** (via Docker or local installation)
3. **Set up `.env` with local DB creds and OpenAI keys**
4. **Start FastAPI app with MCP routing enabled**

```bash
uvicorn backend.app.main:app --reload
```

5. **Frontend (in `frontend/`)**

```bash
npm install
npm run dev
```

---

## Notes on Adjustments

* **Subscriber Goals**: Added explicit subscriber target (1000 within 3 months).
* **AI Usefulness Score**: Included user approval and usefulness tracking of AI-generated artifacts.
* **Backup Strategy**: Detailed local backup processes and planned Azure database backups.
* **CI/CD Tools**: Early GitHub Actions implementation clarified.
* **Scope Clarifications**: Explicitly documented MVP features and future-phase deferrals.
* **Local Compliance**: Focused MVP localization specifically on Australia.
* **Third-party Reliability**: Documented contingency strategy for API failure.
* **AI Integration**: Defined OpenAI API logging and user-cost tracking.
* **Hybrid Architecture**: Confirmed hybrid monolithic-microservices architecture approach.
* **Custom MCP Interface**: Added a new principle and model element introducing a dedicated MCP service layer to manage all SQL database interactions for scalability, separation of concerns, and multi-client support.
* **Development Environment Setup**: Added section with tech stack, folder structure, and setup steps tailored for use in Cursor and BMAD development.

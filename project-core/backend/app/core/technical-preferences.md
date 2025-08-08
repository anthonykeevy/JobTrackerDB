# Technical Preferences for JobTrackerDB

## 1. Languages & Frameworks
- **Backend:** Python (FastAPI)
  - FastAPI acts only as an API layer, responding to frontend requests.
  - All backend-to-database communication is handled via the MCP (Middleware/Controller/Processor) layer.
  - **Authentication:** FastAPI must support OAuth 2.0/OpenID Connect flows for Google, Microsoft, Facebook, and Apple. The backend handles the OAuth handshake and token validation, then delegates user/session management to SQL stored procedures.
- **Frontend:** React with Tailwind CSS
  - **State Management:** Recommended: Zustand or Redux Toolkit for scalable state management.
- **All development should use Python where possible.**

## 2. Database & Storage
- **Database:** Microsoft SQL Server 2022 (MSSQL 2022)
  - All data logic (queries, business logic, CRUD) must be handled in the database via views and stored procedures.
  - **Naming conventions for SQL are a strict requirement:**
    - **Database Name:** `JobTrackerDB`
    - **Schema:** Default `dbo`
    - **Table Names:** Use singular names (e.g., `Profile`, `User`, `Resume`)
    - **Primary Keys:** Use an auto-incrementing ID field named [TableName]ID (e.g., ProfileID, UserID)
    - **Foreign Keys:** Named after the primary key they reference (e.g., ProfileID in child tables)
    - **Views:** Prefix with `v_` (e.g., v_ProfileSummary)
    - **Stored Procedures:** Prefix with `s_` (e.g., s_GetUserDetails)
    - **String Fields:** Use `nvarchar` type to support Unicode characters
    - **Related Tables:** Use hierarchical naming (e.g., ProfileSkill, JobApplicationAttachment)
  - **All CRUD and business logic must be implemented in stored procedures and views.**
  - **All sensitive operations must go through stored procedures.**
  - **User Table Schema Recommendation for OAuth Providers:**
    - Add fields to the `User` table:
      - `Provider` (nvarchar): e.g., 'google', 'microsoft', 'facebook', 'apple', or 'local'
      - `ProviderUserID` (nvarchar): Unique user ID from the provider
      - `Email` (nvarchar): User's email address
      - `Name` (nvarchar): User's display name
      - `LastLogin` (datetime): Last login timestamp
    - Update stored procedures to handle login/registration via external providers.

## 3. Project Structure & Documentation
- **Folder Structure:** Hierarchical, mirroring database and logical app structure.
- **Code Documentation:** Every function/class/module must include:
  - Purpose
  - Expected outcomes
  - Example input/output (if possible)
- **Documentation:** Both in-code comments and separate markdown files for major modules/components.
- **Auto-generated API docs** (e.g., Swagger/OpenAPI for FastAPI).

## 4. Internationalization & Localization
- **Dates:** Always use international format (ISO 8601, e.g., YYYY-MM-DD).
- **User Location:** App should auto-detect user location, but always confirm with the user. All date/time data stored in UTC in the database, converted for display in user’s timezone.

## 5. Authentication & Security
- **Authentication:** OAuth 2.0/OpenID Connect (Google, Microsoft, Facebook, Apple, and local accounts).
- **Auth handled by the database via stored procedures.**
- **Authorization:** Also handled in the database.
- **All sensitive operations must go through stored procedures.**
- **Backend must validate OAuth tokens with the provider before passing user info to the database.**

## 6. DevOps & CI/CD
- **Version Control:** Git (GitHub).
- **CI/CD:** Automated, using GitHub Actions.
- **Database migrations/deployments automated as part of CI/CD.**

## 7. Testing & Quality
- **Test Coverage:** 100% required.
- **Testing:** Both backend and frontend must be tested.
- **Test frameworks:**
  - **Backend:** Pytest (Python)
  - **Frontend:** Jest + React Testing Library
  - **End-to-End:** Cypress (recommended)

## 8. Frontend-Backend Communication
- **Frontend:** React app communicates only with FastAPI backend.
- **Backend:** FastAPI communicates with the database only via the MCP layer, which in turn calls SQL views and stored procedures.

## 9. Other
- **You are an experienced SQL developer, not a generalist developer.**
- **All SQL naming conventions are strict requirements.**
- **Other conventions (Python, JS, etc.) should follow best practices and be well documented for guidance.**

---

### Open Areas & Best-Practice Recommendations
- **React State Management:** Zustand (simple, scalable) or Redux Toolkit (for complex state needs).
- **Testing:** Aim for 100% coverage; use CI to enforce.
- **Documentation:** Use docstrings in Python, JSDoc in JS, and markdown files for high-level docs.
- **CI/CD:** Use GitHub Actions for automated testing, linting, and deployment. Automate database migrations with tools like Flyway or custom scripts.
- **Security:** Always validate and sanitize inputs at the database level. Use parameterized queries in stored procedures.
- **Timezone Handling:** Store all times in UTC; convert to user’s timezone for display using frontend logic.
- **OAuth Providers:** Start with Google, Microsoft, Facebook, and Apple. Add others as needed. Use a modular approach in FastAPI to allow easy addition of new providers.

---

**This document is the single source of truth for all technical preferences and must be referenced for all future architecture and development work.** 
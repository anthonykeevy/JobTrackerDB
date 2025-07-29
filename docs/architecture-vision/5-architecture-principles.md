# 5. Architecture Principles

TUser-Centric Design: Start with user journeys, intuitive interfaces.

Hybrid Monolithic-Microservices: Central monolithic platform with supporting microservices.

Custom MCP Interface: A dedicated internal MCP service will act as a structured interface between the application and the SQL database. This service will handle all database logic, logging, validation, and permission control, and will be designed to support future clients like mobile apps or internal analytics tools.

Developer Experience: Early CI/CD via GitHub Actions.

Security and Privacy: Australian compliance initially, baseline global standards.

Interoperability: Robust third-party API integration with manual contingency fallback.

AI Ethics: Transparent, unbiased algorithms, user-driven artifact approval with usefulness scoring.

Gamification: Engagement metrics and progress tracking.

Cost-Conscious Engineering: Initial local hosting; Azure migration planned post-MVP.

Evolutionary Design: Flexible architecture for future scalability.

- **Naming Convention**: Adopt a consistent naming standard for database objects. The main database is `JobTrackerDB`, with all tables residing in the default `dbo` schema using singular names (e.g., `Profile`, `User`) to enhance discoverability for developers. Use hierarchical naming for related tables (e.g., `ProfileSkill` for skills tied to a profile, `JobApplication` for job applications) to reflect relationships. Each table must include an auto-incrementing `ID` field named `[TableName]ID` (e.g., `ProfileID` for `Profile`, `ProfileSkillID` for `ProfileSkill`) to serve as the primary key and facilitate foreign key identification. Prefix views with `v_` (e.g., `v_ProfileSummary`) and stored procedures with `s_` (e.g., `s_GetUserDetails`) to distinguish object types. Use `nvarchar` for string fields to support Unicode characters for global compatibility. Example: `Profile` stores user profiles with a `ProfileID`, `ProfileSkill` links skills to a profile using `ProfileID` as a foreign key, and `v_ProfileSummary` provides a view of profile data.
    

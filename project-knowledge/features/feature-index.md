# JobTrackerDB Feature Index

## Features by Epic

### Epic 1: Career Profile Intake
- **EPC-1.1**: Resume Upload Validation → [affects: AI parsing, file storage, profile creation]
- **EPC-1.2**: Basic Information Collection → [affects: profile schema, validation]
- **EPC-1.15**: Address Validation Backend Integration → [affects: mapping, database schema, API integration]

### Epic 2: Job Discovery & Logging
- **EPC-2.1**: Job Search Integration → [affects: external APIs, data storage]
- **EPC-2.2**: Job Application Tracking → [affects: profile relationships, status management]

### Epic 3: AI-Powered Analysis
- **EPC-3.1**: Resume Parsing → [affects: OpenAI integration, data extraction]
- **EPC-3.2**: Fit Score Analysis → [affects: AI algorithms, job matching]

## Feature Dependencies

### Dependency Chain
```
Database Schema → Profile Builder → Address Validation → Resume Upload → AI Parsing
              ↓                ↓                    ↓             ↓
         User Management → Authentication → Job Tracking → Fit Scoring
```

### Critical Path Features
1. **Database Schema** - Foundation for all data operations
2. **Authentication** - Required for all user features  
3. **Profile Builder** - Core user onboarding flow
4. **Address Validation** - Critical for profile completion

## Technology Stack by Feature

### React Components
- **Profile Builder**: Multi-step form with validation
- **Dashboard**: Main user interface
- **Map Component**: Address visualization

### FastAPI Endpoints
- **Resume Upload**: File processing and AI parsing
- **Address Validation**: Geoscape API integration
- **Profile Management**: CRUD operations

### Database Tables
- **Profile**: Core user profile data
- **ProfileAddress**: Address with geolocation
- **ProfileVersion**: Version control for profiles
- **APIUsageTracking**: Billing and quota management

### External APIs
- **Geoscape**: Australian address validation
- **OpenAI**: Resume parsing and analysis
- **SmartyStreets**: US address validation (backup)

## Cross-Cutting Concerns

### Authentication & Authorization
- **Affects**: All user-facing features
- **Implementation**: JWT-based authentication
- **Database**: User, UserEmailAddress tables

### Error Handling
- **Affects**: All API endpoints
- **Implementation**: FastAPI exception handlers
- **Frontend**: Error boundary components

### Logging & Monitoring
- **Affects**: All backend operations
- **Implementation**: Python logging + API call tracking
- **Storage**: project-artifacts/logs/

### Data Validation
- **Affects**: All input forms and API endpoints
- **Implementation**: Zod (frontend) + Pydantic (backend)
- **Standards**: International date formats, timezone handling

## Current Status

### Completed Features ✅
- Database migration system (Alembic)
- Complete schema design (31+ tables) 
- Frontend profile builder (9 steps)
- Address validation frontend integration
- Map visualization
- Form validation system
- Responsive design
- API configuration

### In Progress 🔄
- Address validation backend integration
- Resume parsing AI implementation
- Cross-feature testing

### Planned ⏳
- Job tracking features
- Fit score analysis
- Billing system integration
- User authentication
- AI-powered resume optimization

## Feature Relationships Map

### Data Flow
```
User Input → Form Validation → API Endpoint → Database → Response
     ↓              ↓              ↓            ↓          ↓
  UI State → Error Handling → Logging → Audit Trail → User Feedback
```

### Component Dependencies
```
LoginScreen → Dashboard → ProfileBuilder → ReviewStep
     ↓           ↓            ↓             ↓
  useAuth → ProtectedRoute → Form Steps → API Calls
```

## Implementation Patterns

### Naming Conventions
- **Tables**: Hierarchical naming (ProfileAddress, UserEmailAddress)
- **Components**: PascalCase with descriptive names
- **API Endpoints**: RESTful with clear resource naming
- **Files**: kebab-case for multi-word files

### Code Organization
- **Backend**: Feature-based modules in app/api/
- **Frontend**: Component-based with shared utilities
- **Tests**: Mirror source structure with clear naming

## Future Considerations

### Scalability
- Database partitioning for large user bases
- API rate limiting and caching
- Frontend code splitting and lazy loading

### Technology Evolution
- Migration path for new frameworks
- API versioning strategy
- Database schema evolution

### Team Collaboration
- Feature branch strategy
- Code review processes
- Documentation maintenance

---

**Last Updated**: {Current Date}
**Maintained By**: Project team
**Next Review**: {Review Schedule}

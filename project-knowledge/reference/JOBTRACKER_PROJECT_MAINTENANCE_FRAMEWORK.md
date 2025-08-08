# JobTrackerDB Project Maintenance Framework

## Overview

This framework provides a structured approach to managing the JobTrackerDB project that optimizes for:
- Feature-driven development with traceability
- Cursor IDE + BMAD Method integration
- Clean separation of work phases and artifacts
- Cross-feature relationship tracking
- End-of-task cleanup and integration processes

## Framework Principles

### 1. **Feature-Centric Organization**
- Each feature/functionality maintains its own workspace during development
- Clear separation between active work, completed work, and reference materials
- Cross-feature relationships explicitly documented and indexed

### 2. **Workflow Integration**
- Process supports both concurrent development sessions and single-session focus
- BMAD Method tasks and Cursor semantic search work harmoniously
- Future tool integration accommodated through extensible structure

### 3. **Lifecycle Management**
- Clear phases: Planning → Development → Testing → Integration → Cleanup
- Artifacts preserved for future reference but organized by relevance
- Automated and manual organization options

## Directory Structure Framework

```
JobTrackerDB/
├── 📁 active-work/                    # Current development workspace
│   ├── feature-{name}/                # Individual feature workspaces
│   │   ├── planning/                  # BMAD tasks, user stories, analysis
│   │   ├── development/               # Work-in-progress code, tests, scripts
│   │   ├── testing/                   # Test files, results, debugging
│   │   ├── integration/               # Cross-feature impact analysis
│   │   └── feature-manifest.md       # Feature metadata and relationships
│   └── shared-workspace/              # Multi-feature development
│
├── 📁 project-core/                   # Production codebase
│   ├── backend/                       # Clean production backend
│   │   ├── app/                       # Application code
│   │   ├── migrations/                # Database migrations
│   │   ├── tests/                     # Unit and integration tests
│   │   └── config/                    # Configuration files
│   ├── frontend/                      # Clean production frontend
│   ├── scripts/                       # Production scripts only
│   └── docker/                        # Container configurations
│
├── 📁 project-knowledge/              # Documentation and reference
│   ├── architecture/                  # High-level design docs
│   ├── features/                      # Completed feature documentation
│   │   ├── {feature-name}/            # Individual feature docs
│   │   │   ├── implementation.md      # How it was built
│   │   │   ├── decisions.md           # Key decisions made
│   │   │   ├── testing-approach.md    # Testing strategy used
│   │   │   ├── cross-references.md    # Related features/impacts
│   │   │   └── artifacts/             # Supporting files
│   │   └── feature-index.md           # Cross-feature relationship map
│   ├── technical-specs/               # Technical documentation
│   ├── user-research/                 # User stories, requirements
│   └── reference/                     # External docs, guides
│
├── 📁 project-artifacts/              # Generated and temporary files
│   ├── test-results/                  # Test outputs by date
│   │   └── {YYYY-MM-DD}/              # Daily test result folders
│   ├── ai-baselines/                  # AI model test results
│   ├── performance-data/              # Performance benchmarks
│   ├── logs/                          # Application logs
│   │   ├── development/               # Dev environment logs
│   │   ├── testing/                   # Test execution logs
│   │   └── archived/                  # Older logs (auto-rotated)
│   └── exports/                       # Data exports, reports
│
├── 📁 development-tools/              # Development utilities
│   ├── scripts/                       # Development scripts
│   │   ├── service-management/        # Start/stop/status scripts
│   │   ├── database/                  # DB utilities
│   │   ├── testing/                   # Test automation
│   │   └── cleanup/                   # Cleanup automation
│   ├── templates/                     # Code and doc templates
│   ├── workflows/                     # BMAD workflows and checklists
│   └── cursor-config/                 # Cursor-specific configurations
│
├── 📁 external-integrations/          # Third-party integrations
│   ├── apis/                          # API configurations and tests
│   ├── databases/                     # Database schemas and seeds
│   └── services/                      # External service configs
│
└── 📁 project-meta/                   # Project management
    ├── planning/                      # Project planning docs
    ├── progress/                      # Progress tracking
    ├── reviews/                       # End-of-task reviews
    ├── maintenance/                   # Cleanup logs and schedules
    └── future-considerations/         # Technology roadmap
```

## Feature Development Workflow

### Phase 1: Feature Planning
```
1. Create new feature workspace: active-work/feature-{name}/
2. Generate feature-manifest.md with:
   - Feature description and scope
   - Related features/dependencies
   - Success criteria
   - Technology considerations
3. Use BMAD Method to create planning artifacts in planning/
4. Document cross-feature impacts in integration/
```

### Phase 2: Development
```
1. Work in development/ subdirectory
2. Create tests in testing/ subdirectory
3. Generate debugging artifacts as needed
4. Update feature-manifest.md with progress
5. Use Cursor semantic search across project-core/ for context
```

### Phase 3: Testing & Integration
```
1. Run comprehensive tests in testing/
2. Document cross-feature impacts in integration/
3. Update feature-index.md with relationships
4. Validate against related features
```

### Phase 4: Completion & Cleanup
```
1. Move production code to project-core/
2. Create feature documentation in project-knowledge/features/{name}/
3. Archive working files to project-artifacts/
4. Update cross-references and indices
5. Run cleanup scripts to remove temporary files
6. Review and consolidate related features
```

## File Naming Conventions

### Feature Files
- Feature workspace: `feature-{kebab-case-name}/`
- Feature manifest: `feature-manifest.md`
- Implementation docs: `{feature-name}-implementation.md`
- Cross-references: `{feature-name}-cross-references.md`

### Test Files
- Unit tests: `test_{module_name}.py` (backend), `{Component}.test.tsx` (frontend)
- Integration tests: `integration_{feature_name}.py`
- Test results: `test-results-{YYYY-MM-DD-HHMMSS}.{format}`

### Documentation
- Architecture docs: `arch-{topic}.md`
- Technical specs: `spec-{component}.md`
- User stories: `story-{epic}.{number}-{title}.md`
- Decision records: `decision-{YYYY-MM-DD}-{topic}.md`

### Scripts
- Service scripts: `{service}-{action}.ps1` (e.g., `backend-start.ps1`)
- Utility scripts: `util-{purpose}.py` (e.g., `util-db-seed.py`)
- Cleanup scripts: `cleanup-{scope}.ps1` (e.g., `cleanup-test-artifacts.ps1`)

## Cross-Feature Relationship Tracking

### Feature Index System
```markdown
# Feature Index (project-knowledge/features/feature-index.md)

## Features by Epic
- **Epic 1: Profile Builder**
  - EPC-1.1: Resume Upload → [affects: AI parsing, file storage]
  - EPC-1.2: Address Validation → [affects: mapping, database schema]
  
## Feature Dependencies
- Address Validation → Database Schema → Profile Builder
- AI Parsing → Resume Upload → Profile Builder

## Technology Stack by Feature
- React Components: Profile Builder, Dashboard
- FastAPI Endpoints: Resume Upload, Address Validation
- Database Tables: Profile, Address, Resume

## Cross-Cutting Concerns
- Authentication: [affects all user features]
- Error Handling: [affects all API features]
- Logging: [affects all backend features]
```

### Feature Manifest Template
```markdown
# Feature Manifest: {Feature Name}

## Overview
- **Epic**: {Epic Name}
- **Story ID**: {Story ID}
- **Priority**: {High/Medium/Low}
- **Status**: {Planning/Development/Testing/Complete}

## Scope
- {Brief description}
- {Key functionality}

## Dependencies
### Upstream Dependencies
- {Feature that must be complete first}

### Downstream Impacts
- {Features that will be affected by this}

## Technology Stack
- **Backend**: {FastAPI endpoints, database tables}
- **Frontend**: {React components, pages}
- **External**: {APIs, services}

## Cross-Feature Relationships
- **Data Dependencies**: {Shared data models}
- **API Dependencies**: {Shared endpoints}
- **UI Dependencies**: {Shared components}

## Success Criteria
- [ ] {Acceptance criteria 1}
- [ ] {Acceptance criteria 2}

## Implementation Notes
{Key decisions, approaches, gotchas}

## Testing Strategy
- **Unit Tests**: {Coverage approach}
- **Integration Tests**: {Cross-feature testing}
- **User Testing**: {Manual testing approach}

## Cleanup Checklist
- [ ] Production code moved to project-core/
- [ ] Documentation created in project-knowledge/
- [ ] Cross-references updated
- [ ] Temporary files archived
- [ ] Feature index updated
```

## BMAD Method Integration

### Task Workflows for Features
```
1. Use BMAD create-doc with feature templates
2. Store BMAD artifacts in active-work/{feature}/planning/
3. Reference BMAD tasks in feature-manifest.md
4. Use BMAD checklists for end-of-task cleanup
```

### Cursor Optimization
```
1. Semantic search optimized by keeping clean project-core/
2. Feature workspaces don't clutter main search results
3. Feature documentation structured for easy discovery
4. Cross-references enable relationship navigation
```

## Cleanup and Maintenance Processes

### End-of-Task Cleanup (Manual)
```
1. Run cleanup script: development-tools/scripts/cleanup/feature-cleanup.ps1
2. Validate feature documentation completeness
3. Update cross-references and indices
4. Archive working artifacts
5. Review and consolidate related features
```

### Weekly Maintenance (Semi-Automated)
```
1. Review active-work/ for stale features
2. Archive old test results and logs
3. Update feature index with new relationships
4. Clean up temporary files and caches
5. Review and update documentation links
```

### Monthly Review (Manual)
```
1. Comprehensive feature relationship review
2. Technology stack assessment
3. Documentation consolidation
4. Performance impact analysis
5. Future tool integration planning
```

## Tool Integration Guidelines

### Current Tools
- **Cursor**: Optimized semantic search on clean project-core/
- **BMAD Method**: Structured workflows in active-work/planning/
- **PowerShell**: Scripts organized in development-tools/scripts/
- **Git**: Clean commits from project-core/ only

### Future Tool Accommodation
```
1. Extensible directory structure
2. Configuration files in dedicated locations
3. Tool-specific artifacts in separate directories
4. API for accessing project metadata
5. Plugin architecture considerations
```

## Implementation Priority

### Phase 1: Core Structure (Week 1)
- [ ] Create main directory structure
- [ ] Move existing files to appropriate locations
- [ ] Create templates and initial documentation
- [ ] Set up basic cleanup scripts

### Phase 2: Workflow Integration (Week 2)
- [ ] Implement feature development workflow
- [ ] Create feature index system
- [ ] Integrate BMAD method workflows
- [ ] Test with current features

### Phase 3: Automation & Optimization (Week 3)
- [ ] Automated cleanup scripts
- [ ] Cursor configuration optimization
- [ ] Cross-reference automation
- [ ] Documentation generation tools

### Phase 4: Maintenance & Iteration (Ongoing)
- [ ] Weekly and monthly review processes
- [ ] Continuous improvement based on usage
- [ ] Future tool integration as needed
- [ ] Team collaboration preparation

## Benefits Summary

### Immediate Benefits
- Clean separation of work phases
- Better feature traceability
- Reduced clutter in main directories
- Improved Cursor semantic search

### Long-term Benefits
- Historical context preservation
- Cross-feature relationship clarity
- Scalable development process
- Future tool integration readiness
- Team collaboration preparation

### Maintenance Benefits
- Structured cleanup processes
- Automated artifact management
- Clear responsibility boundaries
- Reduced technical debt accumulation

---

**Next Steps**: Review this framework and let me know if you'd like me to help implement it, starting with the core directory structure and migration of existing files.

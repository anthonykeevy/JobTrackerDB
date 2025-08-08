# BMAD Method Feature Development Workflow

## Overview
This workflow integrates the BMAD Method with the JobTrackerDB project maintenance framework for feature development.

## Phase 1: Planning & Analysis

### 1.1 Feature Initiation
```powershell
# Start new feature workspace
.\development-tools\scripts\start-feature.ps1 -FeatureName "address-validation" -Epic "EPC-1" -StoryId "EPC-1.15"
```

### 1.2 BMAD Planning Tasks
Use BMAD Method in the planning/ directory:

**BMAD Commands to use:**
- `@bmad-master *task create-doc {feature-spec}` → Save to planning/
- `@bmad-master *execute-checklist {story-draft-checklist}` → Review requirements
- `@bmad-master *task advanced-elicitation` → If requirements unclear

**Planning Artifacts to Create:**
- `planning/requirements.md` - Feature requirements (use BMAD create-doc)
- `planning/technical-approach.md` - Technical decisions
- `planning/testing-strategy.md` - Test approach
- `integration/cross-feature-analysis.md` - Impact analysis

### 1.3 Cross-Feature Analysis
Update the following documents:
- Review `project-knowledge/features/feature-index.md`
- Identify dependencies and impacts
- Document in `integration/cross-feature-analysis.md`

## Phase 2: Development

### 2.1 Development Setup
Work in the `development/` directory:
```
feature-{name}/
├── development/
│   ├── backend/          # Backend code in progress
│   ├── frontend/         # Frontend code in progress  
│   ├── scripts/          # Development scripts
│   └── notes/            # Development notes
```

### 2.2 BMAD Development Support
**Useful BMAD Commands:**
- `@bmad-master *kb` → Access BMAD knowledge base for patterns
- `@bmad-master *task document-project` → If documenting complex logic
- `@bmad-master *task generate-ai-frontend-prompt` → For AI assistance

### 2.3 Development Practices
- Keep `feature-manifest.md` updated with progress
- Document key decisions in development notes
- Use Cursor semantic search on `project-core/` for context
- Avoid cluttering `project-core/` during development

## Phase 3: Testing & Integration

### 3.1 Testing Approach
Work in the `testing/` directory:
```
testing/
├── unit-tests/           # Feature-specific unit tests
├── integration-tests/    # Cross-feature integration tests
├── test-results/         # Test outputs and reports
└── test-data/           # Test datasets and fixtures
```

### 3.2 Cross-Feature Testing
- Review `integration/cross-feature-analysis.md`
- Test identified integration points
- Validate upstream and downstream impacts
- Document test results

### 3.3 BMAD Testing Support
**BMAD Commands:**
- `@bmad-master *execute-checklist {story-dod-checklist}` → Verify completion criteria
- `@bmad-master *task execute-checklist` → Run testing checklists

## Phase 4: Completion & Integration

### 4.1 Code Migration
Move production-ready code to `project-core/`:
```powershell
# Example migration
Copy-Item "active-work\feature-address-validation\development\backend\*" "project-core\backend\" -Recurse
Copy-Item "active-work\feature-address-validation\development\frontend\*" "project-core\frontend\" -Recurse
```

### 4.2 Documentation Creation
Create feature documentation in `project-knowledge/features/{feature-name}/`:
- `implementation.md` (use template)
- `decisions.md` - Key technical decisions
- `testing-approach.md` - How it was tested
- `cross-references.md` - Related features
- `artifacts/` - Supporting files

### 4.3 BMAD Documentation Support
**BMAD Commands:**
- `@bmad-master *create-doc {brownfield-architecture-tmpl}` → Document architecture impacts
- `@bmad-master *task document-project` → Create comprehensive docs

## Phase 5: Cleanup & Review

### 5.1 Automated Cleanup
```powershell
# Run feature cleanup script
.\development-tools\scripts\cleanup\feature-cleanup.ps1 -FeatureName "address-validation"
```

### 5.2 Manual Tasks
- [ ] Update `project-knowledge/features/feature-index.md`
- [ ] Archive working files to `project-artifacts/`
- [ ] Update cross-references
- [ ] Review and consolidate related features

### 5.3 BMAD Review Support
**BMAD Commands:**
- `@bmad-master *execute-checklist {architect-checklist}` → Architecture review
- `@bmad-master *execute-checklist {change-checklist}` → Change impact review

## Integration with Cursor IDE

### Cursor Optimization
- Keep `project-core/` clean for optimal semantic search
- Use feature workspaces for development clutter
- Reference production code patterns from `project-core/`
- Use Cursor's navigation for cross-feature references

### Cursor + BMAD Synergy
1. **BMAD for Structure** → Use BMAD tasks for planning and documentation
2. **Cursor for Implementation** → Use Cursor for coding and navigation
3. **Framework for Organization** → Use this workflow for lifecycle management

## Workflow Checklist

### Planning Phase ✅
- [ ] Feature workspace created
- [ ] Feature manifest completed
- [ ] BMAD planning tasks executed
- [ ] Cross-feature analysis completed
- [ ] Dependencies identified

### Development Phase ✅
- [ ] Development workspace organized
- [ ] Key decisions documented
- [ ] Progress tracked in manifest
- [ ] BMAD support used as needed

### Testing Phase ✅
- [ ] Unit tests created
- [ ] Integration tests completed
- [ ] Cross-feature impacts validated
- [ ] Test results documented

### Integration Phase ✅
- [ ] Code migrated to project-core
- [ ] Documentation created
- [ ] Feature index updated
- [ ] Cross-references established

### Cleanup Phase ✅
- [ ] Cleanup script executed
- [ ] Working files archived
- [ ] Manual updates completed
- [ ] Review completed

## Benefits

### For Development
- Clear separation of work phases
- Reduced clutter in main codebase
- Better feature traceability
- Cross-feature relationship tracking

### For BMAD Method
- Structured application of BMAD tasks
- Clear artifact organization
- Consistent documentation patterns
- Workflow reproducibility

### For Cursor IDE
- Optimized semantic search
- Clean navigation experience
- Better code discovery
- Reduced false positives in search

### For Project Maintenance
- Systematic cleanup processes
- Historical context preservation
- Scalable organization
- Future-proof structure

---

**Next Steps**: Use this workflow for the next feature development cycle and iterate based on experience.

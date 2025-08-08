# Start New Feature Script
# Creates a new feature workspace with proper structure

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName,
    
    [Parameter(Mandatory=$false)]
    [string]$Epic = "",
    
    [Parameter(Mandatory=$false)]
    [string]$StoryId = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Priority = "Medium"
)

$ProjectRoot = "C:\Users\tonyk\OneDrive\Projects\JobTrackerDB"
$FeaturePath = "$ProjectRoot\active-work\feature-$FeatureName"
$TemplatePath = "$ProjectRoot\development-tools\templates"

Write-Host "🚀 Starting new feature: $FeatureName" -ForegroundColor Green

# Check if feature already exists
if (Test-Path $FeaturePath) {
    Write-Host "❌ Feature workspace already exists: $FeaturePath" -ForegroundColor Red
    exit 1
}

# Create feature workspace structure
Write-Host "📁 Creating feature workspace structure..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "$FeaturePath\planning" -Force | Out-Null
New-Item -ItemType Directory -Path "$FeaturePath\development" -Force | Out-Null
New-Item -ItemType Directory -Path "$FeaturePath\testing" -Force | Out-Null
New-Item -ItemType Directory -Path "$FeaturePath\integration" -Force | Out-Null

Write-Host "   ✅ Created workspace: $FeaturePath" -ForegroundColor Green

# Create feature manifest from template
Write-Host "📝 Creating feature manifest..." -ForegroundColor Cyan
$ManifestTemplate = Get-Content "$TemplatePath\feature-manifest-template.md" -Raw

$ManifestContent = $ManifestTemplate `
    -replace '\{Feature Name\}', $FeatureName `
    -replace '\{Epic Name\}', $Epic `
    -replace '\{Story ID\}', $StoryId `
    -replace '\{High/Medium/Low\}', $Priority `
    -replace '\{Planning/Development/Testing/Complete\}', 'Planning' `
    -replace '\{YYYY-MM-DD\}', (Get-Date -Format 'yyyy-MM-dd')

Set-Content -Path "$FeaturePath\feature-manifest.md" -Value $ManifestContent
Write-Host "   ✅ Created feature manifest" -ForegroundColor Green

# Create initial planning documents
Write-Host "📋 Setting up planning documents..." -ForegroundColor Cyan

# Create basic planning files
$PlanningFiles = @(
    "requirements.md",
    "technical-approach.md",
    "testing-strategy.md"
)

foreach ($file in $PlanningFiles) {
    $content = @"
# $($file -replace '\.md$', '' -replace '-', ' ' | %{(Get-Culture).TextInfo.ToTitleCase($_)}) - $FeatureName

## Overview
{Add content here}

## Details
{Add detailed information}

Created: $(Get-Date -Format 'yyyy-MM-dd')
"@
    Set-Content -Path "$FeaturePath\planning\$file" -Value $content
}

Write-Host "   ✅ Created planning documents" -ForegroundColor Green

# Create integration analysis template
Write-Host "🔗 Setting up integration analysis..." -ForegroundColor Cyan
$IntegrationContent = @"
# Cross-Feature Integration Analysis - $FeatureName

## Upstream Dependencies
- [ ] {Feature that must be complete first}
- [ ] {Another dependency}

## Downstream Impacts
- [ ] {Feature that will be affected}
- [ ] {Another affected feature}

## Shared Components
### Backend Components
- [ ] {Shared API endpoints}
- [ ] {Database tables}
- [ ] {Services}

### Frontend Components
- [ ] {Shared React components}
- [ ] {Shared utilities}
- [ ] {Shared styles}

## Integration Testing
- [ ] {Cross-feature test scenario 1}
- [ ] {Cross-feature test scenario 2}

## Risk Assessment
### High Risk
- {Risk and mitigation}

### Medium Risk
- {Risk and mitigation}

Created: $(Get-Date -Format 'yyyy-MM-dd')
"@

Set-Content -Path "$FeaturePath\integration\cross-feature-analysis.md" -Value $IntegrationContent
Write-Host "   ✅ Created integration analysis template" -ForegroundColor Green

# Update feature index
Write-Host "📇 Updating feature index..." -ForegroundColor Cyan
$IndexPath = "$ProjectRoot\project-knowledge\features\feature-index.md"

if (Test-Path $IndexPath) {
    $IndexContent = Get-Content $IndexPath -Raw
    
    # Find the section to add to (you might want to customize this)
    $NewEntry = "- **$FeatureName**: {Description} → [affects: TBD]"
    
    Write-Host "   📝 Manual update required for feature-index.md" -ForegroundColor Yellow
    Write-Host "   💡 Add this entry: $NewEntry" -ForegroundColor Yellow
} else {
    Write-Host "   ⚠️  Feature index not found: $IndexPath" -ForegroundColor Yellow
}

# Show next steps
Write-Host ""
Write-Host "🎯 Feature workspace created successfully!" -ForegroundColor Green
Write-Host "📍 Location: $FeaturePath" -ForegroundColor White
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Update feature-manifest.md with specific requirements"
Write-Host "   2. Complete planning documents in planning/"
Write-Host "   3. Update cross-feature-analysis.md with dependencies"
Write-Host "   4. Add entry to feature-index.md"
Write-Host "   5. Start development in development/"
Write-Host ""
Write-Host "🔧 Useful Commands:" -ForegroundColor Cyan
Write-Host "   Open workspace: code `"$FeaturePath`""
Write-Host "   Edit manifest: code `"$FeaturePath\feature-manifest.md`""
Write-Host "   Cleanup (when done): .\development-tools\scripts\cleanup\feature-cleanup.ps1 -FeatureName `"$FeatureName`""

# Quick Start Feature Script
param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName
)

$ProjectRoot = "C:\Users\tonyk\OneDrive\Projects\JobTrackerDB"
$FeaturePath = "$ProjectRoot\active-work\feature-$FeatureName"

Write-Host "🚀 Creating feature workspace: $FeatureName" -ForegroundColor Green

# Create directories
New-Item -ItemType Directory -Path "$FeaturePath\planning" -Force | Out-Null
New-Item -ItemType Directory -Path "$FeaturePath\development" -Force | Out-Null
New-Item -ItemType Directory -Path "$FeaturePath\testing" -Force | Out-Null
New-Item -ItemType Directory -Path "$FeaturePath\integration" -Force | Out-Null

# Create basic manifest
$manifest = @"
# Feature Manifest: $FeatureName

## Overview
- **Epic**: EPC-1
- **Story ID**: EPC-1.15
- **Priority**: High
- **Status**: Planning
- **Created**: $(Get-Date -Format 'yyyy-MM-dd')

## Scope
- Address validation backend integration
- Geoscape API implementation

## Success Criteria
- [ ] Backend API endpoints implemented
- [ ] Database integration working
- [ ] Frontend integration complete

Created: $(Get-Date -Format 'yyyy-MM-dd')
"@

Set-Content -Path "$FeaturePath\feature-manifest.md" -Value $manifest

Write-Host "✅ Feature workspace created at: $FeaturePath" -ForegroundColor Green
Write-Host "📝 Edit the manifest: $FeaturePath\feature-manifest.md" -ForegroundColor Cyan

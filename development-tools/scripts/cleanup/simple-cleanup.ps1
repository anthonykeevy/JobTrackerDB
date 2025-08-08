# Simple Feature Cleanup Script
param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName,
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun
)

$ProjectRoot = "C:\Users\tonyk\OneDrive\Projects\JobTrackerDB"
$FeaturePath = "$ProjectRoot\active-work\feature-$FeatureName"

Write-Host "Feature Cleanup: $FeatureName" -ForegroundColor Green

if (-not (Test-Path $FeaturePath)) {
    Write-Host "Feature workspace not found: $FeaturePath" -ForegroundColor Red
    exit 1
}

Write-Host "Cleanup checklist for: $FeatureName"

# Check development folder
$DevPath = "$FeaturePath\development"
if (Test-Path $DevPath) {
    $Files = Get-ChildItem $DevPath -Recurse -File
    if ($Files.Count -gt 0) {
        Write-Host "Found $($Files.Count) files in development folder" -ForegroundColor Yellow
        Write-Host "Review these files for migration to project-core:" -ForegroundColor Yellow
        $Files | ForEach-Object { Write-Host "  - $($_.FullName)" }
    } else {
        Write-Host "Development folder is clean" -ForegroundColor Green
    }
}

# Check documentation
$KnowledgePath = "$ProjectRoot\project-knowledge\features\$FeatureName"
if (-not (Test-Path $KnowledgePath)) {
    Write-Host "Feature documentation folder not created" -ForegroundColor Yellow
    if (-not $DryRun) {
        New-Item -ItemType Directory -Path $KnowledgePath -Force | Out-Null
        Write-Host "Created documentation folder: $KnowledgePath" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Review and migrate production code from development/ to project-core/"
Write-Host "2. Create implementation documentation"
Write-Host "3. Update feature-index.md"
Write-Host "4. Archive working files"
Write-Host "5. Remove feature workspace when complete"

if ($DryRun) {
    Write-Host ""
    Write-Host "This was a dry run. Use without -DryRun to perform actions." -ForegroundColor Yellow
}

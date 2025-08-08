# Feature Cleanup Script
# This script helps organize completed features and clean up workspace

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName,
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun
)

$ProjectRoot = "C:\Users\tonyk\OneDrive\Projects\JobTrackerDB"
$FeaturePath = "$ProjectRoot\active-work\feature-$FeatureName"
$ArchivePath = "$ProjectRoot\project-artifacts\archived-features"
$KnowledgePath = "$ProjectRoot\project-knowledge\features\$FeatureName"

Write-Host "🧹 Feature Cleanup: $FeatureName" -ForegroundColor Green

if (-not (Test-Path $FeaturePath)) {
    Write-Host "❌ Feature workspace not found: $FeaturePath" -ForegroundColor Red
    exit 1
}

# Check if feature-manifest.md exists
$ManifestPath = "$FeaturePath\feature-manifest.md"
if (-not (Test-Path $ManifestPath)) {
    Write-Host "⚠️  Feature manifest not found. Creating from template..." -ForegroundColor Yellow
    # Could copy template here
}

Write-Host "📋 Cleanup checklist for: $FeatureName"

# 1. Check production code status
Write-Host "1. 🔍 Checking production code migration..."
$DevPath = "$FeaturePath\development"
if (Test-Path $DevPath) {
    $Files = Get-ChildItem $DevPath -Recurse -File
    if ($Files.Count -gt 0) {
        Write-Host "   ⚠️  Found $($Files.Count) files in development folder" -ForegroundColor Yellow
        Write-Host "   📝 Review these files for migration to project-core:" -ForegroundColor Yellow
        $Files | ForEach-Object { Write-Host "      - $($_.FullName)" }
    } else {
        Write-Host "   ✅ Development folder is clean" -ForegroundColor Green
    }
}

# 2. Check documentation status
Write-Host "2. 📚 Checking documentation..."
if (-not (Test-Path $KnowledgePath)) {
    Write-Host "   ⚠️  Feature documentation folder not created" -ForegroundColor Yellow
    if (-not $DryRun) {
        New-Item -ItemType Directory -Path $KnowledgePath -Force | Out-Null
        Write-Host "   ✅ Created documentation folder: $KnowledgePath" -ForegroundColor Green
    }
}

# 3. Archive working files
Write-Host "3. 📦 Archiving working files..."
if (-not $DryRun) {
    if (-not (Test-Path $ArchivePath)) {
        New-Item -ItemType Directory -Path $ArchivePath -Force | Out-Null
    }
    
    $ArchiveFeaturePath = "$ArchivePath\$FeatureName-$(Get-Date -Format 'yyyy-MM-dd')"
    if (-not (Test-Path $ArchiveFeaturePath)) {
        Copy-Item -Path $FeaturePath -Destination $ArchiveFeaturePath -Recurse -Force
        Write-Host "   ✅ Archived to: $ArchiveFeaturePath" -ForegroundColor Green
    }
}

# 4. Check test results
Write-Host "4. 🧪 Checking test results..."
$TestPath = "$FeaturePath\testing"
if (Test-Path $TestPath) {
    $TestFiles = Get-ChildItem $TestPath -Recurse -File
    if ($TestFiles.Count -gt 0) {
        Write-Host "   📊 Found $($TestFiles.Count) test files" -ForegroundColor Cyan
        Write-Host "   💡 Consider moving important test results to project-artifacts/test-results/" -ForegroundColor Cyan
    }
}

# 5. Update feature index
Write-Host "5. 📇 Feature index update needed..."
$IndexPath = "$ProjectRoot\project-knowledge\features\feature-index.md"
if (Test-Path $IndexPath) {
    Write-Host "   📝 Manually update feature-index.md with completion status" -ForegroundColor Yellow
} else {
    Write-Host "   ❌ Feature index not found: $IndexPath" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Review and migrate production code from development/ to project-core/"
Write-Host "   2. Create implementation documentation in project-knowledge/features/$FeatureName/"
Write-Host "   3. Update feature-index.md with relationships and status"
Write-Host "   4. Move test artifacts to appropriate project-artifacts/ locations"
Write-Host "   5. Remove feature workspace: Remove-Item '$FeaturePath' -Recurse -Force"

if ($DryRun) {
    Write-Host ""
    Write-Host "🔍 This was a dry run. Use without -DryRun to perform actions." -ForegroundColor Yellow
}

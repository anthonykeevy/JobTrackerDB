# Weekly Project Maintenance Script
# Performs routine cleanup and organization tasks

param(
    [Parameter(Mandatory=$false)]
    [switch]$DryRun
)

$ProjectRoot = "C:\Users\tonyk\OneDrive\Projects\JobTrackerDB"

Write-Host "🔧 Weekly Project Maintenance" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# 1. Review active features
Write-Host "1. 📋 Reviewing active features..." -ForegroundColor Cyan
$ActiveWorkPath = "$ProjectRoot\active-work"
$FeatureFolders = Get-ChildItem $ActiveWorkPath -Directory | Where-Object { $_.Name -like "feature-*" }

if ($FeatureFolders.Count -eq 0) {
    Write-Host "   ✅ No active feature workspaces found" -ForegroundColor Green
} else {
    Write-Host "   📊 Found $($FeatureFolders.Count) active feature(s):" -ForegroundColor Yellow
    foreach ($folder in $FeatureFolders) {
        $FeatureName = $folder.Name -replace "^feature-", ""
        $ManifestPath = "$($folder.FullName)\feature-manifest.md"
        
        if (Test-Path $ManifestPath) {
            $ManifestContent = Get-Content $ManifestPath -Raw
            if ($ManifestContent -match "Status.*?:\s*(.+)") {
                $Status = $matches[1].Trim()
                Write-Host "      - $FeatureName [$Status]" -ForegroundColor White
            } else {
                Write-Host "      - $FeatureName [Status Unknown]" -ForegroundColor Yellow
            }
        } else {
            Write-Host "      - $FeatureName [No Manifest]" -ForegroundColor Red
        }
    }
}

# 2. Clean up old test results
Write-Host ""
Write-Host "2. 🧪 Cleaning up old test results..." -ForegroundColor Cyan
$TestResultsPath = "$ProjectRoot\project-artifacts\test-results"
$ArchiveThreshold = (Get-Date).AddDays(-30)

if (Test-Path $TestResultsPath) {
    $OldResults = Get-ChildItem $TestResultsPath -Directory | Where-Object { $_.CreationTime -lt $ArchiveThreshold }
    
    if ($OldResults.Count -eq 0) {
        Write-Host "   ✅ No old test results to archive" -ForegroundColor Green
    } else {
        Write-Host "   📦 Found $($OldResults.Count) old test result folder(s) to archive" -ForegroundColor Yellow
        
        if (-not $DryRun) {
            $ArchivePath = "$ProjectRoot\project-artifacts\archived\test-results"
            if (-not (Test-Path $ArchivePath)) {
                New-Item -ItemType Directory -Path $ArchivePath -Force | Out-Null
            }
            
            foreach ($folder in $OldResults) {
                $ArchiveTarget = "$ArchivePath\$($folder.Name)"
                if (-not (Test-Path $ArchiveTarget)) {
                    Move-Item -Path $folder.FullName -Destination $ArchiveTarget
                    Write-Host "      ✅ Archived: $($folder.Name)" -ForegroundColor Green
                }
            }
        }
    }
}

# 3. Rotate logs
Write-Host ""
Write-Host "3. 📜 Rotating logs..." -ForegroundColor Cyan
$LogsPath = "$ProjectRoot\project-artifacts\logs"
$ArchiveThreshold = (Get-Date).AddDays(-14)

if (Test-Path $LogsPath) {
    $LogFiles = Get-ChildItem $LogsPath -File -Recurse | Where-Object { 
        $_.LastWriteTime -lt $ArchiveThreshold -and $_.Extension -eq ".log" 
    }
    
    if ($LogFiles.Count -eq 0) {
        Write-Host "   ✅ No old log files to archive" -ForegroundColor Green
    } else {
        Write-Host "   📦 Found $($LogFiles.Count) old log file(s) to archive" -ForegroundColor Yellow
        
        if (-not $DryRun) {
            $ArchiveLogPath = "$ProjectRoot\project-artifacts\logs\archived"
            if (-not (Test-Path $ArchiveLogPath)) {
                New-Item -ItemType Directory -Path $ArchiveLogPath -Force | Out-Null
            }
            
            foreach ($file in $LogFiles) {
                $ArchiveFileName = "$($file.BaseName)-$($file.LastWriteTime.ToString('yyyy-MM-dd'))$($file.Extension)"
                $ArchiveTarget = "$ArchiveLogPath\$ArchiveFileName"
                
                if (-not (Test-Path $ArchiveTarget)) {
                    Move-Item -Path $file.FullName -Destination $ArchiveTarget
                    Write-Host "      ✅ Archived: $($file.Name) → $ArchiveFileName" -ForegroundColor Green
                }
            }
        }
    }
}

# 4. Check project-core cleanliness
Write-Host ""
Write-Host "4. 🏠 Checking project-core cleanliness..." -ForegroundColor Cyan
$ProjectCorePath = "$ProjectRoot\project-core"

if (-not (Test-Path $ProjectCorePath)) {
    Write-Host "   ⚠️  project-core directory not found" -ForegroundColor Yellow
} else {
    # Check for temporary files
    $TempFiles = Get-ChildItem $ProjectCorePath -Recurse -File | Where-Object { 
        $_.Name -match "\.(tmp|temp|bak|old)$" -or 
        $_.Name -like "test_*" -or 
        $_.Name -like "*_test_*"
    }
    
    if ($TempFiles.Count -eq 0) {
        Write-Host "   ✅ project-core is clean" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Found $($TempFiles.Count) potential temporary file(s) in project-core:" -ForegroundColor Yellow
        $TempFiles | ForEach-Object { Write-Host "      - $($_.FullName)" }
    }
}

# 5. Generate maintenance report
Write-Host ""
Write-Host "5. 📊 Generating maintenance report..." -ForegroundColor Cyan
$ReportPath = "$ProjectRoot\project-meta\maintenance\weekly-report-$(Get-Date -Format 'yyyy-MM-dd').md"

if (-not $DryRun) {
    $ReportDir = Split-Path $ReportPath -Parent
    if (-not (Test-Path $ReportDir)) {
        New-Item -ItemType Directory -Path $ReportDir -Force | Out-Null
    }
    
    $Report = @"
# Weekly Maintenance Report - $(Get-Date -Format 'yyyy-MM-dd')

## Active Features
$($FeatureFolders.Count) active feature workspace(s)

## Cleanup Actions
- Test results: $($OldResults.Count) folders archived
- Log files: $($LogFiles.Count) files archived
- project-core: $($TempFiles.Count) potential temp files found

## Next Actions Needed
- Review active features for completion status
- Update feature-index.md if any features completed
- Consider archiving stale feature workspaces

Generated: $(Get-Date)
"@
    
    Set-Content -Path $ReportPath -Value $Report
    Write-Host "   ✅ Report saved: $ReportPath" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎯 Maintenance Summary:" -ForegroundColor Green
Write-Host "   Active Features: $($FeatureFolders.Count)"
Write-Host "   Test Results Archived: $($OldResults.Count)"
Write-Host "   Log Files Archived: $($LogFiles.Count)"
Write-Host "   Temp Files in project-core: $($TempFiles.Count)"

if ($DryRun) {
    Write-Host ""
    Write-Host "🔍 This was a dry run. Use without -DryRun to perform actions." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Weekly maintenance completed!" -ForegroundColor Green

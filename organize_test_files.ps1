# JobTrackerDB Test Files Organization Script
# This script moves test files from the backend directory to their appropriate locations
# in the organized testing structure.

Write-Host "📁 Organizing JobTrackerDB Test Files" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Create the organized testing structure if it doesn't exist
Write-Host "Creating testing directory structure..." -ForegroundColor Yellow

$testDirs = @(
    "../tests/backend/ai/baseline",
    "../tests/backend/ai/performance", 
    "../tests/backend/ai/prompts",
    "../tests/backend/api",
    "../tests/backend/database",
    "../tests/backend/integration",
    "../tests/frontend/components",
    "../tests/frontend/pages",
    "../tests/frontend/integration",
    "../tests/general/performance",
    "../tests/general/security",
    "../tests/general/e2e",
    "../tests/data/resumes",
    "../tests/data/baseline",
    "../tests/data/exports"
)

foreach ($dir in $testDirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created: $dir" -ForegroundColor Cyan
    }
}

Write-Host "`n📦 Moving test files to organized structure..." -ForegroundColor Yellow

# AI/Resume Parsing Tests
$aiFiles = @{
    "test_resume_parser_performance.py" = "../tests/backend/ai/performance/"
    "test_prompt_management.py" = "../tests/backend/ai/prompts/"
    "compare_prompt_versions.py" = "../tests/backend/ai/prompts/"
    "improve_resume_prompt.py" = "../tests/backend/ai/prompts/"
    "activate_prompt.py" = "../tests/backend/ai/prompts/"
    "check_prompts.py" = "../tests/backend/ai/prompts/"
    "cleanup_prompts.py" = "../tests/backend/ai/prompts/"
    "initialize_prompts.py" = "../tests/backend/ai/prompts/"
}

# API Tests
$apiFiles = @{
    "test_resume_upload.py" = "../tests/backend/api/"
    "test_address_api.py" = "../tests/backend/api/"
    "test_geoscape_api.py" = "../tests/backend/api/"
    "test_geoscape_api_v2.py" = "../tests/backend/api/"
    "test_geoscape_raw_response.py" = "../tests/backend/api/"
    "test_coordinates.py" = "../tests/backend/api/"
}

# Database Tests
$databaseFiles = @{
    "check_resume_data_saved.py" = "../tests/backend/database/"
    "check_resume_data.py" = "../tests/backend/database/"
    "schema_comparison.py" = "../tests/backend/database/"
    "create_smart_migration.py" = "../tests/backend/database/"
    "safe_migration_template.py" = "../tests/backend/database/"
    "setup_database.py" = "../tests/backend/database/"
    "reset_password.py" = "../tests/backend/database/"
}

# Integration Tests
$integrationFiles = @{
    "mcp_server.py" = "../tests/backend/integration/"
}

# Performance Tests
$performanceFiles = @{
    "test_results_test_20250805_192953.json" = "../tests/general/performance/"
    "test_results_test_20250805_192752.json" = "../tests/general/performance/"
    "test_results_test_20250805_185426.json" = "../tests/general/performance/"
    "test_results_test_20250805_185104.json" = "../tests/general/performance/"
    "test_results_test_20250805_185009.json" = "../tests/general/performance/"
}

# Data Files
$dataFiles = @{
    "JobTrackerDB_API.postman_collection.json" = "../tests/data/exports/"
    "JobTrackerDB_API.postman_environment.json" = "../tests/data/exports/"
    "README_Postman_Testing.md" = "../tests/data/exports/"
}

# Function to move files
function Move-TestFiles {
    param(
        [hashtable]$fileMapping,
        [string]$category
    )
    
    Write-Host "`n📂 Moving $category files..." -ForegroundColor Magenta
    
    foreach ($file in $fileMapping.Keys) {
        $sourcePath = $file
        $destPath = $fileMapping[$file] + $file
        
        if (Test-Path $sourcePath) {
            try {
                Move-Item $sourcePath $destPath -Force
                Write-Host "  ✅ Moved: $file -> $($fileMapping[$file])" -ForegroundColor Green
            }
            catch {
                Write-Host "  ❌ Failed to move: $file - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
        else {
            Write-Host "  ⚠️  File not found: $file" -ForegroundColor Yellow
        }
    }
}

# Move files by category
Move-TestFiles -fileMapping $aiFiles -category "AI/Resume Parsing"
Move-TestFiles -fileMapping $apiFiles -category "API"
Move-TestFiles -fileMapping $databaseFiles -category "Database"
Move-TestFiles -fileMapping $integrationFiles -category "Integration"
Move-TestFiles -fileMapping $performanceFiles -category "Performance"
Move-TestFiles -fileMapping $dataFiles -category "Data/Exports"

# Create a summary of the organization
Write-Host "`n📊 Organization Summary" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Green

$categories = @{
    "AI/Resume Parsing" = "../tests/backend/ai/"
    "API Tests" = "../tests/backend/api/"
    "Database Tests" = "../tests/backend/database/"
    "Integration Tests" = "../tests/backend/integration/"
    "Performance Tests" = "../tests/general/performance/"
    "Data/Exports" = "../tests/data/exports/"
}

foreach ($category in $categories.Keys) {
    $path = $categories[$category]
    if (Test-Path $path) {
        $fileCount = (Get-ChildItem $path -File | Measure-Object).Count
        Write-Host "  $category`: $fileCount files" -ForegroundColor Cyan
    }
}

Write-Host "`n🎉 Test file organization completed!" -ForegroundColor Green
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review the moved files in their new locations" -ForegroundColor White
Write-Host "  2. Update any import paths in the moved files" -ForegroundColor White
Write-Host "  3. Run the baseline extractor: cd tests/backend/ai/baseline && python extract_resume_baseline.py" -ForegroundColor White
Write-Host "  4. Test the organized structure" -ForegroundColor White

Write-Host "`n📁 Testing Structure Created:" -ForegroundColor Green
Write-Host "  tests/" -ForegroundColor Cyan
Write-Host "  ├── backend/" -ForegroundColor Cyan
Write-Host "  │   ├── ai/" -ForegroundColor Cyan
Write-Host "  │   │   ├── baseline/" -ForegroundColor Cyan
Write-Host "  │   │   ├── performance/" -ForegroundColor Cyan
Write-Host "  │   │   └── prompts/" -ForegroundColor Cyan
Write-Host "  │   ├── api/" -ForegroundColor Cyan
Write-Host "  │   ├── database/" -ForegroundColor Cyan
Write-Host "  │   └── integration/" -ForegroundColor Cyan
Write-Host "  ├── frontend/" -ForegroundColor Cyan
Write-Host "  ├── general/" -ForegroundColor Cyan
Write-Host "  └── data/" -ForegroundColor Cyan 
-- Query to see the benefits and details of the Resume Parsing Prompt Management System
-- This query shows the resume parsing prompt, its versions, and performance metrics

-- 1. Show all prompts with their details
SELECT 
    PromptID,
    PromptName,
    PromptType,
    PromptVersion,
    Description,
    IsActive,
    IsDefault,
    createdDate,
    createdBy,
    lastUpdated,
    updatedBy
FROM PromptManagement
ORDER BY PromptType, PromptVersion DESC;

-- 2. Show the active resume parsing prompt
SELECT 
    PromptType,
    PromptName,
    PromptVersion,
    IsActive,
    IsDefault,
    Description
FROM PromptManagement
WHERE IsActive = 1
ORDER BY PromptType;

-- 3. Show resume parsing prompt content details (truncated for readability)
SELECT 
    PromptID,
    PromptName,
    PromptType,
    PromptVersion,
    LEFT(SystemPrompt, 100) + '...' AS SystemPrompt_Preview,
    LEFT(UserPrompt, 100) + '...' AS UserPrompt_Preview,
    LEFT(ExpectedOutput, 100) + '...' AS ExpectedOutput_Preview,
    LEFT(ValidationRules, 100) + '...' AS ValidationRules_Preview,
    LEFT(PerformanceMetrics, 100) + '...' AS PerformanceMetrics_Preview
FROM PromptManagement
ORDER BY PromptType, PromptVersion DESC;

-- 4. Show prompt statistics
SELECT 
    PromptType,
    COUNT(*) AS TotalPrompts,
    COUNT(CASE WHEN IsActive = 1 THEN 1 END) AS ActivePrompts,
    COUNT(CASE WHEN IsDefault = 1 THEN 1 END) AS DefaultPrompts,
    MAX(PromptVersion) AS LatestVersion,
    MIN(createdDate) AS FirstCreated,
    MAX(createdDate) AS LastCreated
FROM PromptManagement
GROUP BY PromptType;

-- 5. Show the full content of the Resume Parser prompt
SELECT 
    PromptID,
    PromptName,
    PromptType,
    PromptVersion,
    SystemPrompt,
    UserPrompt,
    ExpectedOutput,
    ValidationRules,
    PerformanceMetrics,
    Description,
    IsActive,
    IsDefault
FROM PromptManagement
WHERE PromptType = 'resume_parse' AND IsActive = 1;

-- 6. Show the full content of the Resume Parser prompt (detailed view)
SELECT 
    PromptID,
    PromptName,
    PromptType,
    PromptVersion,
    SystemPrompt,
    UserPrompt,
    ExpectedOutput,
    ValidationRules,
    PerformanceMetrics,
    Description,
    IsActive,
    IsDefault
FROM PromptManagement
WHERE PromptType = 'resume_parse' AND IsActive = 1;

-- 7. Show resume parsing prompt version history
SELECT 
    PromptType,
    PromptName,
    PromptVersion,
    IsActive,
    IsDefault,
    createdDate,
    createdBy,
    CASE 
        WHEN IsActive = 1 THEN 'ACTIVE'
        WHEN IsDefault = 1 THEN 'DEFAULT'
        ELSE 'INACTIVE'
    END AS Status
FROM PromptManagement
ORDER BY PromptType, PromptVersion DESC; 
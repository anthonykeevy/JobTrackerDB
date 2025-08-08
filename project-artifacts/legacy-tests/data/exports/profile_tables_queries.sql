-- SQL Queries to Select All Fields from Profile Tables
-- JobTrackerDB Profile Tables

-- 1. Main Profile Table
SELECT * FROM Profile;

-- 2. Profile Work Experience Table
SELECT * FROM ProfileWorkExperience;

-- 3. Profile Education Table
SELECT * FROM ProfileEducation;

-- 4. Profile Skills Table
SELECT * FROM Skills;

-- 5. Profile Certifications Table
SELECT * FROM ProfileCertification;

-- 6. User Table (linked to Profile)
SELECT * FROM [User];

-- 7. Profile Address Table (if exists)
SELECT * FROM ProfileAddress;

-- 8. Profile Projects Table (if exists)
SELECT * FROM ProfileProjects;

-- 9. Profile Languages Table (if exists)
SELECT * FROM ProfileLanguages;

-- 10. Profile References Table (if exists)
SELECT * FROM ProfileReferences;

-- 11. Profile Awards Table (if exists)
SELECT * FROM ProfileAwards;

-- 12. Profile Publications Table (if exists)
SELECT * FROM ProfilePublications;

-- 13. Profile Volunteer Work Table (if exists)
SELECT * FROM ProfileVolunteerWork;

-- 14. Profile Interests Table (if exists)
SELECT * FROM ProfileInterests;

-- 15. Profile Social Media Table (if exists)
SELECT * FROM ProfileSocialMedia;

-- 16. Profile Resume Files Table
SELECT * FROM Resume;

-- 17. API Usage Tracking Table (for AI usage)
SELECT * FROM APIUsageTracking;

-- 18. Profile with User Information (JOIN query)
SELECT 
    p.*,
    u.UserID,
    u.Username,
    u.EmailAddress as UserEmail,
    u.IsActive,
    u.CreatedDate as UserCreatedDate
FROM Profile p
LEFT JOIN [User] u ON p.ProfileID = u.ProfileID;

-- 19. Complete Profile with All Related Data (Comprehensive JOIN)
SELECT 
    p.*,
    u.Username,
    u.EmailAddress as UserEmail,
    u.IsActive,
    COUNT(DISTINCT pwe.ProfileWorkExperienceID) as WorkExperienceCount,
    COUNT(DISTINCT pe.ProfileEducationID) as EducationCount,
    COUNT(DISTINCT s.SkillID) as SkillsCount,
    COUNT(DISTINCT pc.ProfileCertificationID) as CertificationsCount
FROM Profile p
LEFT JOIN [User] u ON p.ProfileID = u.ProfileID
LEFT JOIN ProfileWorkExperience pwe ON p.ProfileID = pwe.ProfileID
LEFT JOIN ProfileEducation pe ON p.ProfileID = pe.ProfileID
LEFT JOIN Skills s ON p.ProfileID = s.ProfileID
LEFT JOIN ProfileCertification pc ON p.ProfileID = pc.ProfileID
GROUP BY p.ProfileID, p.FirstName, p.LastName, p.EmailAddress, p.PhoneNumber, 
         p.Subtitle, p.DateOfBirth, p.Nationality, p.AddressLine1, p.AddressLine2, 
         p.AddressLine3, p.CreatedDate, p.CreatedBy, p.ModifiedDate, p.ModifiedBy,
         u.Username, u.EmailAddress, u.IsActive;

-- 20. Profile Statistics Query
SELECT 
    COUNT(*) as TotalProfiles,
    COUNT(CASE WHEN FirstName IS NOT NULL AND LastName IS NOT NULL THEN 1 END) as CompleteNames,
    COUNT(CASE WHEN EmailAddress IS NOT NULL THEN 1 END) as HasEmail,
    COUNT(CASE WHEN PhoneNumber IS NOT NULL THEN 1 END) as HasPhone,
    COUNT(CASE WHEN DateOfBirth IS NOT NULL THEN 1 END) as HasDateOfBirth,
    COUNT(CASE WHEN Subtitle IS NOT NULL THEN 1 END) as HasSummary,
    AVG(CASE WHEN DateOfBirth IS NOT NULL THEN DATEDIFF(YEAR, DateOfBirth, GETDATE()) END) as AverageAge
FROM Profile;

-- 21. Recent Profile Activity
SELECT 
    p.ProfileID,
    p.FirstName,
    p.LastName,
    p.ModifiedDate,
    p.ModifiedBy,
    u.Username as ModifiedByUsername
FROM Profile p
LEFT JOIN [User] u ON p.ModifiedBy = u.UserID
WHERE p.ModifiedDate IS NOT NULL
ORDER BY p.ModifiedDate DESC;

-- 22. Profile Completion Score Query
SELECT 
    p.ProfileID,
    p.FirstName,
    p.LastName,
    CASE 
        WHEN p.FirstName IS NOT NULL AND p.LastName IS NOT NULL THEN 1 
        ELSE 0 
    END as HasName,
    CASE WHEN p.EmailAddress IS NOT NULL THEN 1 ELSE 0 END as HasEmail,
    CASE WHEN p.PhoneNumber IS NOT NULL THEN 1 ELSE 0 END as HasPhone,
    CASE WHEN p.DateOfBirth IS NOT NULL THEN 1 ELSE 0 END as HasDateOfBirth,
    CASE WHEN p.Subtitle IS NOT NULL THEN 1 ELSE 0 END as HasSummary,
    CASE WHEN pwe.ProfileWorkExperienceID IS NOT NULL THEN 1 ELSE 0 END as HasWorkExperience,
    CASE WHEN pe.ProfileEducationID IS NOT NULL THEN 1 ELSE 0 END as HasEducation,
    CASE WHEN s.SkillID IS NOT NULL THEN 1 ELSE 0 END as HasSkills,
    CASE WHEN pc.ProfileCertificationID IS NOT NULL THEN 1 ELSE 0 END as HasCertifications
FROM Profile p
LEFT JOIN ProfileWorkExperience pwe ON p.ProfileID = pwe.ProfileID
LEFT JOIN ProfileEducation pe ON p.ProfileID = pe.ProfileID
LEFT JOIN Skills s ON p.ProfileID = s.ProfileID
LEFT JOIN ProfileCertification pc ON p.ProfileID = pc.ProfileID; 
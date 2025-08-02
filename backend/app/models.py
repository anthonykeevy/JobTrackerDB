"""
Naming Convention

- Database Name: `JobTrackerDB`
- Schema: Default `dbo` schema
- Table Names: Use singular names (e.g., `Profile`, `User`, `Resume`)
- Primary Keys: Use an auto-incrementing ID field named [TableName]ID (e.g., ProfileID, UserID)
- Foreign Keys: Named after the primary key they reference (e.g., ProfileID in child tables)
- Views: Prefix with `v_` (e.g., v_ProfileSummary)
- Stored Procedures: Prefix with `s_` (e.g., s_GetUserDetails)
- String Fields: Use `nvarchar` type to support Unicode characters for global compatibility
- Related Tables: Use hierarchical naming (e.g., ProfileSkill for skills linked to a profile, JobApplicationAttachment for files tied to job applications)

This naming convention ensures clarity, consistency, and ease of discovery for all database entities.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, DECIMAL, Text, Unicode, UnicodeText, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
import logging
import secrets

Base = declarative_base()

# Reference/lookup tables
class Country(Base):
    __tablename__ = 'countries'
    
    CountryID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), unique=True, nullable=False, index=True)
    CodeAlpha2 = Column(String(2), unique=True, nullable=False)  # ISO 3166-1 alpha-2
    CodeAlpha3 = Column(String(3), unique=True, nullable=False)  # ISO 3166-1 alpha-3
    NumericCode = Column(String(3), nullable=False)  # ISO 3166-1 numeric
    PhoneCode = Column(String(10), nullable=True)  # International dialing code
    CurrencyCode = Column(String(3), nullable=True)  # ISO 4217 currency code
    IsActive = Column(Boolean, default=True, nullable=False)
    DisplayOrder = Column(Integer, default=999, nullable=False)  # For ordering in dropdowns
    CreatedAt = Column(DateTime, default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class ProfileAddress(Base):
    """Enhanced address table with Geoscape API integration support"""
    __tablename__ = "ProfileAddress"
    
    ProfileAddressID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    
    # Standard address components
    StreetNumber = Column(Unicode(20))
    StreetName = Column(Unicode(255), nullable=False)
    StreetType = Column(Unicode(50))  # Street, Road, Avenue, etc.
    UnitNumber = Column(Unicode(20))  # Apartment, Unit, Suite
    UnitType = Column(Unicode(50))  # Unit, Apartment, Suite, etc.
    Suburb = Column(Unicode(100), nullable=False)
    State = Column(Unicode(50), nullable=False)
    Postcode = Column(Unicode(20), nullable=False)
    Country = Column(Unicode(100), nullable=False, default='Australia')
    
    # Geoscape API data
    PropertyID = Column(Unicode(100))  # Geoscape property identifier
    Latitude = Column(DECIMAL(10, 8))
    Longitude = Column(DECIMAL(11, 8))
    PropertyType = Column(Unicode(100))  # Residential, Commercial, etc.
    LandArea = Column(DECIMAL(10, 2))  # Square meters
    FloorArea = Column(DECIMAL(10, 2))  # Square meters
    
    # Validation and confidence
    IsValidated = Column(Boolean, default=False)
    ValidationSource = Column(Unicode(50))  # 'geoscape', 'smarty_streets', 'manual'
    ConfidenceScore = Column(DECIMAL(3, 2))  # 0.00 to 1.00
    ValidationDate = Column(DateTime)
    
    # Address status
    IsActive = Column(Boolean, default=True)
    IsPrimary = Column(Boolean, default=False)
    AddressType = Column(Unicode(50))  # 'residential', 'work', 'mailing', 'temporary'
    
    # Metadata
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))
    
    # Relationships
    profile = relationship("Profile", back_populates="addresses")
    
    def __repr__(self):
        return f"<ProfileAddress(ProfileID={self.ProfileID}, Address='{self.StreetNumber} {self.StreetName} {self.StreetType}, {self.Suburb} {self.State} {self.Postcode}')>"

class APIUsageTracking(Base):
    """Track external API usage for billing and monitoring"""
    __tablename__ = "APIUsageTracking"
    
    APIUsageID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=True)  # Can be null for system calls
    
    # API details
    APIProvider = Column(Unicode(50), nullable=False)  # 'geoscape', 'smarty_streets', 'openai', etc.
    APIEndpoint = Column(Unicode(255), nullable=False)  # Specific endpoint called
    RequestType = Column(Unicode(50), nullable=False)  # 'autocomplete', 'validate', 'geocode', etc.
    
    # Usage metrics
    CallCount = Column(Integer, default=1, nullable=False)
    CreditCost = Column(DECIMAL(10, 4), nullable=False)  # Cost in credits/API units
    ResponseTime = Column(Integer)  # Response time in milliseconds
    
    # Request/Response data
    RequestData = Column(UnicodeText)  # JSON string of request parameters
    ResponseStatus = Column(Unicode(20))  # 'success', 'error', 'timeout'
    ResponseData = Column(UnicodeText)  # JSON string of response (truncated if large)
    ErrorMessage = Column(Unicode(500))
    
    # Billing information
    BillingPeriod = Column(Unicode(20))  # 'YYYY-MM' for monthly billing
    IsBillable = Column(Boolean, default=True)
    
    # Metadata
    CreatedAt = Column(DateTime, default=func.now(), nullable=False)
    IPAddress = Column(Unicode(45))  # Support IPv6
    UserAgent = Column(Unicode(500))
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<APIUsageTracking(Provider={self.APIProvider}, Endpoint={self.APIEndpoint}, Cost={self.CreditCost})>"

class Role(Base):
    __tablename__ = "Role"
    RoleID = Column(Integer, primary_key=True, autoincrement=True)
    RoleName = Column(Unicode(50), unique=True, nullable=False)
    Description = Column(Unicode(255))
    IsSubscription = Column(Boolean, default=False)
    MonthlyCost = Column(DECIMAL(10, 2))
    MaxJobApplications = Column(Integer)
    CanGenerateAIContent = Column(Boolean, default=False)
    CanViewGamification = Column(Boolean, default=False)
    CanManageUsers = Column(Boolean, default=False)
    CanAccessAnalytics = Column(Boolean, default=False)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class Profile(Base):
    __tablename__ = "Profile"
    ProfileID = Column(Integer, primary_key=True, autoincrement=True)
    PhotoURL = Column(Unicode(500))
    FirstName = Column(Unicode(100), nullable=False)
    LastName = Column(Unicode(100), nullable=False)
    Subtitle = Column(Unicode(255))
    # Legacy address fields (deprecated - use ProfileAddress table)
    AddressLine1 = Column(Unicode(255))
    AddressLine2 = Column(Unicode(255))
    AddressLine3 = Column(Unicode(255))
    PhoneNumber = Column(Unicode(50))
    EmailAddress = Column(Unicode(255), unique=True, nullable=False)
    Website = Column(Unicode(255))
    LinkedInURL = Column(Unicode(255))
    GitHubURL = Column(Unicode(255))
    OtherSocialProfiles = Column(Unicode(500))
    DateOfBirth = Column(Unicode(50))
    Nationality = Column(Unicode(100))
    CountryCode = Column(Unicode(3))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))
    
    # Relationships
    addresses = relationship("ProfileAddress", back_populates="profile", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "User"
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(Unicode(100), unique=True, nullable=False)
    EmailAddress = Column(Unicode(255), unique=True, nullable=False)
    HashedPassword = Column(Unicode(500), nullable=False)
    IsActive = Column(Boolean, default=True)
    LastLogin = Column(DateTime)
    RoleID = Column(Integer, ForeignKey("Role.RoleID"), default=2, nullable=False)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    Provider = Column(Unicode(100))  # Added for social login
    ProviderUserID = Column(Unicode(100))  # Added for social login
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    role = relationship("Role")
    profile = relationship("Profile")

class UserPreferences(Base):
    __tablename__ = "UserPreferences"
    PreferenceID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    PhotoURLConsent = Column(Boolean, default=False)
    DateOfBirthConsent = Column(Boolean, default=False)
    GitHubURLConsent = Column(Boolean, default=False)
    NationalityConsent = Column(Boolean, default=False)
    OtherSocialProfilesConsent = Column(Boolean, default=False)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class UserRoleOverride(Base):
    __tablename__ = "UserRoleOverride"
    OverrideID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    CapabilityName = Column(Unicode(50), nullable=False)
    IsEnabled = Column(Boolean, nullable=False)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class Objective(Base):
    __tablename__ = "Objective"
    ObjectiveID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    Objective = Column(Unicode(1000), nullable=False)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class Languages(Base):
    __tablename__ = "Languages"
    LanguageID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    LanguageName = Column(Unicode(100), nullable=False)
    Level = Column(Unicode(50))
    Rating = Column(Unicode(50))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class Hobbies(Base):
    __tablename__ = "Hobbies"
    HobbyID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    HobbyName = Column(Unicode(100), nullable=False)
    Description = Column(Unicode(500))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class JobApplication(Base):
    __tablename__ = "JobApplication"
    JobApplicationID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    JobTitle = Column(Unicode(255), nullable=False)
    CompanyName = Column(Unicode(255), nullable=False)
    Location = Column(Unicode(255))
    DateApplied = Column(DateTime, nullable=False)
    ApplicationStatus = Column(Unicode(50))
    Source = Column(Unicode(100))
    JobListingURL = Column(Unicode(500))
    ResumeVersion = Column(Unicode(255))
    CoverLetterVersion = Column(Unicode(255))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class JobApplicationNote(Base):
    __tablename__ = "JobApplicationNote"
    JobApplicationNoteID = Column(Integer, primary_key=True, autoincrement=True)
    JobApplicationID = Column(Integer, ForeignKey("JobApplication.JobApplicationID"), nullable=False)
    NoteText = Column(UnicodeText, nullable=False)
    NoteDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class JobApplicationAttachment(Base):
    __tablename__ = "JobApplicationAttachment"
    JobApplicationAttachmentID = Column(Integer, primary_key=True, autoincrement=True)
    JobApplicationID = Column(Integer, ForeignKey("JobApplication.JobApplicationID"), nullable=False)
    FileName = Column(Unicode(255), nullable=False)
    FileType = Column(Unicode(50))
    FileURL = Column(Unicode(500), nullable=False)
    uploadedDate = Column(DateTime, default=datetime.utcnow)
    uploadedBy = Column(Unicode(100))

class JobApplicationStatusHistory(Base):
    __tablename__ = "JobApplicationStatusHistory"
    StatusHistoryID = Column(Integer, primary_key=True, autoincrement=True)
    JobApplicationID = Column(Integer, ForeignKey("JobApplication.JobApplicationID"), nullable=False)
    Status = Column(Unicode(50), nullable=False)
    StatusDate = Column(DateTime, default=datetime.utcnow)
    updatedBy = Column(Unicode(100))

class JobApplicationInterview(Base):
    __tablename__ = "JobApplicationInterview"
    InterviewID = Column(Integer, primary_key=True, autoincrement=True)
    JobApplicationID = Column(Integer, ForeignKey("JobApplication.JobApplicationID"), nullable=False)
    InterviewDate = Column(DateTime, nullable=False)
    InterviewType = Column(Unicode(50))
    Interviewer = Column(Unicode(255))
    InterviewNotes = Column(UnicodeText)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class JobApplicationTask(Base):
    __tablename__ = "JobApplicationTask"
    TaskID = Column(Integer, primary_key=True, autoincrement=True)
    JobApplicationID = Column(Integer, ForeignKey("JobApplication.JobApplicationID"), nullable=False)
    TaskDescription = Column(Unicode(1000), nullable=False)
    TaskStatus = Column(Unicode(50))
    DueDate = Column(DateTime)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class Skills(Base):
    __tablename__ = "Skills"

    SkillID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    SkillName = Column(Unicode(100), nullable=False)
    Proficiency = Column(Unicode(50))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class Resume(Base):
    __tablename__ = "Resume"

    ResumeID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    Title = Column(Unicode(255), nullable=False)
    Content = Column(UnicodeText, nullable=False)
    Format = Column(Unicode(50))  # markdown, HTML, text
    FileURL = Column(Unicode(500))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class CoverLetter(Base):
    __tablename__ = "CoverLetter"

    CoverLetterID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    Title = Column(Unicode(255), nullable=False)
    Content = Column(UnicodeText, nullable=False)
    Format = Column(Unicode(50))
    FileURL = Column(Unicode(500))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class Message(Base):
    __tablename__ = "Message"

    MessageID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    JobApplicationID = Column(Integer, ForeignKey("JobApplication.JobApplicationID"), nullable=True)
    Subject = Column(Unicode(255))
    Body = Column(UnicodeText, nullable=False)
    Format = Column(Unicode(50))
    FileURL = Column(Unicode(500))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

# Add AuthLog model
class AuthLog(Base):
    __tablename__ = "AuthLog"
    AuthLogID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=True)
    Provider = Column(Unicode(50), nullable=False)
    AttemptTime = Column(DateTime, default=datetime.utcnow, nullable=False)
    Success = Column(Boolean, nullable=False)
    ErrorMessage = Column(Unicode(500), nullable=True)
    IPAddress = Column(Unicode(50), nullable=True)

class UserPasswordResetToken(Base):
    __tablename__ = "UserPasswordResetToken"

    UserPasswordResetTokenID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    Token = Column(Unicode(128), unique=True, nullable=False, index=True)
    ExpiresAt = Column(DateTime, nullable=False)
    CreatedDate = Column(DateTime, default=datetime.utcnow, nullable=False)
    CreatedBy = Column(Unicode(100), nullable=False)

    user = relationship("User")

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)

# =============================================================================
# ENHANCED EMAIL MANAGEMENT SYSTEM
# =============================================================================

class UserEmailAddress(Base):
    __tablename__ = "UserEmailAddress"
    UserEmailAddressID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    EmailAddress = Column(Unicode(255), unique=True, nullable=False, index=True)
    EmailType = Column(Unicode(50))  # 'primary', 'personal', 'work', 'backup'
    IsVerified = Column(Boolean, default=False)
    IsActive = Column(Boolean, default=True)
    IsLoginEmail = Column(Boolean, default=False)
    VerificationToken = Column(Unicode(255))
    VerificationExpiry = Column(DateTime)
    VerifiedDate = Column(DateTime)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    user = relationship("User", back_populates="email_addresses")

class UserEmailAddressHistory(Base):
    __tablename__ = "UserEmailAddressHistory"
    UserEmailAddressHistoryID = Column(Integer, primary_key=True, autoincrement=True)
    UserEmailAddressID = Column(Integer, ForeignKey("UserEmailAddress.UserEmailAddressID"), nullable=False)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    EmailAddress = Column(Unicode(255), nullable=False)
    Action = Column(Unicode(50))  # 'added', 'verified', 'changed_login', 'deactivated', 'removed'
    PreviousValue = Column(Unicode(255))
    NewValue = Column(Unicode(255))
    Reason = Column(Unicode(500))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))

class UserEmailVerificationLog(Base):
    __tablename__ = "UserEmailVerificationLog"
    UserEmailVerificationLogID = Column(Integer, primary_key=True, autoincrement=True)
    UserEmailAddressID = Column(Integer, ForeignKey("UserEmailAddress.UserEmailAddressID"), nullable=False)
    VerificationToken = Column(Unicode(255))
    VerificationAttempts = Column(Integer, default=0)
    LastAttemptDate = Column(DateTime)
    IsSuccessful = Column(Boolean, default=False)
    IPAddress = Column(Unicode(50))
    UserAgent = Column(Unicode(500))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))

# =============================================================================
# ENHANCED PROFILE SYSTEM
# =============================================================================

class ProfileVersion(Base):
    __tablename__ = "ProfileVersion"
    ProfileVersionID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    VersionNumber = Column(Integer, nullable=False)
    IsConfirmed = Column(Boolean, default=False)
    HappinessScore = Column(DECIMAL(3,2))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    profile = relationship("Profile")

class ProfileCareerAspiration(Base):
    __tablename__ = "ProfileCareerAspiration"
    ProfileCareerAspirationID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    ShortTermRole = Column(Unicode(255))
    LongTermRole = Column(Unicode(255))
    AspirationStatement = Column(Unicode(1000))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    profile = relationship("Profile")

class ProfileEducation(Base):
    __tablename__ = "ProfileEducation"
    ProfileEducationID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    InstitutionName = Column(Unicode(255), nullable=False)
    Degree = Column(Unicode(255))
    FieldOfStudy = Column(Unicode(255))
    StartDate = Column(DateTime)
    EndDate = Column(DateTime)
    GPA = Column(DECIMAL(3,2))
    Description = Column(Unicode(1000))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    profile = relationship("Profile")

class ProfileWorkExperience(Base):
    __tablename__ = "ProfileWorkExperience"
    ProfileWorkExperienceID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    JobTitle = Column(Unicode(255), nullable=False)
    CompanyName = Column(Unicode(255), nullable=False)
    StartDate = Column(DateTime)
    EndDate = Column(DateTime)
    IsCurrent = Column(Boolean, default=False)
    Description = Column(Unicode(2000))
    Achievements = Column(Unicode(2000))
    IsAchievement = Column(Boolean, default=False)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    profile = relationship("Profile")

class ProfileCertification(Base):
    __tablename__ = "ProfileCertification"
    ProfileCertificationID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    CertificationName = Column(Unicode(255), nullable=False)
    IssuingOrganization = Column(Unicode(255))
    IssueDate = Column(DateTime)
    ExpiryDate = Column(DateTime)
    CredentialID = Column(Unicode(100))
    Description = Column(Unicode(1000))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    profile = relationship("Profile")

class ProfileProject(Base):
    __tablename__ = "ProfileProject"
    ProfileProjectID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    ProjectName = Column(Unicode(255), nullable=False)
    Description = Column(Unicode(2000))
    Technologies = Column(Unicode(500))
    ProjectURL = Column(Unicode(500))
    StartDate = Column(DateTime)
    EndDate = Column(DateTime)
    IsCurrent = Column(Boolean, default=False)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    profile = relationship("Profile")

class ProfileVolunteerExperience(Base):
    __tablename__ = "ProfileVolunteerExperience"
    ProfileVolunteerExperienceID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    OrganizationName = Column(Unicode(255), nullable=False)
    Role = Column(Unicode(255))
    StartDate = Column(DateTime)
    EndDate = Column(DateTime)
    Description = Column(Unicode(1000))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    profile = relationship("Profile")

# =============================================================================
# JOB DISCOVERY & LOGGING SYSTEM
# =============================================================================

class JobBoard(Base):
    __tablename__ = "JobBoard"
    JobBoardID = Column(Integer, primary_key=True, autoincrement=True)
    BoardName = Column(Unicode(255), nullable=False)
    BoardType = Column(Unicode(50))  # 'aggregator', 'recruiter', 'corporate'
    Domain = Column(Unicode(255))
    IndustryFocus = Column(Unicode(255))
    FunctionalArea = Column(Unicode(255))
    ValidationConfidence = Column(DECIMAL(3,2))
    IsActive = Column(Boolean, default=True)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

class JobBoardJob(Base):
    __tablename__ = "JobBoardJob"
    JobBoardJobID = Column(Integer, primary_key=True, autoincrement=True)
    JobBoardID = Column(Integer, ForeignKey("JobBoard.JobBoardID"), nullable=False)
    JobTitle = Column(Unicode(255), nullable=False)
    CompanyName = Column(Unicode(255), nullable=False)
    JobDescription = Column(UnicodeText)
    Location = Column(Unicode(255))
    JobURL = Column(Unicode(500))
    JobAgeEstimate = Column(Integer)
    IsRepost = Column(Boolean, default=False)
    RepostFrequency = Column(Integer)
    UnitCount = Column(Integer, default=1)
    IsActive = Column(Boolean, default=True)
    # Contact Person Profile (nullable)
    ContactPersonProfileID = Column(Integer, ForeignKey("Profile.ProfileID"))
    ContactPersonType = Column(Unicode(50))  # 'recruiter', 'hiring_manager', 'hr_representative'
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    job_board = relationship("JobBoard")
    contact_person = relationship("Profile")

class JobBoardJobVersion(Base):
    __tablename__ = "JobBoardJobVersion"
    JobBoardJobVersionID = Column(Integer, primary_key=True, autoincrement=True)
    JobBoardJobID = Column(Integer, ForeignKey("JobBoardJob.JobBoardJobID"), nullable=False)
    VersionNumber = Column(Integer, nullable=False)
    ChangeReason = Column(Unicode(255))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    job = relationship("JobBoardJob")

class UserJobBoardJobInteraction(Base):
    __tablename__ = "UserJobBoardJobInteraction"
    UserJobBoardJobInteractionID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    JobBoardJobID = Column(Integer, ForeignKey("JobBoardJob.JobBoardJobID"), nullable=False)
    InteractionType = Column(Unicode(50))  # 'viewed', 'logged', 'applied', 'bookmarked'
    FitScore = Column(DECIMAL(5,2))
    UserNotes = Column(Unicode(1000))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    user = relationship("User")
    job = relationship("JobBoardJob")

class JobBoardJobSkill(Base):
    __tablename__ = "JobBoardJobSkill"
    JobBoardJobSkillID = Column(Integer, primary_key=True, autoincrement=True)
    JobBoardJobID = Column(Integer, ForeignKey("JobBoardJob.JobBoardJobID"), nullable=False)
    SkillName = Column(Unicode(255), nullable=False)
    SkillType = Column(Unicode(50))  # 'required', 'preferred', 'optional'
    Importance = Column(DECIMAL(3,2))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    job = relationship("JobBoardJob")

# =============================================================================
# FIT SCORE ANALYSIS SYSTEM
# =============================================================================

class UserJobBoardJobFitScore(Base):
    __tablename__ = "UserJobBoardJobFitScore"
    UserJobBoardJobFitScoreID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    JobBoardJobID = Column(Integer, ForeignKey("JobBoardJob.JobBoardJobID"), nullable=False)
    ProfileVersionID = Column(Integer, ForeignKey("ProfileVersion.ProfileVersionID"), nullable=False)
    OverallScore = Column(DECIMAL(5,2))
    SkillsMatched = Column(Integer)
    SkillsPartial = Column(Integer)
    SkillsMissing = Column(Integer)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    user = relationship("User")
    job = relationship("JobBoardJob")
    profile_version = relationship("ProfileVersion")

class UserJobBoardJobFitScoreDetail(Base):
    __tablename__ = "UserJobBoardJobFitScoreDetail"
    UserJobBoardJobFitScoreDetailID = Column(Integer, primary_key=True, autoincrement=True)
    UserJobBoardJobFitScoreID = Column(Integer, ForeignKey("UserJobBoardJobFitScore.UserJobBoardJobFitScoreID"), nullable=False)
    SkillName = Column(Unicode(255), nullable=False)
    MatchStatus = Column(Unicode(50))  # 'matched', 'partial', 'missing'
    UserSkillLevel = Column(Unicode(50))
    JobSkillRequirement = Column(Unicode(50))
    Score = Column(DECIMAL(5,2))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    fit_score = relationship("UserJobBoardJobFitScore")

class UserSkillGapResolution(Base):
    __tablename__ = "UserSkillGapResolution"
    UserSkillGapResolutionID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    SkillName = Column(Unicode(255), nullable=False)
    ResolutionType = Column(Unicode(50))  # 'added', 'confirmed', 'learning'
    ResolutionDate = Column(DateTime, default=datetime.utcnow)
    Notes = Column(Unicode(1000))
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    user = relationship("User")

# =============================================================================
# ENHANCED RESUME & ARTIFACT SYSTEM
# =============================================================================

class ResumeResumeVersion(Base):
    __tablename__ = "ResumeResumeVersion"
    ResumeResumeVersionID = Column(Integer, primary_key=True, autoincrement=True)
    ResumeID = Column(Integer, ForeignKey("Resume.ResumeID"), nullable=False)
    ProfileVersionID = Column(Integer, ForeignKey("ProfileVersion.ProfileVersionID"), nullable=False)
    JobBoardJobID = Column(Integer, ForeignKey("JobBoardJob.JobBoardJobID"))
    Content = Column(UnicodeText)  # markdown format
    Template = Column(Unicode(100))
    Tone = Column(Unicode(50))
    ExportFormat = Column(Unicode(50))  # 'PDF', 'DOCX', 'HTML'
    FileURL = Column(Unicode(500))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    resume = relationship("Resume")
    profile_version = relationship("ProfileVersion")
    job = relationship("JobBoardJob")

class CoverLetterCoverLetterVersion(Base):
    __tablename__ = "CoverLetterCoverLetterVersion"
    CoverLetterCoverLetterVersionID = Column(Integer, primary_key=True, autoincrement=True)
    CoverLetterID = Column(Integer, ForeignKey("CoverLetter.CoverLetterID"), nullable=False)
    ProfileVersionID = Column(Integer, ForeignKey("ProfileVersion.ProfileVersionID"), nullable=False)
    JobBoardJobID = Column(Integer, ForeignKey("JobBoardJob.JobBoardJobID"))
    Content = Column(UnicodeText)  # markdown format
    Tone = Column(Unicode(50))
    ExportFormat = Column(Unicode(50))
    FileURL = Column(Unicode(500))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    cover_letter = relationship("CoverLetter")
    profile_version = relationship("ProfileVersion")
    job = relationship("JobBoardJob")

class ExportTemplate(Base):
    __tablename__ = "ExportTemplate"
    ExportTemplateID = Column(Integer, primary_key=True, autoincrement=True)
    TemplateName = Column(Unicode(255), nullable=False)
    TemplateType = Column(Unicode(50))  # 'resume', 'cover-letter', 'report'
    Content = Column(UnicodeText)  # HTML/CSS template
    IsActive = Column(Boolean, default=True)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

# =============================================================================
# GAMIFICATION SYSTEM
# =============================================================================

class UserGamificationPoints(Base):
    __tablename__ = "UserGamificationPoints"
    UserGamificationPointsID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    PointsEarned = Column(Integer, nullable=False)
    PointsType = Column(Unicode(50))  # 'job_logging', 'profile_completion', 'skill_confirmation'
    Description = Column(Unicode(255))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    user = relationship("User")

class UserAchievement(Base):
    __tablename__ = "UserAchievement"
    UserAchievementID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    AchievementName = Column(Unicode(255), nullable=False)
    AchievementDescription = Column(Unicode(500))
    EarnedDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    user = relationship("User")

# =============================================================================
# NOTIFICATION SYSTEM
# =============================================================================

class UserNotification(Base):
    __tablename__ = "UserNotification"
    UserNotificationID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    NotificationType = Column(Unicode(50))
    Title = Column(Unicode(255))
    Message = Column(Unicode(1000))
    IsRead = Column(Boolean, default=False)
    IsEmailSent = Column(Boolean, default=False)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    user = relationship("User")

class UserNotificationPreference(Base):
    __tablename__ = "UserNotificationPreference"
    UserNotificationPreferenceID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    NotificationType = Column(Unicode(50))
    EmailEnabled = Column(Boolean, default=True)
    InAppEnabled = Column(Boolean, default=True)
    Frequency = Column(Unicode(50))  # 'immediate', 'daily', 'weekly'
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    user = relationship("User")

# =============================================================================
# ANALYTICS & DASHBOARD SYSTEM
# =============================================================================

class UserAnalytics(Base):
    __tablename__ = "UserAnalytics"
    UserAnalyticsID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    ProfileCompleteness = Column(DECIMAL(5,2))
    TotalJobApplications = Column(Integer)
    AverageFitScore = Column(DECIMAL(5,2))
    ResumeGeneratedCount = Column(Integer)
    LastActivityDate = Column(DateTime)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    user = relationship("User")

class UserJobBoardJobSearchAnalytics(Base):
    __tablename__ = "UserJobBoardJobSearchAnalytics"
    UserJobBoardJobSearchAnalyticsID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    JobBoardID = Column(Integer, ForeignKey("JobBoard.JobBoardID"))
    ApplicationsCount = Column(Integer)
    InterviewCount = Column(Integer)
    OfferCount = Column(Integer)
    SuccessRate = Column(DECIMAL(5,2))
    Period = Column(Unicode(20))  # 'weekly', 'monthly', 'yearly'
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    user = relationship("User")
    job_board = relationship("JobBoard")

# =============================================================================
# PRIVACY & CONSENT SYSTEM
# =============================================================================

class ProfileConsent(Base):
    __tablename__ = "ProfileConsent"
    ProfileConsentID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    ConsentType = Column(Unicode(50))  # 'contact_info', 'professional_details', 'social_media'
    IsGranted = Column(Boolean, default=False)
    GrantedTo = Column(Unicode(100))  # 'all_users', 'specific_user', 'job_applicants'
    GrantedDate = Column(DateTime)
    ExpiryDate = Column(DateTime)
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    profile = relationship("Profile")

class ProfileType(Base):
    __tablename__ = "ProfileType"
    ProfileTypeID = Column(Integer, primary_key=True, autoincrement=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"), nullable=False)
    ProfileType = Column(Unicode(50))  # 'job_seeker', 'recruiter', 'hiring_manager', 'hr_representative'
    IsVerified = Column(Boolean, default=False)
    VerificationMethod = Column(Unicode(100))
    createdDate = Column(DateTime, default=datetime.utcnow)
    createdBy = Column(Unicode(100))
    lastUpdated = Column(DateTime)
    updatedBy = Column(Unicode(100))

    profile = relationship("Profile")

# Update User model to include email relationship
User.email_addresses = relationship("UserEmailAddress", back_populates="user")
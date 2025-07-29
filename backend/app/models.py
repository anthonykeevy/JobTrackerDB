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

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, DECIMAL, Text, Unicode, UnicodeText
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
import logging
import secrets

Base = declarative_base()

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
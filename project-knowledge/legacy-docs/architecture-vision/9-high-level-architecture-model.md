# 9. High-Level Architecture Model

## Core Components

- **Frontend**: React SPA with responsive design and progressive disclosure UI
- **Backend**: FastAPI (Python) with authentication and session management
- **Database**: MSSQL (`JobTrackerDB`) with structured schema and audit logging
- **MCP Service**: Custom internal service providing centralized API interface to JobTrackerDB

## Authentication & Security Layer

- **Authentication Endpoints**: RESTful API for user registration, login, password management
- **Session Management**: Secure session handling with timeout and renewal
- **Audit Logging**: Comprehensive logging of all authentication and user events
- **Security Framework**: CSRF protection, rate limiting, account lockout, encryption

## AI & Integration Services

- **OpenAI API**: Integration with detailed logging of user and token costs
- **Email Service**: Transactional emails for verification and notifications
- **Gamification Engine**: Points tracking and achievement system

## Data & Compliance

- **Audit Trail**: Complete audit logging for security and compliance
- **Data Encryption**: AES-256 encryption at rest and in transit
- **Privacy Compliance**: GDPR and Australian privacy regulation adherence
- **Backup Strategy**: Local database backups and planned Azure migration
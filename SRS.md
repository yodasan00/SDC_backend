# Software Requirements Specification (SRS) for SDC Backend

## 1. Introduction

### 1.1 Purpose
The SDC Backend is a Django-based REST API system designed to manage IT service desk tickets. The system facilitates a structured workflow for ticket creation, approval, and resolution involving multiple user roles within an organization.

### 1.2 Scope
The system provides:
- User authentication and role-based access control
- Ticket lifecycle management (creation, approval, work assignment, completion)
- Comment system for ticket discussions
- Audit logging for all ticket status changes
- Dashboard statistics for different user roles
- System-wide reporting capabilities

### 1.3 Definitions, Acronyms, and Abbreviations
- **SDC**: Service Desk Center
- **DIT**: Department of Information Technology
- **API**: Application Programming Interface
- **JWT**: JSON Web Token
- **REST**: Representational State Transfer

## 2. Overall Description

### 2.1 Product Perspective
The SDC Backend serves as the server-side component of a web-based IT service desk management system. It provides RESTful APIs that can be consumed by frontend applications or other systems.

### 2.2 Product Functions
- User registration and authentication
- Role-based ticket management
- Multi-phase ticket workflow
- Real-time dashboard statistics
- Audit trail maintenance
- Comment management

### 2.3 User Characteristics
- **Department Users**: End-users who create and track tickets
- **DIT Approvers**: IT administrators who approve or reject tickets
- **SDC Staff**: Technical personnel who execute approved work

### 2.4 Constraints
- Built using Django 6.0.1 and Django REST Framework
- Uses PostgreSQL/MySQL database
- Requires Python 3.12+
- JWT-based authentication
- RESTful API design

## 3. Specific Requirements

### 3.1 External Interface Requirements

#### 3.1.1 User Interfaces
The system provides REST API endpoints. No direct user interfaces are included in the backend.

#### 3.1.2 Hardware Interfaces
- Standard web server hardware
- Database server (PostgreSQL/MySQL recommended)

#### 3.1.3 Software Interfaces
- Python 3.12+
- Django 6.0.1
- Django REST Framework 3.16.1
- djangorestframework-simplejwt 5.2.2
- PostgreSQL/MySQL database

#### 3.1.4 Communication Interfaces
- HTTP/HTTPS protocols
- JSON data format
- JWT token-based authentication

### 3.2 Functional Requirements

#### 3.2.1 Authentication System
**FR-1**: User Registration
- System shall allow user registration with username, email, and password
- System shall assign user roles (DEPARTMENT, DIT, SDC)

**FR-2**: User Login
- System shall authenticate users with username/password
- System shall return JWT tokens upon successful authentication

**FR-3**: Role-Based Access Control
- System shall enforce role-based permissions for all operations
- Department users: Create tickets, view own tickets
- DIT users: Approve/reject pending tickets, view all tickets
- SDC users: Work on approved tickets, complete tickets

#### 3.2.2 Ticket Management

**FR-4**: Ticket Creation
- Department users shall create tickets with title and description
- System shall set initial status to 'PENDING'
- System shall log creation in audit trail

**FR-5**: Ticket Approval Workflow
- DIT users shall view all pending tickets
- DIT users shall approve or reject pending tickets
- System shall update ticket status and log changes

**FR-6**: Ticket Execution
- SDC users shall view approved tickets
- SDC users shall start work on approved tickets (status: IN_PROGRESS)
- SDC users shall complete tickets (status: COMPLETED)
- System shall log all status changes

**FR-7**: Ticket Tracking
- Users shall view tickets based on their roles and permissions
- Department users shall view only their own tickets
- DIT/SDC users shall view tickets relevant to their workflow

#### 3.2.3 Comment System

**FR-8**: Add Comments
- Authenticated users shall add comments to tickets
- Comments shall be associated with user and timestamp

**FR-9**: View Comments
- Authenticated users shall view all comments on tickets they can access

#### 3.2.4 Audit Logging

**FR-10**: Automatic Logging
- System shall log all ticket status changes
- Logs shall include user, action, old status, new status, timestamp

**FR-11**: Audit Trail Access
- Authenticated users shall view audit logs for accessible tickets

#### 3.2.5 Dashboard and Reporting

**FR-12**: Department Dashboard
- Department users shall view statistics of their tickets by status

**FR-13**: DIT Dashboard
- DIT users shall view system-wide ticket statistics

**FR-14**: SDC Dashboard
- SDC users shall view statistics of tickets in their workflow

**FR-15**: System Reports
- DIT users shall access comprehensive system reports
- Reports shall include ticket counts by status and department

### 3.3 Non-Functional Requirements

#### 3.3.1 Performance Requirements
**NFR-1**: Response Time
- API responses shall be returned within 2 seconds for 95% of requests
- Database queries shall complete within 500ms

**NFR-2**: Concurrent Users
- System shall support up to 1000 concurrent users
- System shall handle 100 requests per second

#### 3.3.2 Security Requirements
**NFR-3**: Authentication Security
- Passwords shall be hashed using secure algorithms
- JWT tokens shall have reasonable expiration times
- System shall implement proper session management

**NFR-4**: Authorization
- All endpoints shall enforce role-based access control
- System shall prevent unauthorized access to sensitive data

**NFR-5**: Data Protection
- User data shall be encrypted in transit (HTTPS)
- Sensitive data shall be encrypted at rest
- System shall implement input validation and sanitization

#### 3.3.3 Reliability Requirements
**NFR-6**: Availability
- System shall maintain 99.5% uptime
- System shall implement proper error handling and logging

**NFR-7**: Data Integrity
- Database transactions shall maintain ACID properties
- System shall prevent data corruption

#### 3.3.4 Usability Requirements
**NFR-8**: API Usability
- API endpoints shall follow REST conventions
- Error messages shall be clear and informative
- API documentation shall be comprehensive

#### 3.3.5 Maintainability Requirements
**NFR-9**: Code Quality
- Code shall follow Django best practices
- System shall include comprehensive unit tests
- Documentation shall be maintained and up-to-date

## 4. Interface Requirements

### 4.1 API Endpoints

#### Authentication Endpoints
- POST /api/auth/login/ - User login
- POST /api/auth/register/ - User registration
- POST /api/auth/refresh/ - Token refresh

#### Ticket Management Endpoints
- POST /api/tickets/create/ - Create ticket (Department)
- GET /api/tickets/my/ - List user's tickets (Department)
- GET /api/tickets/pending/ - List pending tickets (DIT)
- POST /api/tickets/{id}/approve/ - Approve ticket (DIT)
- POST /api/tickets/{id}/reject/ - Reject ticket (DIT)
- GET /api/tickets/approved/ - List approved tickets (SDC)
- POST /api/tickets/{id}/start/ - Start work (SDC)
- POST /api/tickets/{id}/complete/ - Complete ticket (SDC)

#### Comment Endpoints
- POST /api/comments/ - Add comment
- GET /api/tickets/{id}/comments/ - List ticket comments

#### Audit Endpoints
- GET /api/tickets/{id}/audit/ - List ticket audit logs

#### Dashboard Endpoints
- GET /api/dashboard/department/ - Department statistics
- GET /api/dashboard/dit/ - DIT statistics
- GET /api/dashboard/sdc/ - SDC statistics
- GET /api/reports/system/ - System reports (DIT)

### 4.2 Data Formats
All API communication uses JSON format with the following structures:

#### Ticket Object
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "created_by": "user_object",
  "status": "string",
  "created_at": "datetime"
}
```

#### User Object
```json
{
  "id": "integer",
  "username": "string",
  "role": "string"
}
```

## 5. Assumptions and Dependencies

### 5.1 Assumptions
- Users have basic computer literacy
- Network connectivity is reliable
- Database server is properly configured
- Frontend applications will handle user interface

### 5.2 Dependencies
- Python 3.12+ runtime environment
- PostgreSQL/MySQL database server
- Web server (nginx/apache) for production deployment
- SSL certificate for HTTPS in production

## 6. Appendices

### 6.1 Ticket Status Flow
1. PENDING → APPROVED (by DIT) or REJECTED (by DIT)
2. APPROVED → IN_PROGRESS (by SDC)
3. IN_PROGRESS → COMPLETED (by SDC)

### 6.2 User Roles and Permissions
- **DEPARTMENT**: Create tickets, view own tickets, add comments
- **DIT**: View all tickets, approve/reject pending tickets, view reports
- **SDC**: View approved tickets, start/complete work, add comments

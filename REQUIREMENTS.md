# REQUIREMENTS.md

# Astrology Research CRM

## Business Requirements

---

# Project Objective

Develop a web-based Astrology Research CRM that enables astrologers and researchers to:

* Store customer birth details
* Store astrology information manually or through APIs
* Maintain a structured astrology knowledge base
* Verify predictions with customers
* Track remedies and outcomes
* Maintain consultation history
* Support collaborative research by multiple users
* Build a long-term astrology research database

The application is intended for internal research and consultation management.

It is not intended to be a public astrology prediction portal.

---

# Target Users

## Admin

Responsible for:

* Managing users
* Managing roles
* Managing access permissions
* Managing all modules

---

## Content Editor

Responsible for:

* Creating knowledge records
* Maintaining predictions
* Maintaining remedies
* Maintaining KP rules
* Maintaining BNN rules
* Maintaining case studies
* Maintaining research questions

---

## Researcher

Responsible for:

* Creating customers
* Conducting consultations
* Verifying predictions
* Tracking remedies
* Recording observations

---

## Viewer

Responsible for:

* Viewing information only

No create, edit, or delete permissions.

---

# Functional Requirements

---

# Module 1 - Authentication

## Features

* User login
* User logout
* Password change
* Session management

## Access

All authenticated users.

---

# Module 2 - Role Management

## Features

* Create role
* Edit role
* View role
* Activate role
* Deactivate role

## Example Roles

* Admin
* Content Editor
* Researcher
* Viewer

---

# Module 3 - User Management

## Features

* Create user
* Edit user
* View user
* Activate user
* Deactivate user

## User Information

* Name
* Username
* Email
* Mobile
* Role

---

# Module 4 - Customer Management

## Features

* Add customer
* Edit customer
* View customer
* Search customer
* Filter customer
* Deactivate customer

---

## Customer Information

### Personal

* Name
* Gender
* Mobile
* Email

### Birth Details

* Date of Birth
* Time of Birth
* Place of Birth
* Latitude
* Longitude
* Timezone

### Background

* Occupation
* Education
* Marital Status

### Additional

* Notes

---

# Module 5 - API Data Management

## Purpose

Store astrology information obtained from:

* Manual entry
* Astrology APIs
* Excel imports
* CSV imports

---

## Features

* Add API record
* View API record
* Edit API record
* Search API record

---

## Supported Information

* Lagna
* Moon Sign
* Sun Sign
* Nakshatra
* Pada
* Current Mahadasha
* Current Antardasha

---

## Future Support

* Divisional Charts
* KP Data
* Ashtakavarga
* Transit Data
* Compatibility Data

---

# Module 6 - Category Management

## Purpose

Manage categories used in Astrology Knowledge Base.

---

## Features

* Add category
* Edit category
* View category
* Activate category
* Deactivate category

---

## Example Categories

* Nakshatra
* Nakshatra Pada
* Dosha
* Remedy
* KP
* BNN
* Arudha
* Dasha
* Transit
* Research
* Case Study

---

# Module 7 - Astrology Knowledge Base

## Purpose

Store all astrology knowledge in a single flexible repository.

---

## Knowledge Types

* Prediction
* Remedy
* Rule
* Observation
* Question
* Note

---

## Sections

* Nakshatra
* Nakshatra Pada
* Dosha
* Planet in House
* Planet in Nakshatra
* Planet in Sign
* Arudha Lagna
* KP
* BNN
* Dasha
* Transit
* Research
* Case Study

---

## Features

* Add knowledge
* Edit knowledge
* View knowledge
* Search knowledge
* Filter knowledge
* Activate knowledge
* Deactivate knowledge

---

## Examples

### Prediction

Ardra natives may enjoy research and investigation.

---

### Remedy

Recite Hanuman Chalisa daily.

---

### KP Rule

2-7-11 house connection may indicate marriage.

---

### BNN Rule

Jupiter-Saturn combination may indicate delayed success.

---

# Module 8 - Customer Knowledge Tracking

## Purpose

Track how knowledge applies to specific customers.

---

## Supported Tracking Types

### Prediction Verification

Determine whether a prediction applies.

### Remedy Tracking

Track remedy effectiveness.

### Research Answers

Collect answers to research questions.

### Observations

Record special observations.

---

## Features

* Add tracking record
* Edit tracking record
* View tracking record
* Search tracking record

---

## Prediction Status

* Applies
* Partially Applies
* Does Not Apply
* Not Asked

---

## Remedy Status

* Suggested
* Started
* In Progress
* Completed
* Stopped

---

## Effectiveness Rating

Scale:

1 to 10

---

## Outcome Types

* Very Effective
* Effective
* Partial
* No Effect
* Negative Effect

---

# Module 9 - Consultation Notes

## Purpose

Maintain consultation history.

---

## Features

* Add consultation note
* Edit consultation note
* View consultation note
* Search consultation note

---

## Consultation Information

* Consultation Date
* Topic
* Notes
* Follow-up Required
* Follow-up Date

---

# Module 10 - Dashboard

## Purpose

Provide a quick summary of system activity.

---

## Dashboard Cards

* Total Customers
* Total Knowledge Records
* Total Verifications
* Total Remedies Tracked
* Total Consultations

---

## Dashboard Widgets

### Recent Customers

Show latest customers added.

### Recent Consultations

Show latest consultations.

### Recent Verifications

Show latest prediction verifications.

### Recent Remedies

Show latest remedy tracking entries.

---

# Search Requirements

System should support searching by:

* Customer Name
* Mobile Number
* Nakshatra
* Pada
* Occupation
* Education
* Knowledge Title
* Category
* Section
* Knowledge Type

---

# Reporting Requirements

Phase 1 Reports

### Customer Report

List all customers.

### Knowledge Report

List all knowledge records.

### Prediction Verification Report

Show verification statistics.

### Remedy Effectiveness Report

Show remedy outcome statistics.

### Consultation Report

Show consultation history.

---

# Non-Functional Requirements

## Performance

* Fast page load
* Optimized queries
* Suitable for thousands of customers

---

## Security

* Login required
* Role-based access control
* User activity tracking

---

## Maintainability

* Clean Django structure
* Modular code
* Clear naming conventions

---

## Scalability

Future support should be possible for:

* Astrology APIs
* AI Research Assistant
* Advanced Reporting
* D9 Charts
* KP Modules
* BNN Modules
* Mobile Application

---

# Out of Scope for MVP

Do NOT implement:

* Horoscope chart generation
* Planetary calculations
* Ephemeris calculations
* Automated prediction generation
* PDF report generation
* Payment gateway
* Customer self-registration

These may be added in future phases.

---

# Success Criteria

The system is considered successful when:

1. Researchers can store customers easily.
2. Knowledge can be maintained without database changes.
3. Predictions can be verified systematically.
4. Remedies can be tracked and evaluated.
5. Multiple team members can collaborate.
6. Astrology APIs can be integrated later without redesigning the database.
7. Long-term astrology research becomes possible.

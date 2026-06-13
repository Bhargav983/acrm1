# PROJECT_PLAN.md

# Astrology Research CRM

## Project Vision

Build a maintainable Astrology Research CRM that allows astrologers and researchers to:

* Store customer birth details
* Maintain astrology knowledge
* Verify predictions
* Track remedies
* Record consultations
* Build a long-term astrology research database

The system should support thousands of customers and years of research without requiring database redesign.

---

# Project Philosophy

This project is NOT:

* A horoscope generation website
* A kundali generation system
* A prediction portal
* A public astrology platform

This project IS:

* A research CRM
* A knowledge management system
* A prediction verification platform
* A remedy effectiveness tracker

---

# MVP Goal

The first version must allow a researcher to:

1. Add a customer
2. Enter birth details
3. Enter astrology details manually or through API data
4. View matching knowledge records
5. Verify predictions
6. Assign remedies
7. Track outcomes
8. Record consultation notes

If these activities work smoothly, the MVP is successful.

---

# Development Strategy

Build from the inside out.

Order:

1. Database
2. Authentication
3. Masters
4. Transactions
5. Dashboard
6. Reports
7. UI Improvements

Never start with fancy UI.

Always start with working data structures.

---

# Phase 1 - Project Setup

## Objective

Create a clean Django foundation.

## Tasks

### Environment Setup

* Create Django project
* Create virtual environment
* Configure settings
* Configure SQLite

### Applications

Create apps:

* accounts
* customers
* knowledge
* consultations
* core

### Common Setup

* Bootstrap 5
* Base template
* Navigation
* Sidebar
* Login page

## Deliverable

User can access the application and log in.

---

# Phase 2 - Authentication & Roles

## Objective

Secure the application.

## Tasks

### Role Master

* Create role model
* Create role CRUD

### User Master

* Create user model
* Create user CRUD

### Authentication

* Login
* Logout
* Password change

### Permissions

Implement:

* Admin
* Content Editor
* Researcher
* Viewer

## Deliverable

Role-based access works correctly.

---

# Phase 3 - Customer Management

## Objective

Manage customers and birth details.

## Tasks

### Customer Master

Create:

* Model
* Forms
* List page
* Add page
* Edit page
* View page

### Features

* Search customer
* Filter customer
* Active / Inactive

## Deliverable

Researchers can manage customers.

---

# Phase 4 - API Data Management

## Objective

Prepare for future astrology API integrations.

## Tasks

### API Data Master

Create:

* Model
* CRUD
* Search

### Support

* Manual Entry
* API Entry
* Excel Import
* CSV Import

## Deliverable

Astrology information can be stored independently from customer records.

---

# Phase 5 - Category Management

## Objective

Create flexible classification structure.

## Tasks

### Category Master

Create:

* Model
* CRUD
* Search

### Seed Categories

* Nakshatra
* Nakshatra Pada
* Dosha
* Remedy
* KP
* BNN
* Arudha
* Research
* Case Study

## Deliverable

Categories can be managed dynamically.

---

# Phase 6 - Astrology Knowledge Base

## Objective

Build the heart of the system.

## Tasks

### Knowledge Base

Create:

* Model
* CRUD
* Search
* Filters

### Supported Knowledge

* Predictions
* Remedies
* KP Rules
* BNN Rules
* Observations
* Questions
* Notes

### Filters

* Category
* Section
* Knowledge Type
* Applies To Type
* Applies To Name

## Deliverable

Knowledge repository is fully functional.

---

# Phase 7 - Customer Knowledge Tracking

## Objective

Track how knowledge applies to customers.

## Tasks

### Tracking Module

Create:

* Model
* CRUD
* Search

### Prediction Verification

Support:

* Applies
* Partially Applies
* Does Not Apply
* Not Asked

### Remedy Tracking

Support:

* Suggested
* Started
* In Progress
* Completed
* Stopped

### Effectiveness Tracking

Support:

* Rating 1-10
* Outcome

## Deliverable

Researchers can verify predictions and track remedies.

---

# Phase 8 - Consultation Notes

## Objective

Store consultation history.

## Tasks

### Consultation Notes

Create:

* Model
* CRUD
* Search

### Features

* Consultation Date
* Topic
* Notes
* Follow-up Date

## Deliverable

Consultation history is maintained.

---

# Phase 9 - Dashboard

## Objective

Provide operational visibility.

## Dashboard Cards

* Total Customers
* Total Knowledge Records
* Total Verifications
* Total Remedies
* Total Consultations

## Dashboard Widgets

### Recent Customers

Latest customer records.

### Recent Consultations

Latest consultation records.

### Recent Verifications

Latest verification records.

### Recent Remedies

Latest remedy tracking records.

## Deliverable

Useful operational dashboard.

---

# Phase 10 - Reports

## Objective

Provide research insights.

## Reports

### Customer Report

All customers.

### Knowledge Report

All knowledge records.

### Verification Report

Prediction verification statistics.

### Remedy Report

Remedy effectiveness statistics.

### Consultation Report

Consultation history.

## Deliverable

Basic reporting available.

---

# Phase 11 - Seed Data

## Objective

Make the system usable immediately.

## Create Sample Data

### Roles

* Admin
* Content Editor
* Researcher
* Viewer

### Categories

All default categories.

### Knowledge Records

At least:

* 20 Predictions
* 10 Remedies
* 10 KP Rules
* 10 BNN Rules
* 10 Research Questions

### Customers

10 Sample Customers

## Deliverable

System can be demonstrated without manual data entry.

---

# Future Phase 2

## Research Intelligence

Add:

* Pattern Analysis
* Prediction Accuracy Reports
* Remedy Effectiveness Reports
* Category Analysis

---

# Future Phase 3

## Astrology API Integration

Support:

* Birth Chart APIs
* Dasha APIs
* Transit APIs
* KP APIs

Automatic population of API Data Master.

---

# Future Phase 4

## AI Research Assistant

Examples:

* Show common traits among Ardra natives.
* Show successful remedies for Kuja Dosha.
* Show common marriage patterns for Rohini natives.
* Show prediction accuracy by category.

---

# Definition of Success

The project is successful when:

* Customer data is organized.
* Knowledge is centralized.
* Predictions can be verified.
* Remedies can be tracked.
* Multiple researchers can collaborate.
* Future APIs can be integrated without redesign.
* Long-term astrology research becomes practical.

---

# Build Order Rule

Always complete the previous phase before starting the next phase.

Do not skip phases.

Do not build advanced features before the MVP is stable.

Database integrity and usability are more important than visual design.

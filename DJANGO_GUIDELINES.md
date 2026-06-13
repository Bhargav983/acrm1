# DJANGO_GUIDELINES.md

# Astrology Research CRM - Django Guidelines

## Purpose

This document defines Django development rules for the Astrology Research CRM.

The goal is to help Codex, Claude Code, Cursor, or any AI coding assistant build the project in a clean and maintainable way.

---

# Tech Stack

## Backend

* Python 3.12+
* Django 5.x

## Database

* SQLite for MVP
* PostgreSQL later if needed

## Frontend

* Django Templates
* Bootstrap 5
* HTML
* CSS
* Minimal JavaScript only when needed

Do not use:

* React
* Vue
* Angular
* Next.js
* DRF unless specifically requested later

---

# Recommended Django Apps

Create these apps:

```text
accounts
customers
knowledge
consultations
core
```

---

# App Responsibilities

## accounts

Handles:

* Login
* Logout
* User Master
* Role Master
* Role-based permissions

## customers

Handles:

* Customer Master
* API Data Master

## knowledge

Handles:

* Category Master
* Astrology Knowledge Base
* Customer Knowledge Tracking

## consultations

Handles:

* Consultation Notes

## core

Handles:

* Dashboard
* Base templates
* Shared utilities

---

# Model Rules

Follow `DATA_MODEL.md`.

Do not create extra tables without approval.

Use clear model names:

* Role
* User
* Customer
* Category
* AstrologyKnowledge
* CustomerKnowledgeTracking
* ConsultationNote
* APIData

---

# Field Rules

Use simple Django field types.

Examples:

* CharField for names and labels
* TextField for notes and descriptions
* DateField for dates
* DateTimeField for audit timestamps
* BooleanField for active status
* ForeignKey for relationships
* PositiveSmallIntegerField for ratings

---

# Audit Fields

Where useful, add:

* created_at
* updated_at
* created_by
* updated_by
* is_active

Prefer these names consistently.

---

# Soft Delete Rule

Do not hard delete important records.

Use:

```text
is_active = False
```

for:

* Customers
* Knowledge records
* Categories
* Roles
* Users

---

# Authentication Rules

Use Django authentication system.

All main pages require login.

Unauthenticated users must be redirected to login.

---

# Role Rules

Roles:

* Admin
* Content Editor
* Researcher
* Viewer

## Admin

Full access.

## Content Editor

Can manage:

* Category Master
* Astrology Knowledge Base

Can view:

* Customers
* Tracking
* Consultations

## Researcher

Can manage:

* Customers
* Customer Knowledge Tracking
* Consultation Notes

Can view:

* Knowledge Base

## Viewer

Read-only access.

---

# Permission Implementation

For MVP, keep permission implementation simple.

Do not over-engineer permissions.

Use helper functions or mixins such as:

* is_admin
* is_content_editor
* is_researcher
* is_viewer

Later this can be upgraded to granular permissions.

---

# View Rules

Use simple Django views.

Function-based views are acceptable.

Class-based views are also acceptable, but stay consistent.

Every CRUD module should have:

* list view
* detail view
* create view
* update view
* deactivate view

Avoid hard delete views unless explicitly required.

---

# URL Rules

Each app should have its own `urls.py`.

Use namespaces.

Example:

```text
customers:list
customers:create
customers:detail
customers:update
```

---

# Template Rules

Use a shared base template.

Recommended structure:

```text
templates/
  base.html
  dashboard.html

  accounts/
  customers/
  knowledge/
  consultations/
```

Use Bootstrap 5.

Pages should be clean, professional, and easy to use.

Do not create horoscope-style decorative UI.

This is a CRM and research tool.

---

# Form Rules

Use Django forms or ModelForms.

Each form should:

* Validate required fields
* Show useful error messages
* Use Bootstrap classes
* Be simple and fast to fill

Avoid overly long forms where possible.

---

# Search and Filter Rules

List pages should support simple search.

Priority search fields:

## Customers

* Customer Name
* Mobile Number
* Nakshatra
* Pada
* Occupation
* Education

## Knowledge

* Title
* Category
* Section
* Knowledge Type
* Applies To Name
* Related Factor

## Tracking

* Customer
* Knowledge
* Tracking Type
* Status

---

# Dashboard Rules

Dashboard should show:

* Total Customers
* Total Knowledge Records
* Total Verifications
* Total Remedies Tracked
* Total Consultations

Also show recent records.

Do not overbuild charts in MVP.

---

# API Data Rules

API Data Master must support both manual and future API records.

Do not hardcode any astrology API provider.

Store:

* data source
* API provider
* API type
* request parameters
* raw response
* parsed response
* searchable astrology summary

---

# Astrology Rules

Do not implement astrology calculations.

Do not calculate:

* Lagna
* Nakshatra
* Dasha
* Transit
* Divisional charts
* Ashtakavarga
* KP cusps

These may come from APIs later.

For MVP, data is manually entered or stored from imported/API source.

---

# Knowledge Base Rules

All astrology content must go into Astrology Knowledge Base.

Do not create separate tables for:

* Nakshatra Prediction
* Pada Prediction
* Dosha Prediction
* Remedy
* KP Rule
* BNN Rule
* Past Life Observation

Use fields:

* category
* section
* knowledge_type
* applies_to_type
* applies_to_name
* applies_to_subtype
* related_factor

---

# Customer Tracking Rules

All customer-specific verification goes into Customer Knowledge Tracking.

Do not create separate tables for:

* Prediction Verification
* Remedy Tracking
* Research Answers
* Observations

Use tracking_type to separate the purpose.

---

# Seed Data Rules

Create seed data for:

* Roles
* Categories
* Sample knowledge records
* Sample customers

Seed data should allow demo without manual setup.

---

# Migration Rules

Before running migrations:

* Check model names
* Check field names
* Check relationships
* Check duplicate fields

Keep migrations clean.

Do not create unnecessary migration churn.

---

# Admin Panel Rules

Register all main models in Django Admin:

* Role
* User
* Customer
* Category
* AstrologyKnowledge
* CustomerKnowledgeTracking
* ConsultationNote
* APIData

Admin should be useful for debugging and data correction.

---

# Error Handling

Show friendly messages.

Use Django messages framework for:

* Create success
* Update success
* Deactivate success
* Permission denied
* Validation errors

---

# Code Style

Use:

* Clear names
* Small functions
* Reusable helpers
* Consistent formatting

Avoid:

* Long views
* Duplicated query logic
* Hardcoded values spread everywhere

---

# Testing Checklist

Before considering a module complete:

* List page works
* Add page works
* Edit page works
* Detail page works
* Deactivate works
* Search works
* Permission works
* Form validation works

---

# Out of Scope for MVP

Do not implement:

* Horoscope generation
* Chart drawing
* PDF reports
* Payment gateway
* Customer self-login
* Public website
* AI chatbot
* WhatsApp integration

---

# Development Order

Follow this order:

1. Project setup
2. Authentication
3. Roles and users
4. Customer module
5. API Data module
6. Category module
7. Astrology Knowledge Base
8. Customer Knowledge Tracking
9. Consultation Notes
10. Dashboard
11. Reports
12. UI polish

Do not skip steps.

---

# Final Goal

Build a clean, working Django MVP that is easy to extend.

The system should support real consultation workflow and long-term astrology research.

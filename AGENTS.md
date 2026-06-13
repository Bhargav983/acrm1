# AGENTS.md

# Astrology Research CRM

## Project Overview

Astrology Research CRM is a Django-based application designed for astrology research, consultation management, prediction verification, remedy tracking, and long-term pattern discovery.

This system is NOT an astrology calculation engine.

The purpose is to:

* Store customer birth details
* Store astrology information manually or through APIs
* Maintain an astrology knowledge base
* Verify predictions with real customers
* Track remedies and outcomes
* Build a long-term astrology research database

---

# Before Writing Any Code

You MUST read the following files in this order:

1. DATA_MODEL.md
2. REQUIREMENTS.md
3. PROJECT_PLAN.md
4. DJANGO_GUIDELINES.md
5. UI_FLOW.md

Do not start coding until these files are understood.

---

# Core Principle

This is a Research CRM.

The goal is NOT:

* Horoscope generation
* Fancy astrology reports
* PDF report generation
* Automated future prediction

The goal IS:

* Data collection
* Research
* Verification
* Pattern discovery

---

# Development Philosophy

Prefer:

* Simple
* Maintainable
* Readable
* Modular

Avoid:

* Over-engineering
* Unnecessary abstractions
* Complex architectures
* Premature optimization

---

# Technology Stack

## Backend

* Django 5.x
* Python 3.12+

## Database

* SQLite for MVP

Future:

* PostgreSQL

## Frontend

* Django Templates
* Bootstrap 5

Do NOT use React, Vue, Angular, or Next.js.

---

# Django Application Structure

Create these Django apps:

accounts
customers
knowledge
consultations
core

---

# Responsibilities

## accounts

Handles:

* Login
* Logout
* Users
* Roles
* Permissions

---

## customers

Handles:

* Customer Master
* API Data Master

---

## knowledge

Handles:

* Category Master
* Astrology Knowledge Base
* Customer Knowledge Tracking

---

## consultations

Handles:

* Consultation Notes

---

## core

Handles:

* Dashboard
* Common utilities
* Home page

---

# Database Rules

Follow DATA_MODEL.md exactly.

Do not create additional tables unless explicitly requested.

Keep the schema simple.

Avoid unnecessary normalization.

---

# Astrology Rules

The application must support:

* Nakshatra research
* Pada research
* Dosha research
* Remedy tracking
* KP research
* BNN research
* Arudha research
* Planet in House research
* Planet in Nakshatra research
* Case studies

All of these must use the Astrology Knowledge Base table.

Do not create separate tables for each concept.

---

# Knowledge Base Rules

The Astrology Knowledge Base is the most important table.

Everything must be stored there:

* Predictions
* Remedies
* Rules
* Observations
* Questions
* Notes

Future concepts should be added through records, not new tables.

---

# API Integration Rules

The system must be API-ready.

Do not hardcode any astrology API.

Store all API responses inside API Data Master.

Support:

* Manual entry
* API data
* Excel import
* CSV import

Future APIs should work without database redesign.

---

# UI Guidelines

Design should feel like:

* CRM
* Research platform
* Internal business application

Not:

* Horoscope website
* Public astrology portal

---

# Dashboard Requirements

Dashboard should show:

* Total Customers
* Total Knowledge Records
* Total Verifications
* Total Remedies Tracked
* Recent Consultations

---

# CRUD Rules

Every master should have:

* List Page
* Add Page
* Edit Page
* View Page

Delete should be soft delete whenever possible.

Use Active/Inactive status.

---

# Forms

Forms should be:

* Simple
* Fast
* Mobile friendly
* Bootstrap based

Avoid long complicated screens.

---

# Permissions

Roles:

* Admin
* Content Editor
* Researcher
* Viewer

Admin:

* Full access

Content Editor:

* Manage knowledge records

Researcher:

* Manage customers
* Manage verification
* Manage consultations

Viewer:

* Read only

---

# Coding Standards

Use:

* Meaningful model names
* Meaningful field names
* Django best practices
* Clear comments where necessary

Avoid:

* Magic values
* Duplicate code
* Unused code

---

# Migration Rules

Before creating migrations:

* Verify model structure
* Verify relationships

Keep migrations clean.

---

# Testing Rules

Before marking a task complete:

Verify:

* Create works
* Edit works
* View works
* Permissions work
* Validation works

---

# Documentation Rules

Whenever a major module is created:

Update:

* README.md
* PROJECT_PLAN.md (progress section)

---

# Important Restriction

Do NOT implement:

* Astrology calculation engine
* Horoscope chart generation
* Planetary calculations
* Dasha calculations
* Ephemeris calculations

Those may come from APIs later.

Store and manage data only.

---

# Expected Outcome

Build a maintainable Astrology Research CRM that can support thousands of customers and years of astrology research while remaining simple to maintain and easy to extend.

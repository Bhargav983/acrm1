# DATA_MODEL.md

# Astrology Research CRM

## Purpose

Astrology Research CRM is designed to collect, organize, verify, and research astrology knowledge.

The system is NOT an astrology calculation engine.

The system stores:

* Customer birth details
* Astrology details entered manually or fetched from APIs
* Predictions
* Remedies
* KP Rules
* BNN Rules
* Past-Life Observations
* Research Questions
* Case Studies
* Verification results
* Consultation history

The primary goal is long-term astrology research and pattern discovery.

---

# Final MVP Tables

1. Role Master
2. User Master
3. Customer Master
4. Category Master
5. Astrology Knowledge Base
6. Customer Knowledge Tracking
7. Consultation Notes
8. API Data Master

---

# 1. Role Master

## Purpose

Stores user roles and permissions.

## Fields

* Role ID
* Role Name
* Description
* Can View
* Can Add
* Can Edit
* Can Delete
* Active
* Created Date
* Updated Date

## Example Roles

* Admin
* Researcher
* Content Editor
* Viewer

---

# 2. User Master

## Purpose

Stores users who can log in.

## Fields

* User ID
* Full Name
* Username
* Email
* Mobile Number
* Role
* Password
* Active
* Last Login
* Created Date
* Updated Date

---

# 3. Customer Master

## Purpose

Stores customer details and birth information.

## Fields

### Personal Information

* Customer ID
* Customer Name
* Gender
* Mobile Number
* Email

### Birth Information

* Date of Birth
* Time of Birth
* Place of Birth
* Latitude
* Longitude
* Timezone

### Background Information

* Occupation
* Education
* Marital Status

### Other

* Notes
* Active
* Created By
* Created Date
* Updated By
* Updated Date

## Notes

Customer Master stores only customer information.

Astrology calculations are stored separately.

---

# 4. Category Master

## Purpose

Stores categories used by the Astrology Knowledge Base.

## Fields

* Category ID
* Category Name
* Description
* Active
* Created Date
* Updated Date

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
* Planet in House
* Planet in Nakshatra
* Planet in Sign
* Past Life
* Research
* Case Study
* Career
* Marriage
* Health
* Finance
* Spiritual
* Personality

---

# 5. Astrology Knowledge Base

## Purpose

Main knowledge repository.

Stores all astrology knowledge.

No separate tables are required for predictions, remedies, KP rules, BNN rules, etc.

## Fields

### Basic

* Knowledge ID
* Category
* Section
* Knowledge Type

### Astrology Mapping

* Applies To Type
* Applies To Name
* Applies To Subtype
* Related Factor

### Content

* Title
* Description
* Verification Question
* Expected Result

### Classification

* Nature
* Confidence Level

### Status

* Active
* Created By
* Created Date
* Updated By
* Updated Date

---

## Section Examples

* Nakshatra
* Nakshatra Pada
* Dosha
* Planet in House
* Planet in Nakshatra
* Planet in Sign
* Arudha Lagna
* Dasha
* Transit
* KP
* BNN
* Past Life
* Remedy
* Research
* Case Study

---

## Knowledge Type Examples

* Prediction
* Remedy
* Rule
* Observation
* Question
* Note

---

## Applies To Type Examples

* Nakshatra
* Pada
* Dosha
* Planet
* House
* Sign
* Planet Combination
* Arudha
* Dasha
* Transit
* General

---

## Applies To Name Examples

* Ardra
* Rohini
* Moola
* Kuja Dosha
* Sade Sati
* Saturn
* Jupiter
* 7th House
* Gemini
* AL
* Jupiter Saturn

---

## Applies To Subtype Examples

* Pada 1
* Pada 2
* Pada 3
* Pada 4
* High Severity
* Medium Severity
* Low Severity
* 7th House
* 10th House

---

## Related Factor Examples

* Career
* Marriage
* Health
* Finance
* Education
* Spirituality
* Family
* Children
* Business
* Foreign Travel

---

## Nature Values

* Positive
* Negative
* Neutral
* Remedy

---

# 6. Customer Knowledge Tracking

## Purpose

Stores customer-specific verification and tracking.

This table handles:

* Prediction Verification
* Remedy Tracking
* Research Answers
* Observations

## Fields

### Basic

* Tracking ID
* Customer
* Knowledge
* Tracking Type

### Status

* Status

### Feedback

* Customer Feedback
* Researcher Notes

### Dates

* Start Date
* End Date
* Follow-up Date

### Results

* Effectiveness Rating
* Outcome

### Audit

* Verified By
* Verified Date
* Created Date
* Updated Date

---

## Tracking Type Examples

* Prediction Verification
* Remedy Tracking
* Research Answer
* Observation

---

## Status Examples

### Prediction Verification

* Applies
* Partially Applies
* Does Not Apply
* Not Asked

### Remedy Tracking

* Suggested
* Started
* In Progress
* Completed
* Stopped

### Research Questions

* Answered
* Not Answered
* Needs Follow-up

---

## Outcome Examples

* Very Effective
* Effective
* Partial
* No Effect
* Negative Effect
* Not Applicable

---

## Effectiveness Rating

Scale:

1 to 10

---

# 7. Consultation Notes

## Purpose

Stores consultation history.

## Fields

* Note ID
* Customer
* Consultation Date
* Topic
* Notes
* Follow-up Required
* Follow-up Date
* Created By
* Created Date
* Updated Date

## Example Topics

* Career
* Marriage
* Health
* Finance
* Education
* Spiritual Guidance
* General Consultation

---

# 8. API Data Master

## Purpose

Stores astrology data received from APIs or manual imports.

This table makes the system future-ready.

## Fields

### Basic

* API Data ID
* Customer
* Data Source

### Provider Information

* API Provider
* API Name
* API Type

### Request Information

* Request Date
* Request Parameters

### Searchable Astrology Summary

* Lagna

* Moon Sign

* Sun Sign

* Nakshatra

* Pada

* Current Mahadasha

* Current Antardasha

### Storage

* Raw API Response
* Parsed Response
* Notes

### Status

* Active
* Created Date
* Updated Date

---

## Data Source Examples

* Manual
* API
* Imported Excel
* Imported CSV
* Imported Software

---

## API Type Examples

* Birth Chart
* Dasha
* Transit
* KP
* Ashtakavarga
* Compatibility
* Divisional Charts

---

# Design Principles

## 1. Research First

The system is built for research and verification.

Not for automated prediction generation.

---

## 2. Fewer Tables

The system intentionally uses only 8 core tables.

---

## 3. Flexible Knowledge Storage

All astrology concepts are stored in Astrology Knowledge Base.

No additional tables are required when adding:

* KP
* BNN
* Jaimini
* Dasha Rules
* Transit Rules
* Planet Combinations
* Arudha Rules
* Case Studies

---

## 4. API Ready

Astrology APIs can be integrated later without changing the database design.

---

## 5. Long-Term Goal

Build a proprietary astrology research database capable of discovering repeatable patterns across:

* Nakshatras
* Padas
* Doshas
* Planets
* Houses
* Dasha Periods
* Remedies
* Real-life outcomes

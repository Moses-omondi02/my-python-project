# my-python-project
A command-line application for managing voter registrations with SQLite database storage, built with Python, SQLAlchemy, and Click.

## Project Structure

voters/
├── cli.py              # Main CLI application using Click
├── database.py         # Database configuration and connection management
├── models.py           # SQLAlchemy ORM models (Voter, VoterAddress, VoterLoginCredentials)
├── utils.py            # Utility functions (validation, formatting, data creation)
├── README.md           # This file
└── voter_registration.db # SQLite database (created automatically)

## Features

- Voter registration with complete personal information
- Address management for each voter
- Input validation (dates, country codes, required fields)
- Database persistence with SQLAlchemy ORM
- Search, list, and delete voter functionality
- Tabular display of voter data
- Relationship management between voters and addresses

## Database Schema

1. **voters** - Core voter information
   - `voter_id` (UUID primary key)
   - `national_id_number` (Unique identifier)
   - Personal details (name, title, date of birth)
   - Registration timestamp

2. **voter_address** - Voter address details
   - `address_id` (Auto-incrementing primary key)
   - Complete address fields (street, ward, subcounty, county, postal code, country)
   - Foreign key relationship to voters

## Installation

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd voters

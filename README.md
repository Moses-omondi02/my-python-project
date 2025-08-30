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

## Function Workflow

### register-voter command
- Prompts for national ID, personal details, and address information
- Validates date format, country codes, and required fields
- Creates Voter and VoterAddress records in database
- Returns success message with voter summary

### find-voter command  
- Searches by national ID using SQLAlchemy queries
- Displays formatted voter information using `format_voter_info()`
- Shows associated address if available using `format_address_info()`

### list-voters command
- Retrieves all voters using SQLAlchemy ORM
- Displays in tabular format using `display_voters_table()`
- Shows total count of registered voters

### delete-voter command
- Finds voter by national ID
- Deletes associated address records first (cascade)
- Removes voter record after confirmation

## Validation Rules

- **National ID**: Minimum 5 characters (`validate_national_id`)
- **Date of Birth**: YYYY-MM-DD format, must be 18+ years old (`validate_dob`)  
- **Country Code**: 2-letter ISO code (`validate_country_code`)
- **Names**: Non-empty with whitespace trimming (`validate_name`)
- **Address**: All fields required (`validate_address_data`)

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

## Usage 
python cli.py init_db_command    # Initialize database
python cli.py register-voter     # Register new voter
python cli.py find-voter         # Find voter by ID
python cli.py list-voters        # List all voters
python cli.py delete-voter       # Delete voter by ID

## Installation

1. **Clone the repository**:
```bash
git clone <https://github.com/Moses-omondi02/my-python-project>
cd voters



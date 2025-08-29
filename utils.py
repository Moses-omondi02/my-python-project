from datetime import datetime, date
from typing import Dict, List, Tuple, Optional, Callable
from tabulate import tabulate

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_country_code(country: str) -> bool:
    return len(country) == 2 and country.isalpha()

def get_validated_input(prompt: str, validation_func: Optional[Callable] = None, error_msg: str = "Invalid input") -> str:
    while True:
        try:
            value = input(prompt).strip()
            if validation_func and not validation_func(value):
                raise ValueError(error_msg)
            return value
        except ValueError as e:
            print(f"Error: {e}")

def format_voter_info(voter) -> str:
    voter_data: Dict = {
        'voter_id': voter.voter_id,
        'name': f"{voter.first_name} {voter.last_name}",
        'national_id': voter.national_id_number,
        'dob': voter.date_of_birth,
        'registered': voter.registration_date
    }
    
    lines: List[str] = [
        "Voter Information:",
        f"  ID: {voter_data['voter_id']}",
        f"  Name: {voter_data['name']}",
        f"  National ID: {voter_data['national_id']}",
        f"  Date of Birth: {voter_data['dob']}",
        f"  Registered: {voter_data['registered']}"
    ]
    return "\n".join(lines)

def format_address_info(address) -> str:
    address_data: Dict = {
        'type': address.address_type,
        'address': address.address_line_1,
        'ward': address.ward,
        'county': address.county,
        'postal': address.postal_code,
        'country': address.country
    }
    
    lines: List[str] = [
        f"  {address_data['type']} Address:",
        f"    {address_data['address']}",
        f"    {address_data['ward']}, {address_data['county']}",
        f"    {address_data['postal']}, {address_data['country']}"
    ]
    return "\n".join(lines)

def create_voter_dict(national_id: str, title: str, first_name: str, middle_name: str, 
                     last_name: str, dob: date) -> Dict:
    return {
        'national_id_number': national_id,
        'title': title,
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'date_of_birth': dob
    }

def validate_address_data(address_line_1, ward, subcounty, county, postal_code, country, address_type):
    """Validate address data"""
    errors = []
    
    if not address_line_1 or len(address_line_1.strip()) < 5:
        errors.append("Address line 1 must be at least 5 characters")
    
    if not ward or len(ward.strip()) == 0:
        errors.append("Ward is required")
    
    if not subcounty or len(subcounty.strip()) == 0:
        errors.append("Subcounty is required")
    
    if not county or len(county.strip()) == 0:
        errors.append("County is required")
    
    if not postal_code or len(postal_code.strip()) == 0:
        errors.append("Postal code is required")
    
    if not validate_country_code(country):
        errors.append("Country must be a valid 2-letter code")
    
    if not address_type or len(address_type.strip()) == 0:
        errors.append("Address type is required")
    
    return errors

def create_address_dict(voter_id, address_line_1, ward, subcounty, county, postal_code, country, address_type):
    """Create an address dictionary from input data"""
    return {
        'voter_id': voter_id,
        'address_line_1': address_line_1,
        'ward': ward,
        'subcounty': subcounty,
        'county': county,
        'postal_code': postal_code,
        'country': country.upper(),
        'address_type': address_type
    }

def display_voters_table(voters):
    """Display voters in a table format"""
    if not voters:
        print("No voters found.")
        return
    
    table_data = []
    for voter in voters:
        table_data.append([
            voter.national_id_number,
            f"{voter.first_name} {voter.last_name}",
            voter.date_of_birth,
            voter.registration_date.strftime("%Y-%m-%d %H:%M")
        ])
    
    headers = ["National ID", "Name", "Date of Birth", "Registered On"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
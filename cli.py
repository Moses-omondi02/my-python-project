
import click
from datetime import datetime
from typing import List, Dict, Optional
from database import get_db, init_db, drop_db  
from models import Voter, VoterAddress  
from utils import validate_date, validate_country_code, format_voter_info, format_address_info, create_voter_dict, display_voters_table, validate_address_data, create_address_dict  
from sqlalchemy.orm import Session
from tabulate import tabulate

@click.group()
def cli():
    """Voter Registration System CLI - Manage voter registrations"""
    pass


@cli.command()
def init_db_command():  
    """Initialize the database tables"""
    init_db()  
    click.echo("Database tables created successfully!")

@cli.command()
def drop_db_command():  
    """Drop all database tables"""
    if click.confirm('Are you sure you want to drop all tables? This cannot be undone!'):
        drop_db()  
        click.echo("Database dropped successfully!")


@cli.command()
@click.option('--national-id', prompt='National ID Number', help='National identification number')
@click.option('--title', prompt='Title (Mr/Mrs/Ms/Dr)', default='', help='Title of the voter')
@click.option('--first-name', prompt='First Name', help='First name of the voter')
@click.option('--middle-name', prompt='Middle Name', default='', help='Middle name of the voter')
@click.option('--last-name', prompt='Last Name', help='Last name of the voter')
@click.option('--dob', prompt='Date of Birth (YYYY-MM-DD)', help='Date of birth')

@click.option('--address-line-1', prompt='Address Line 1', help='Street address')
@click.option('--ward', prompt='Ward', help='Ward name')
@click.option('--subcounty', prompt='Subcounty', help='Subcounty name')
@click.option('--county', prompt='County', help='County name')
@click.option('--postal-code', prompt='Postal Code', help='Postal code')
@click.option('--country', prompt='Country Code (2 letters)', help='2-letter country code')
@click.option('--address-type', prompt='Address Type', default='Home', help='Type of address (Home/Work/etc)')
def register_voter(national_id, title, first_name, middle_name, last_name, dob, 
                  address_line_1, ward, subcounty, county, postal_code, country, address_type):
    """Register a new voter with address"""
    try:
        
        if not validate_date(dob):
            click.echo("Error: Invalid date format. Use YYYY-MM-DD")
            return
        
        
        if not validate_country_code(country):
            click.echo("Error: Country must be a 2-letter code")
            return
        
        
        address_errors = validate_address_data(address_line_1, ward, subcounty, county, postal_code, country, address_type)
        if address_errors:
            for error in address_errors:
                click.echo(f"❌ {error}")
            return
        
       
        voter_data = create_voter_dict(
            national_id=national_id,
            title=title,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            dob=dob
        )
        
      
        db = next(get_db())
        
        
        voter = Voter(**voter_data)
        db.add(voter)
        db.flush()  
        
        
        address_data = create_address_dict(
            voter_id=voter.voter_id,
            address_line_1=address_line_1,
            ward=ward,
            subcounty=subcounty,
            county=county,
            postal_code=postal_code,
            country=country,
            address_type=address_type
        )
        
        address = VoterAddress(**address_data)
        db.add(address)
        
        db.commit()
        
        click.echo(f"✅ Voter {first_name} {last_name} registered successfully!")
        click.echo(f"📫 Address: {address_line_1}, {ward}, {county}")
        
    except Exception as e:
        click.echo(f"❌ Error registering voter: {str(e)}")

@cli.command()
@click.option('--national-id', prompt='National ID Number', help='National ID to search for')
def find_voter(national_id):
    """Find a voter by national ID"""
    try:
        db = next(get_db())
        voter = db.query(Voter).filter(Voter.national_id_number == national_id).first() 
        
        if voter:
            click.echo(format_voter_info(voter))
            
            address = db.query(VoterAddress).filter(VoterAddress.voter_id == voter.voter_id).first()
            if address:
                click.echo(format_address_info(address))
        else:
            click.echo(f"❌ No voter found with National ID: {national_id}")
            
    except Exception as e:
        click.echo(f"❌ Error finding voter: {str(e)}")

@cli.command()
def list_voters():
    """List all registered voters"""
    try:
        db = next(get_db())
        voters = db.query(Voter).all()
        
        if not voters:
            click.echo("ℹ️  No voters registered yet.")
            return
        
        click.echo("\n📋 Registered Voters:")
        display_voters_table(voters)
        click.echo(f"\nTotal voters: {len(voters)}")
            
    except Exception as e:
        click.echo(f"❌ Error listing voters: {str(e)}")

@cli.command()
@click.option('--national-id', prompt='National ID to delete', help='National ID of voter to delete')
def delete_voter(national_id):
    """Delete a voter by national ID"""
    try:
        db = next(get_db())
        voter = db.query(Voter).filter(Voter.national_id_number == national_id).first()  
        
        if not voter:
            click.echo(f"❌ No voter found with National ID: {national_id}")
            return
        
        if click.confirm(f'Are you sure you want to delete voter {voter.first_name} {voter.last_name}?'):
           
            db.query(VoterAddress).filter(VoterAddress.voter_id == voter.voter_id).delete()
            db.delete(voter)
            db.commit()
            click.echo(f"✅ Voter {voter.first_name} {voter.last_name} deleted successfully!")
            
    except Exception as e:
        click.echo(f"❌ Error deleting voter: {str(e)}")

if __name__ == '__main__':
    cli()
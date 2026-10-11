import os
import pandas as pd
from pydantic import BaseModel, ValidationError, Field
import anthropic

# Initialize Claude Client using the environment variable you set in the terminal
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# 1. Define strict validation rules (prevents "wrong numbers that look right")
class PropertyModel(BaseModel):
    property_id: int
    address: str
    price: float = Field(gt=0, description="Price must be greater than zero")
    square_feet: int = Field(gt=0, description="Square footage must be positive")
    status: str

def generate_claude_pitch(address, price, sqft):
    """Sends clean data to Claude to draft a professional real estate marketing hook."""
    prompt = f"Write a catchy 1-sentence real estate marketing hook for a property at {address}, priced at ${price:,.0f} with {sqft} sq ft."
    
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def run_pipeline():
    print("--- Starting Real Estate Automation Pipeline ---\n")
    
    try:
        df = pd.read_csv('raw_properties.csv')
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return

    valid_records = []
    quarantined_records = []

    # 2. Loop through data and verify rows
    for index, row in df.iterrows():
        try:
            prop = PropertyModel(
                property_id=row['property_id'],
                address=str(row['address']),
                price=float(row['price']),
                square_feet=int(row['square_feet']),
                status=str(row['status'])
            )
            valid_records.append(prop)
        except (ValidationError, ValueError, TypeError):
            print(f"[RISK ALERT] Quarantined row {index} due to invalid data: {row.to_dict()}")
            quarantined_records.append(row.to_dict())

    print(f"\n--- Verification Complete ---")
    print(f"Valid records processed: {len(valid_records)}")
    print(f"Bad records caught & quarantined: {len(quarantined_records)}\n")

    # 3. Enrich valid records with Claude
    print("--- Generating AI Marketing Hooks for Valid Listings ---")
    for item in valid_records:
        pitch = generate_claude_pitch(item.address, item.price, item.square_feet)
        print(f"Listing ID {item.property_id}: {pitch}")

if __name__ == "__main__":
    run_pipeline()
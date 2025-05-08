import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import re
import time
pd.set_option('display.max_columns', None)

# Load Excel file
df = pd.read_excel("outlets_with_coordinates.xlsx")
df = df[df["state"].str.lower() != df["state1"].str.lower()]

# Replace with your filename
df.rename(columns={'latitude': 'latitude1', "longitude": "longitude1"}, inplace=True)
df.drop_duplicates(subset=["name of dealer", "address", "town", "state"], inplace=True)

# Clean the text fields
def clean_text(text):
    text = str(text)
    text = re.sub(r"[^a-zA-Z0-9\s,]", "", text)  # Keep only letters, numbers, space, and commas
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    return text.strip().lower()

# Clean relevant columns
for col in ["name of dealer", "address", "town", "state"]:
    df[col] = df[col].apply(lambda x: clean_text(x) if pd.notnull(x) else "")

# Combine address columns to form full address
def clean_address(row):
    parts = []
    for col in ['name of dealer', 'address', 'town', 'state']:
        part = str(row[col]).lower().strip()
        if part != 'nan' and part != '':
            parts.append(part)
    return ', '.join(parts) + ', India'

df["full_address"] = df.apply(clean_address, axis=1)

# Initialize geocoder with user agent
geolocator = Nominatim(user_agent="geoapi", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=3, error_wait_seconds=5.0)

# Create columns for lat/lon
df["latitude"] = None
df["longitude"] = None

# Function to retry geocoding
def geocode_with_retry(address, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            location = geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except Exception as e:
            print(f"Error geocoding {address}: {e}")
            attempt += 1
            time.sleep(5)  # Wait before retrying
    return None, None

# Loop through rows and geocode
for i, row in df.iterrows():
    full_address = row["full_address"]
    latitude, longitude = geocode_with_retry(full_address)
    if latitude and longitude:
        df.at[i, "latitude"] = latitude
        df.at[i, "longitude"] = longitude
        print(f"[{i+1}] Success: {full_address} ({latitude}, {longitude})")
    else:
        print(f"[{i+1}] Not found: {full_address}")

# Save updated data to new Excel file
df.to_excel("outlets_with_new_coordinates.xlsx", index=False)
print("Coordinates saved to 'outlets_with_coordinates.xlsx'")

import pandas as pd
from geopy.geocoders import Nominatim
import time

# Initialize the geocoder
geolocator = Nominatim(user_agent="geoapiExercises")

# Define the data with dealer names, latitude, and longitude
data = [
    {"dealer_name": "Ambica Enterprises", "latitude": 17.54818399, "longitude": 82.85768437},
    {"dealer_name": "Sri Ambica Electronics", "latitude": 18.86619289, "longitude": 83.55274118},
    {"dealer_name": "Suchitra Electronics", "latitude": 18.10805704, "longitude": 83.13902128},
    {"dealer_name": "Uppala Furniture", "latitude": 12.67968753, "longitude": 74.90483342},
    {"dealer_name": "Aditya Home Needs and Electronics", "latitude": 16.60372374, "longitude": 81.80746076},
    {"dealer_name": "Ayyappa Cell World and Electronics", "latitude": 19.65724758, "longitude": 78.52627527},
    {"dealer_name": "MS Sri Amareshwara Enterprises", "latitude": 15.53539893, "longitude": 76.50913234},
    {"dealer_name": "Royal Furniture", "latitude": 13.09600678, "longitude": 79.65845384},
    {"dealer_name": "Laxmi Furniture", "latitude": 17.90634162, "longitude": 77.52886399},
    {"dealer_name": "Alko Fabrics", "latitude": 17.33656205, "longitude": 76.84399372},
    {"dealer_name": "Mubarak Electronic", "latitude": 16.94010901, "longitude": 75.83655581},
    {"dealer_name": "Laxmi Haryana Handloom", "latitude": 23.2108647, "longitude": 77.44346683},
    {"dealer_name": "Akash K Furniture", "latitude": 23.26680384, "longitude": 77.45792021},
    {"dealer_name": "Kaka Furnitures", "latitude": 28.68669601, "longitude": 77.29841254},
    {"dealer_name": "Ammu Furniture", "latitude": 10.99694999, "longitude": 77.27621865},
    {"dealer_name": "Best Furniture", "latitude": 10.95670442, "longitude": 76.96026118},
    {"dealer_name": "Diamond Furniture", "latitude": 10.99787252, "longitude": 76.95993383},
    {"dealer_name": "Furniture World", "latitude": 11.34010536, "longitude": 77.68399148},
    {"dealer_name": "Goldan Furniture", "latitude": 11.29921929, "longitude": 77.64577218},
    {"dealer_name": "Kavitha Furniture", "latitude": 9.170209975, "longitude": 77.54759725},
    {"dealer_name": "Balaji Home Appliances", "latitude": 9.964928966, "longitude": 77.78872751},
    {"dealer_name": "Modern Furniture", "latitude": 10.9212344, "longitude": 79.43965193},
    {"dealer_name": "VKM Furniture", "latitude": 10.76603809, "longitude": 79.64453302},
    {"dealer_name": "A J Furniture", "latitude": 10.37683902, "longitude": 78.38549081},
    {"dealer_name": "Amaze Furniture", "latitude": 10.96151162, "longitude": 78.07573331},
    {"dealer_name": "R K Furniture", "latitude": 10.96402618, "longitude": 78.04476128},
    {"dealer_name": "Jaiswal Furniture Electronic", "latitude": 26.07742779, "longitude": 83.29043091},
    {"dealer_name": "Vaisno Engineering Works", "latitude": 26.18162468, "longitude": 82.91108339}
]

# Function to get the state from latitude and longitude
def get_state(lat, lon):
    location = geolocator.reverse((lat, lon), language='en', timeout=10)
    if location:
        address = location.raw.get('address', {})
        state = address.get('state', 'Unknown')
        return state
    return 'Unknown'

# Add the state information to the data
for dealer in data:
    dealer['state'] = get_state(dealer['latitude'], dealer['longitude'])
    # Optional: To avoid hitting the API too frequently, add a delay
    time.sleep(1)

# Create the DataFrame
df = pd.DataFrame(data)

# Show the DataFrame
print(df)

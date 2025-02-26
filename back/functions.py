import json
import google.generativeai as genai
import json
from math import radians, sin, cos, sqrt, atan2
import os

api_fkey = os.getenv("GEMINI_KEY")
genai.configure(api_key=api_fkey)

REFERENCE_FILE = "data.txt"

with open(REFERENCE_FILE, "r", encoding="utf-8") as file:
    reference_data = file.read()  

def generate_metadata(item_name):
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
    Generate structured metadata for the item: '{item_name}'.
    Match it with the closest category from the reference list below:
    {reference_data}
    Output should be a valid JSON object with:
    - "EEE": Matching EEE category code
    - "lifespan": Expected lifespan in years
    - "brand": Likely brand (if applicable)
    - "weight": Approximate weight in kg
    Example output:
    {{
      "EEE": "ITEW10",
      "lifespan": 10,
      "brand": "Samsung",
      "weight": 0.6
    }}
    Now, generate the metadata for '{item_name} in json format'.
    """
    response = model.generate_content(prompt)

    metadata_json = json.loads(response.text[7:-3])
    return metadata_json



def nearest_center(userCoordinates: list, refurbishable: bool):
  with open('places.geojson', 'r' ) as place_json:
    places = json.load(place_json)
  
    filtered_places = [
    place for place in places if 
    "Type" in place and "coordinates" in place and
    ((refurbishable and place["Type"] == "Refurbisher") or
     (not refurbishable and place["Type"] != "Refurbisher"))
    ]
    if not filtered_places:
        return {"error": "No matching centers found"}


  def haversine_distance(coord1, coord2):

      R = 6371 
      lat1, lon1 = radians(coord1[0]), radians(coord1[1])
      lat2, lon2 = radians(coord2[0]), radians(coord2[1])

      dlat = lat2 - lat1
      dlon = lon2 - lon1

      a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
      c = 2 * atan2(sqrt(a), sqrt(1 - a))
      return R * c  # Distance in km

  
  nearest = min(filtered_places, key=lambda r: haversine_distance(userCoordinates, r["coordinates"]))
  return nearest


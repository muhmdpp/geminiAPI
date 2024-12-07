from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# Configure the Generative AI API
genai.configure(api_key="AIzaSyCYDJmGjv0J4tCCjsfuNSa4BPhBwnWDCs0")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize FastAPI app
app = FastAPI()

# Define a request model for the API
class UserPreferences(BaseModel):
    activities: str
    budget: str
    noOfDays: str

# Define a response model for the API
class Destination(BaseModel):
    name: str
    attractions: list[str]

# Define the API endpoint
@app.post("/get-destinations/")
def get_destinations(preferences: UserPreferences):
    try:
        # Generate content based on user input
        prompt = (
            f"I am creating a tour guiding app, I will tell the itineraries and preferences. "
            f"Based on that, suggest me some destinations. Give it as a list where the "
            f"destination name and just my preferences: the preferences are budget: {preferences.budget}, "
            f"activities: {preferences.activities}, no. of days: {preferences.noOfDays}. "
            f"Just give the destination names alone and the best 2 spots of that particular area.give in the format of just destination name,attractions as array. the output should not contain anything other than that"
        )
        response = model.generate_content(prompt)

        # Process the generated text
        destinations_list = []
        for destination_str in response.text.split("\n"):
            destination_parts = destination_str.split(",")
            destination_name = destination_parts[0].strip()
            attractions = destination_parts[1].strip()[1:-1].split(", ")
            destinations_list.append(Destination(name=destination_name, attractions=attractions))

        # Return the response with a list of destinations
        return {"destinations": destinations_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
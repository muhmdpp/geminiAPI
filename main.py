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

# Define the API endpoint
@app.post("/get-destinations/")
def get_destinations(preferences: UserPreferences):
    try:
        # Generate content based on user input
        prompt = (
            f"I am creating a tour guiding app. Based on the given preferences, "
            f"suggest me destinations along with the top two attractions in each destination. "
            f"The preferences are budget: {preferences.budget}, activities: {preferences.activities}, "
            f"and number of days: {preferences.noOfDays}. "
            f"Return the output as a JSON object where each destination is a key, and its value is an object "
            f"with 'Attractions' as a key containing an array of the top two attractions. The format should be: "
            f"{{"
            f'"Destination Name": {{"Attractions": ["Attraction 1", "Attraction 2"]}}, '
            f'"Next Destination Name": {{"Attractions": ["Attraction 1", "Attraction 2"]}}'
            f"}}. No other text should be included in the output."
        )

        response = model.generate_content(prompt)
        return {"destinations": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


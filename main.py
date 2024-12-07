from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import json

# Configure the Generative AI API
genai.configure(api_key="AIzaSyCYDJmGjv0J4tCCjsfuNSa4BPhBwnWDCs0")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize FastAPI app
app = FastAPI()

class UserPreferences(BaseModel):
    activities: str
    budget: str
    noOfDays: str

@app.post("/get-destinations/")
def get_destinations(preferences: UserPreferences):
    try:
        prompt = (
            f"I am creating a tour guiding app. Based on the preferences, suggest destinations. "
            f"Format the response as: {{'region': '<region>', 'places': ['<place1>', '<place2>']}} "
            f"with no additional text. Preferences are: budget: {preferences.budget}, "
            f"activities: {preferences.activities}, no. of days: {preferences.noOfDays}."
        )
        response = model.generate_content(prompt)
        # Parse the response to ensure it's valid JSON
        destinations = json.loads(response.text)
        return {"destinations": destinations}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid response format from AI model.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

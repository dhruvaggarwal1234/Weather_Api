from dotenv import load_dotenv
import os 


load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")



print( API_URL, API_KEY)
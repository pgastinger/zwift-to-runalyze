import garth
import os

from dotenv import load_dotenv
load_dotenv()

garmin_username = os.getenv("GARMIN_USERNAME")
garmin_password = os.getenv("GARMIN_PASSWORD")
# If MFA is enabled, you'll be prompted for the code here
garth.login(garmin_username, garmin_password)

# Save the session tokens for future use (up to one year)
garth.save("~/.garth")

# Now you can make API calls, e.g., to get activities
# activities = garth.connectapi("/activities")
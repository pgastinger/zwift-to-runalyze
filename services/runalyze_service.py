"""Runalyze"""

import logging
import requests
import os

RUNALYZE_API_URL = "https://runalyze.com/api/v1/activities/uploads"

class RunalyzeService:
    """Service for interacting with Garmin Connect."""

    def __init__(self, token: str):
        """Initialize RunalyzeService with token.

        Args:
            token: Runalyze token
        """
        self.token = token
        self.logger = logging.getLogger(__name__)
        self.logger.info("RunalyzeService initialized successfully.")
        self.session = requests.Session()
        self.session.headers.update({"token":self.token})


    def upload_file_to_runalyze(self, file_path:str):
        if not os.path.exists(file_path):
            raise FileNotFoundError()
        
        self.logger.info(f"Would upload file {file_path}")
        #print(f"Would upload file {file_path}")

        try:
            with open(file_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(file_path), f, 'application/octet-stream')
                }

                print(f"Uploading file: {os.path.basename(file_path)}...")
                
                # 4. Make the POST request
                response = self.session.post(RUNALYZE_API_URL, files=files)

            # 5. Handle the response
            if response.status_code == 201:
                print("✅ Upload successful!")
                # The response body should contain details about the uploaded activity
                print("Response Data:", response.json())
            else:
                print(f"❌ Upload failed with status code {response.status_code}")
                print("Error Response:", response.text)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
# This script requires the 'fit-tool' library:
# pip install fit-tool
#
# If you receive a 'ModuleNotFoundError', ensure that:
# 1. The 'fit-tool' package is installed via 'pip install fit-tool'.
# 2. You are running the script from the same Python environment/virtual environment
#    where the package was installed.

from fit_tool.fit_file import FitFile
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.developer_data_id_message import DeveloperDataIdMessage
from fit_tool.profile.messages.field_description_message import FieldDescriptionMessage
from fit_tool.profile.messages.session_message import SessionMessage
from fit_tool.profile.messages.activity_message import ActivityMessage
from fit_tool.profile.messages.record_message import RecordMessage
# These are the imports that failed:
from fit_tool.profile.profile_type import DateMode
from fit_tool.profile.profile_type import FileType
from fit_tool.profile.profile_type import Sport
from fit_tool.profile.profile_type import Activity
from fit_tool.profile.profile_type import Manufacturer

from fit_tool.profile.profile_type import ProfileType
import time
import datetime

def generate_sample_fit_file(filepath: str):
    """
    Generates a simple cycling activity FIT file with simulated data.
    The data simulates 5 minutes of cycling.
    """
    # Initialize the FitFile object
    fit_file = FitFile()

    # --- 1. File ID Message (Mandatory First Message) ---
    # This identifies the file type, manufacturer, and creation date.
    file_id_message = FileIdMessage()
    file_id_message.file = FileType.ACTIVITY  # This is an activity file
    file_id_message.manufacturer = Manufacturer.GARMIN  # Use Garmin ID (67)
    file_id_message.product = 1234  # Mock product ID
    file_id_message.serial_number = 99887766  # Unique serial number
    
    # Set the timestamp for the file's creation
    creation_time = int(time.time())
    file_id_message.time_created = DateMode(creation_time)
    fit_file.add(file_id_message)
    print(f"File ID set. Activity starts at: {datetime.datetime.fromtimestamp(creation_time)}")

    # --- 2. Record Messages (The actual activity data points) ---
    num_records = 300  # 5 minutes * 60 seconds = 300 data points
    start_timestamp = creation_time
    total_distance_m = 0.0

    print(f"Generating {num_records} record messages...")

    for i in range(num_records):
        # Time increases by 1 second for each record
        current_time = start_timestamp + i
        
        # Simulate data fields
        power = 150 + (i % 50)  # Power oscillates between 150-200W
        heart_rate = 120 + (i % 30) # HR oscillates between 120-150 bpm
        cadence = 75 + (i % 10)  # Cadence oscillates between 75-84 RPM
        speed_mps = 6.0 + (i / 1000) # Speed starts at 6 m/s (21.6 kph) and slightly increases
        
        # Calculate distance increment for 1 second
        distance_increment = speed_mps * 1
        total_distance_m += distance_increment

        record_message = RecordMessage()
        record_message.timestamp = DateMode(current_time)
        record_message.power = power
        record_message.heart_rate = heart_rate
        record_message.cadence = cadence
        record_message.distance = round(total_distance_m, 2)
        record_message.speed = round(speed_mps, 2)
        
        fit_file.add(record_message)

    # --- 3. Session Message (Summary of the workout) ---
    # Must come after the records and defines the span of the data.
    session_message = SessionMessage()
    session_message.message_index = 0
    
    # Timestamps are based on the first and last record
    session_message.start_time = DateMode(start_timestamp)
    session_message.timestamp = DateMode(current_time) # The timestamp of the last record
    
    session_message.total_elapsed_time = float(num_records)  # Total seconds
    session_message.total_timer_time = float(num_records)    # Total seconds spent actively recording
    session_message.sport = Sport.CYCLING
    session_message.session = S
    
    # Calculate averages and totals
    session_message.total_distance = round(total_distance_m, 2) # Total distance in meters
    session_message.avg_power = round(sum([150 + (i % 50) for i in range(num_records)]) / num_records, 2)
    session_message.avg_heart_rate = round(sum([120 + (i % 30) for i in range(num_records)]) / num_records)
    session_message.max_power = max([150 + (i % 50) for i in range(num_records)])
    session_message.max_heart_rate = max([120 + (i % 30) for i in range(num_records)])
    
    fit_file.add(session_message)
    print("Session message added.")

    # --- 4. Activity Message (Defines the full activity lifecycle) ---
    # This must be the absolute last message in the file.
    activity_message = ActivityMessage()
    activity_message.timestamp = session_message.timestamp # Last timestamp
    activity_message.total_timer_time = session_message.total_timer_time
    activity_message.num_sessions = 1
    activity_message.activity = Activity.MANUAL
    
    fit_file.add(activity_message)
    print("Activity message added.")

    # --- 5. Write the FIT file ---
    fit_file.to_file(filepath)
    print(f"\n✅ Success: FIT file saved to {filepath}")

# --- Execution ---
output_filename = "sample_activity.fit"
generate_sample_fit_file(output_filename)
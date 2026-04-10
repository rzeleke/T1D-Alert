# Import libraries
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read credentials from environment
ACCOUNT_SID    = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN     = os.getenv('TWILIO_AUTH_TOKEN')
FROM_NUMBER    = os.getenv('TWILIO_FROM_NUMBER')
CAREGIVER_PHONE = os.getenv('CAREGIVER_PHONE')

def send_sms(message):
    try:
        # Create a Twilio client using credential
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        # Send the SMS message
        sms = client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=CAREGIVER_PHONE
        )

        print(f"SMS sent successfully. SID: {sms.sid}")
        return True

    except Exception as error:
        print(f"Failed to send SMS: {error}")
        return False
    
def send_exercise_alert(child_name, exercise_title, start_time, has_cgm=False):
    # Build the alert message
    message = (
        f"T1D Alert: {child_name} has {exercise_title} "
        f"starting at {start_time}. "
        f"Please confirm glucose levels are safe before exercise."
    )

    # CGM activity mode reminder if child uses a CGM device
    if has_cgm:
        message += (
            f" Reminder: Set {child_name}'s CGM to Activity Mode "
            f"to reduce hypoglycemia during and/or after exercise."
        )

    return send_sms(message)


if __name__ == '__main__':
    print("Testing SMS notification...")
    print()

    # Test 1 - without CGM
    print("Test 1: Alert without CGM")
    send_exercise_alert(
        child_name='Riot',
        exercise_title='Soccer Practice',
        start_time='2026-04-10 14:00:00',
        has_cgm=False
    )
    print()

    # Test 2 - with CGM
    print("Test 2: Alert with CGM reminder")
    send_exercise_alert(
        child_name='Riot',
        exercise_title='Gym Workout',
        start_time='2026-04-11 10:00:00',
        has_cgm=True
    )
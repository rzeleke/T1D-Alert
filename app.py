# Import libraries
import streamlit as st
from datetime import datetime, timedelta
import storage
import csv_import
import rule_engine
import notification

# Configure the Streamlit page
st.set_page_config(
    page_title="T1D Exercise Alert System",
    page_icon="🏃",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("🏃 T1D Exercise Alert")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["Schedule", "Check-In", "History", "Settings"]
)

# ── Schedule Page ───────────────────────────────────────────────
if page == "Schedule":
    st.title("📅 Exercise Schedule")
    st.write("Upload your Google Calendar export to import exercise sessions.")

    # File upload widget - must be inside the if page block
    uploaded_file = st.file_uploader(
        "Upload your calendar file (.ics)",
        type=["ics"]
    )

    if uploaded_file is not None:
        # Save the uploaded file temporarily to disk
        with open("temp_calendar.ics", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Parse the calendar file
        all_events, exercise_events = csv_import.get_exercise_events("temp_calendar.ics")

        # Show summary
        st.success(f"Found {len(all_events)} total events — {len(exercise_events)} exercise sessions detected.")

        if len(exercise_events) == 0:
            st.warning("No exercise events found. Try adjusting your keywords in Settings.")
        else:
            # Show preview table
            st.subheader("Preview — Exercise Sessions Found")
            preview_data = []
            for event in exercise_events:
                preview_data.append({
                    "Title": event.get("title", ""),
                    "Start": str(event.get("start", "")),
                    "End": str(event.get("end", ""))
                })
            st.dataframe(preview_data, width="stretch")

            # Confirm import button
            if st.button("✅ Confirm Import"):
                storage.create_tables()
                saved = 0
                skipped = 0

                for event in exercise_events:
                    start = event.get("start")
                    end = event.get("end")
                    title = event.get("title", "")

                    # Calculate alert time 30 minutes before session
                    alert_time = start - timedelta(minutes=30)

                    result = storage.save_session(title, start, end, alert_time)
                    if result:
                        saved += 1
                    else:
                        skipped += 1

                st.success(f"Import complete! {saved} sessions saved, {skipped} duplicates skipped.")


# ── Check-In Page ───────────────────────────────────────────────
elif page == "Check-In":
    st.title("🩸 Pre-Exercise Glucose Check-In")
    st.write("Enter your current blood glucose reading before exercise.")

    glucose = st.number_input(
        "Blood glucose level (mg/dL)",
        min_value=40,
        max_value=400,
        value=120,
        step=1
    )

    if st.button("🔍 Check Glucose"):
        result = rule_engine.classify_glucose(glucose)
        color = rule_engine.get_zone_color(result['zone'])

        # Display classification
        st.markdown("---")
        st.subheader(f"Result: {result['classification']}")
        st.info(f"📋 {result['recommendation']}")

        # Color coded zone indicator
        if color == 'green':
            st.success(f"Zone {result['zone']} — {result['classification']}")
        elif color in ['red', 'purple']:
            st.error(f"Zone {result['zone']} — {result['classification']}")
        elif color in ['orange', 'yellow']:
            st.warning(f"Zone {result['zone']} — {result['classification']}")
        else:
            st.info(f"Zone {result['zone']} — {result['classification']}")

        # Send caregiver alert if needed
        if result['alert_caregiver']:
            st.warning("⚠️ Caregiver has been notified.")
            notification.send_sms(
                f"T1D Glucose Alert: Riot's pre-exercise glucose is {glucose} mg/dL. "
                f"Classification: {result['classification']}. "
                f"Recommended action: {result['recommendation']}"
            )

        # Save reading to database
        storage.save_glucose(1, glucose, result['classification'])
        st.caption("Reading saved to history.")


# ── History Page ────────────────────────────────────────────────
elif page == "History":
    st.title("📊 Session History")
    storage.create_tables()

    # Sessions table
    st.subheader("Exercise Sessions")
    sessions = storage.get_all_sessions()

    if len(sessions) == 0:
        st.info("No sessions imported yet. Go to the Schedule page to import your calendar.")
    else:
        session_data = []
        for s in sessions:
            session_data.append({
                "ID": s[0],
                "Title": s[1],
                "Start": s[2],
                "End": s[3],
                "Alert Time": s[4],
                "Imported": s[5]
            })
        st.dataframe(session_data, width='stretch')

    st.markdown("---")

    # Glucose readings table
    st.subheader("Glucose Readings")
    readings = storage.get_glucose_readings()

    if len(readings) == 0:
        st.info("No glucose readings recorded yet. Go to the Check-In page to log a reading.")
    else:
        reading_data = []
        for r in readings:
            reading_data.append({
                "ID": r[0],
                "Session ID": r[1],
                "Glucose (mg/dL)": r[2],
                "Classification": r[3],
                "Recorded At": r[4]
            })
        st.dataframe(reading_data, width='stretch')


# ── Settings Page ───────────────────────────────────────────────
elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Configure your alert preferences.")

    st.subheader("Patient Information")
    child_name = st.text_input("Child/Patient name", value="Riot")
    has_cgm = st.checkbox("Uses a CGM device (Dexcom, Libre, etc.)")

    st.subheader("Alert Settings")
    alert_lead = st.slider(
        "Alert lead time (minutes before exercise)",
        min_value=10,
        max_value=60,
        value=30,
        step=5
    )

    st.subheader("Exercise Keywords")
    st.write("Sessions containing these words will be detected as exercise events.")
    keywords = st.text_area(
        "Keywords (one per line)",
        value="gym\nrun\nworkout\nsoccer\nswim\npractice\nexercise\nyoga\nbike\nwalk\ntennis\nbasketball\nfootball\ntraining"
    )

    if st.button("💾 Save Settings"):
        st.success(f"Settings saved! Alerts will fire {alert_lead} minutes before each session.")
        if has_cgm:
            st.info(f"CGM Activity Mode reminder will be included in alerts for {child_name}.")
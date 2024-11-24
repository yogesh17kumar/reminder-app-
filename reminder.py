import streamlit as st
import datetime
import time

# Title of the app
st.title("Reminder App")

# Function to add a new reminder
def add_reminder(reminder_text, reminder_datetime):
    if "reminders" not in st.session_state:
        st.session_state.reminders = []
    reminder = {"text": reminder_text, "datetime": reminder_datetime}
    st.session_state.reminders.append(reminder)

# Function to display the reminders
def display_reminders():
    if "reminders" in st.session_state and st.session_state.reminders:
        st.write("### Your Reminders:")
        for i, reminder in enumerate(st.session_state.reminders):
            reminder_datetime = reminder["datetime"].strftime("%Y-%m-%d %I:%M %p")
            st.write(f"{i + 1}. {reminder['text']} - Due by {reminder_datetime}")
    else:
        st.write("No reminders yet!")

# Function to check for reminders and display a special message
def check_for_reminders():
    if "reminders" in st.session_state:
        current_time = datetime.datetime.now()
        for reminder in st.session_state.reminders:
            if reminder["datetime"] <= current_time:
                st.session_state.reminders.remove(reminder)
                # Show a special message when the reminder time arrives
                st.success(f"Reminder: {reminder['text']}! It's time!")
                break  # Stop after showing the first matching reminder

# Input for reminder
with st.form(key="reminder_form"):
    reminder_text = st.text_input("Enter your reminder:")
    reminder_date = st.date_input("Set reminder date:", min_value=datetime.date.today())
    reminder_time = st.text_input("Set reminder time (e.g., 2:30 PM or 14:30):")
    
    # Try to parse the time input
    try:
        reminder_time_obj = datetime.datetime.strptime(reminder_time, "%I:%M %p")
    except ValueError:
        try:
            reminder_time_obj = datetime.datetime.strptime(reminder_time, "%H:%M")
        except ValueError:
            reminder_time_obj = None

    # Combine date and time to create datetime
    if reminder_time_obj:
        reminder_datetime = datetime.datetime.combine(reminder_date, reminder_time_obj.time())
    else:
        reminder_datetime = None

    submit_button = st.form_submit_button("Add Reminder")

    if submit_button:
        if reminder_datetime:
            add_reminder(reminder_text, reminder_datetime)
            st.success(f"Reminder set for {reminder_text} on {reminder_datetime.strftime('%Y-%m-%d %I:%M %p')}")
        else:
            st.error("Invalid time format. Please use either HH:MM AM/PM or HH:MM (24-hour).")

# Display the current reminders
display_reminders()

# Check for any reminders that should trigger the special message
check_for_reminders()

# Option to reset all reminders
if st.button("Clear All Reminders"):
    st.session_state.reminders = []
    st.write("All reminders have been cleared.")

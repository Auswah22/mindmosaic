import os

from openai import OpenAI
import streamlit as st
import pandas as pd
from datetime import datetime




import json

def save_mood_log(mood_log):
    with open("mood_log.json", "w") as file:
        json.dump(mood_log, file)

def load_mood_log():
    try:
        with open("mood_log.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []




# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to analyze mood patterns and provide insights
def analyze_mood_patterns(mood_data):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use GPT-4 for mood analysis
            messages=[
                {"role": "system", "content": "You are a mental health assistant that analyzes mood patterns and provides insights."},
                {"role": "user", "content": f"Analyze the following mood data and provide insights and recommendations: {mood_data}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing mood patterns: {str(e)}"

# Function to generate guided journaling prompts
def generate_journaling_prompt():
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Use GPT-4 for journaling prompts
            messages=[
                {"role": "system", "content": "You are a mental health assistant that provides guided journaling prompts."},
                {"role": "user", "content": "Generate a journaling prompt to help someone reflect on their feelings and experiences."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating journaling prompt: {str(e)}"

# Streamlit app for Interactive Mental Health Tools
st.title("Interactive Mental Health Tools")

# Mood Tracker
st.header("Mood Tracker")
mood = st.selectbox("How are you feeling today?", ["Happy", "Sad", "Anxious", "Stressed", "Calm", "Angry", "Tired"])
if st.button("Log Mood"):
    mood_data = {"date": datetime.now().strftime("%Y-%m-%d"), "mood": mood}
    st.session_state.mood_log = st.session_state.get("mood_log", [])
    st.session_state.mood_log.append(mood_data)
    st.success("Mood logged successfully!")

if st.button("Analyze Mood Patterns"):
    if "mood_log" in st.session_state and st.session_state.mood_log:
        mood_data = pd.DataFrame(st.session_state.mood_log)
        insights = analyze_mood_patterns(mood_data.to_string())
        st.write("### Mood Analysis and Recommendations")
        st.write(insights)
    else:
        st.warning("No mood data available. Please log your mood first.")

# Guided Journaling
st.header("Guided Journaling")
if st.button("Get Journaling Prompt"):
    prompt = generate_journaling_prompt()
    st.write("### Journaling Prompt")
    st.write(prompt)

# Breathing Exercises & Meditation
st.header("Breathing Exercises & Meditation")
st.write("### 5-4-3-2-1 Grounding Exercise")
st.write("""
1. **5 Things You Can See**: Look around and name 5 things you can see.
2. **4 Things You Can Touch**: Name 4 things you can touch.
3. **3 Things You Can Hear**: Listen carefully and name 3 things you can hear.
4. **2 Things You Can Smell**: Name 2 things you can smell.
5. **1 Thing You Can Taste**: Name 1 thing you can taste.
""")

st.write("### Box Breathing Exercise")
st.write("""
1. **Inhale** for 4 seconds.
2. **Hold** your breath for 4 seconds.
3. **Exhale** for 4 seconds.
4. **Hold** your breath for 4 seconds.
5. Repeat for 5 minutes.
""")

st.write("### Guided Meditation")
st.write("""
1. Find a quiet place and sit comfortably.
2. Close your eyes and take a few deep breaths.
3. Focus on your breath and let go of any thoughts.
4. Continue for 5-10 minutes.
""")
import os

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO



from mental_health_tools import generate_journaling_prompt

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize session state for user data
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []
if "self_care_plan" not in st.session_state:
    st.session_state.self_care_plan = ""
if "challenges" not in st.session_state:
    st.session_state.challenges = {
        "7 Days of Gratitude": {"completed": False, "points": 50},
        "Mindful Study Breaks": {"completed": False, "points": 30},
        "Daily Meditation": {"completed": False, "points": 20},
    }
if "points" not in st.session_state:
    st.session_state.points = 0
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []
if "community_posts" not in st.session_state:
    st.session_state.community_posts = []

# Function to generate a story based on user input
def generate_story(emotion):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use GPT-4 for storytelling
            messages=[
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": f"Write a short story about someone feeling {emotion}."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating story: {str(e)}"

# Function to generate a visual mosaic based on user input
def generate_mosaic(emotion):
    try:
        response = client.images.generate(
            prompt=f"A visual mosaic representing {emotion}. The mosaic should be a collage of images, colors, and patterns that reflect the emotional state.",
            n=1,
            size="512x512"
        )
        image_url = response.data[0].url
        image = Image.open(BytesIO(requests.get(image_url).content))
        return image
    except Exception as e:
        return f"Error generating mosaic: {str(e)}"

# Function to generate a personalized self-care plan
def generate_self_care_plan(stress_level, preferences):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use GPT-4 for self-care plans
            messages=[
                {"role": "system", "content": "You are a mental health assistant that creates personalized self-care plans."},
                {"role": "user", "content": f"Create a self-care plan for someone with a {stress_level} stress level who enjoys {', '.join(preferences)}. Include mindfulness exercises, study breaks, physical activities, and creative outlets."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating self-care plan: {str(e)}"

# Function to moderate content using OpenAI's moderation API
def moderate_content(text):
    try:
        response = client.moderations.create(input=text)
        return response.results[0].flagged  # Returns True if content is flagged
    except Exception as e:
        st.error(f"Error moderating content: {str(e)}")
        return False

# Function to save posts to session state
def save_post(post):
    st.session_state.community_posts.append(post)

# Function to complete a challenge
def complete_challenge(challenge_name):
    if not st.session_state.challenges[challenge_name]["completed"]:
        st.session_state.challenges[challenge_name]["completed"] = True
        st.session_state.points += st.session_state.challenges[challenge_name]["points"]
        st.success(f"Challenge '{challenge_name}' completed! You earned {st.session_state.challenges[challenge_name]['points']} points.")
    else:
        st.warning(f"Challenge '{challenge_name}' is already completed.")

# Streamlit app for Integrated Dashboard
st.title("MindMosaic: AI-Powered Mental Health Ecosystem")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "EmotionScape (Generative AI)",
    "Mental Health Tools",
    "MindQuest (Gamified Challenges)",
    "Personalized Self-Care Plans",
    "Analytics",
    "Community Support Hub"
])

# Home Page
if page == "Home":
    st.write("### Welcome to MindMosaic!")
    st.write("""
    This dashboard helps you manage your mental health by:
    - Creating personalized stories and mosaics with **EmotionScape**
    - Tracking your mood and accessing mental health tools
    - Participating in the **Community Support Hub**
    - Completing **Gamified Challenges** to earn rewards
    - Generating **Personalized Self-Care Plans**
    - Viewing **Analytics** for well-being trends
    """)

# EmotionScape (Generative AI) Page
elif page == "EmotionScape (Generative AI)":
    st.write("### EmotionScape: Generative AI Art & Story Builder")
    emotion = st.text_input("How are you feeling today? (e.g., overwhelmed, happy, sad)")
    if st.button("Generate EmotionScape"):
        with st.spinner("Generating your EmotionScape..."):
            story = generate_story(emotion)
            mosaic = generate_mosaic(emotion)

        st.write("### Your Personalized Story")
        st.write(story)

        st.write("### Your Visual Mosaic")
        st.image(mosaic, caption="Your EmotionScape Mosaic", use_column_width=True)

# Mental Health Tools Page
elif page == "Mental Health Tools":
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
                    {"role": "system",
                     "content": "You are a mental health assistant that analyzes mood patterns and provides insights."},
                    {"role": "user",
                     "content": f"Analyze the following mood data and provide insights and recommendations: {mood_data}"}
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
                    {"role": "system",
                     "content": "You are a mental health assistant that provides guided journaling prompts."},
                    {"role": "user",
                     "content": "Generate a journaling prompt to help someone reflect on their feelings and experiences."}
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

# Community Support Hub Page
elif page == "Community Support Hub":
    st.write("### Community Support Hub")
    st.write("#### Share Your Story or Experience")
    user_name = st.text_input("Your Name (optional):")
    post_content = st.text_area("Write your post here:")
    if st.button("Submit Post"):
        if post_content.strip():
            if moderate_content(post_content):
                st.error("Your post contains inappropriate content and cannot be published.")
            else:
                post = {
                    "name": user_name if user_name else "Anonymous",
                    "content": post_content,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_post(post)
                st.success("Your post has been published!")
        else:
            st.warning("Please write something before submitting.")

    st.write("#### Community Posts")
    if st.session_state.community_posts:
        for post in reversed(st.session_state.community_posts):
            st.write(f"**{post['name']}** - {post['timestamp']}")
            st.write(post["content"])
            st.write("---")
    else:
        st.write("No posts yet. Be the first to share!")

# MindQuest (Gamified Challenges) Page
elif page == "MindQuest (Gamified Challenges)":
    st.write("### MindQuest: Gamified Wellness Challenges")
    st.write(f"#### Your Points: {st.session_state.points}")

    for challenge, details in st.session_state.challenges.items():
        st.write(f"**{challenge}**")
        st.write(f"- Points: {details['points']}")
        st.write(f"- Status: {'Completed' if details['completed'] else 'Not Completed'}")
        if not details["completed"]:
            if st.button(f"Complete {challenge}"):
                complete_challenge(challenge)

    st.write("#### Rewards")
    if st.session_state.points >= 50:
        st.success("You've unlocked a Virtual Plant for your MindGarden!")
    if st.session_state.points >= 100:
        st.success("You've unlocked a New Mosaic Element for your MindMosaic!")

# Personalized Self-Care Plans Page
elif page == "Personalized Self-Care Plans":
    st.write("### Personalized Self-Care Plans")
    stress_level = st.selectbox("What is your current stress level?", ["low", "medium", "high"])
    preferences = st.multiselect("What activities do you enjoy?", ["mindfulness", "physical activity", "creative outlets"])
    if st.button("Generate Self-Care Plan"):
        self_care_plan = generate_self_care_plan(stress_level, preferences)
        st.session_state.self_care_plan = self_care_plan
        st.success("Self-care plan generated successfully!")

    if st.session_state.self_care_plan:
        st.write("#### Your Self-Care Plan")
        st.write(st.session_state.self_care_plan)

# Analytics Page
elif page == "Analytics":
    st.write("### Well-Being Analytics")
    st.write("""
    This section provides aggregated analytics for schools or universities to monitor student well-being trends.
    All data is anonymized and privacy safeguards are in place.
    """)

    # Example analytics (mock data)
    st.write("#### Mood Distribution (Last 30 Days)")
    mood_distribution = pd.DataFrame({
        "Mood": ["Happy", "Sad", "Anxious", "Stressed", "Calm", "Angry", "Tired"],
        "Count": [120, 45, 60, 80, 90, 30, 50]
    })
    st.bar_chart(mood_distribution.set_index("Mood"))

    st.write("#### Most Popular Self-Care Activities")
    activities = pd.DataFrame({
        "Activity": ["Mindfulness", "Physical Activity", "Creative Outlets", "Reading", "Socializing"],
        "Count": [200, 150, 100, 80, 120]
    })
    st.bar_chart(activities.set_index("Activity"))

    st.write("#### Challenge Completion Rates")
    challenges = pd.DataFrame({
        "Challenge": ["7 Days of Gratitude", "Mindful Study Breaks", "Daily Meditation"],
        "Completion Rate (%)": [70, 50, 40]
    })
    st.bar_chart(challenges.set_index("Challenge"))
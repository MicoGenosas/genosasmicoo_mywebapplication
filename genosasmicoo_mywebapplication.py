import streamlit as st
import datetime

# ---------------- SESSION STATE ----------------
if "users" not in st.session_state:
    st.session_state["users"] = {}

if "profiles" not in st.session_state:
    st.session_state["profiles"] = {}

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "login_mode" not in st.session_state:
    st.session_state["login_mode"] = "Login"

if "submitted_goals" not in st.session_state:
    st.session_state["submitted_goals"] = None


# ---------------- LOGIN / SIGNUP ----------------
if not st.session_state["logged_in"]:

    st.markdown("<h1 style='color:white;'>Hello RoutineMates!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white;'>Please Login / Sign Up</h3>", unsafe_allow_html=True)

    option = st.radio(
        "Select Option",
        ["Login", "Sign Up"],
        horizontal=True,
        index=0 if st.session_state["login_mode"] == "Login" else 1
    )
    st.session_state["login_mode"] = option

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            if username in st.session_state["users"] and st.session_state["users"][username] == password:
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = username
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    else:  # SIGN UP
        age = st.number_input("Age", min_value=18, max_value=100)
        profile_img = st.file_uploader("Upload Profile Image", type=["png", "jpg", "jpeg"])

        if st.button("Create Account"):
            if username == "" or password == "" or profile_img is None:
                st.error("All fields are required.")
            elif username in st.session_state["users"]:
                st.error("Username already exists.")
            else:
                st.session_state["users"][username] = password
                st.session_state["profiles"][username] = profile_img
                st.success("Account created successfully! Please login.")
                st.session_state["login_mode"] = "Login"
                st.rerun()


# ---------------- MAIN APP ----------------
else:
    st.sidebar.title(f"Hello, {st.session_state['current_user']}!")

    if st.session_state["current_user"] in st.session_state["profiles"]:
        st.sidebar.image(st.session_state["profiles"][st.session_state["current_user"]], width=150)

    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Goals", "Healthy Tips", "Tasks Status", "About"]
    )

    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["current_user"] = None
        st.session_state["submitted_goals"] = None
        st.rerun()

    # ---------------- HOME ----------------
    if page == "Home":
        today = datetime.date.today()
        st.markdown(
            f"<h2 style='text-align:center; color:white;'>{today.strftime('%A, %B %d, %Y')}</h2>",
            unsafe_allow_html=True
        )
        st.markdown("---")

        st.subheader("View Time Frames")
        timeframe = st.radio("Choose timeframe:", ["Days", "Months", "Years"], horizontal=True)

        st.subheader("Mood Tracker")
        mood = st.slider("How are you feeling today?", 1, 10, 5)

        col1, col2 = st.columns(2)
        with col1:
            steps_today = st.number_input("Steps Today", min_value=0, step=100, value=1000)
            steps_goal = st.number_input("Steps Goal", min_value=1000, step=500, value=5000)
            st.progress(min(steps_today / steps_goal, 1.0))
        with col2:
            sleep_hours = st.slider("Sleep Hours Last Night", 0, 12, 7)
            st.write(f"You slept {sleep_hours} hours")

        st.subheader("Work Plans")
        st.caption("Your Plan This Weekend")
        exercise_days = st.number_input("Exercise days this week", min_value=0, max_value=7)
        exercise_type = st.selectbox("Exercise type", ["Cardio", "Strength", "Yoga", "Pilates", "Mixed"])
        rest_day = st.selectbox("Rest day", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        session_length = st.slider("Session length (minutes)", 10, 120, 30)
        nutrition_goal = st.text_input("Nutrition goal")
        new_habit = st.text_input("New healthy habit")

        st.subheader("Health Metrics")
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0)
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0)
        if height > 0 and weight > 0:
            bmi = weight / ((height / 100) ** 2)
            st.write(f"Your BMI: {bmi:.2f}")

        systolic = st.number_input("Blood Pressure Systolic", min_value=80, max_value=200)
        diastolic = st.number_input("Blood Pressure Diastolic", min_value=50, max_value=120)
        st.write(f"Blood Pressure: {systolic}/{diastolic} mmHg")

        tomorrow = today + datetime.timedelta(days=1)
        st.subheader("Upcoming Appointment")
        st.write(f"Next Checkup: {tomorrow.strftime('%A, %B %d, %Y')}")

        st.markdown(
            "<p style='text-align:center; color:white;'><i>Take care of your body. It's the only place you have to live.</i> — Jim Rohn</p>",
            unsafe_allow_html=True
        )

    # ---------------- GOALS ----------------
    elif page == "Goals":
        st.markdown("<h2 style='color:white;'>Set Your Health Goals</h2>", unsafe_allow_html=True)

        if st.session_state["submitted_goals"] is None:
            q1 = st.text_area("Small step you can start today")
            q2 = st.text_area("Habit you want to change")
            q3 = st.text_area("How you want to feel at the end of the year")
            q4 = st.text_area("Possible challenge")
            q5 = st.text_area("Support system")
            q6 = st.text_area("Health win you want")

            if st.button("Submit Goals"):
                if all([q1,q2,q3,q4,q5,q6]):
                    st.session_state["submitted_goals"] = {
                        "Step": q1,
                        "Habit": q2,
                        "Feeling": q3,
                        "Challenge": q4,
                        "Support": q5,
                        "Health Win": q6
                    }
                    st.success("Goals submitted!")
                else:
                    st.error("Please complete all fields.")
        else:
            st.subheader("Your Goals")
            for key,val in st.session_state["submitted_goals"].items():
                st.write(f"**{key}:** {val}")

    # ---------------- HEALTHY TIPS ----------------
    elif page == "Healthy Tips":
        st.markdown("<h2 style='color:white;'>Healthy Habits</h2>", unsafe_allow_html=True)
        st.subheader("Nutrition")
        st.write("Eat balanced meals with fruits, vegetables, and protein.")
        st.write("Limit sugary drinks and fast food.")
        st.write("Drink 6–8 glasses of water daily.")

        st.subheader("Movement")
        st.write("Exercise or walk for 20–30 minutes daily.")

        st.subheader("Sleep")
        st.write("Aim for 7–9 hours of sleep each night.")

        st.subheader("Stress")
        st.write("Practice breathing, meditation, or journaling.")

    # ---------------- TASKS STATUS ----------------
    elif page == "Tasks Status":
        st.markdown("<h2 style='color:white;'>Tasks Status</h2>", unsafe_allow_html=True)
        st.markdown("## Tasks & Progress Tracker")

        st.markdown("### 📅 This Month's Data")
        st.write(f"Current Date: {datetime.date.today().strftime('%B %d, %Y')}")

        st.markdown("### 📅 This Year's Data")
        st.write("Year: 2026")

        st.markdown("### 📊 Records")
        records_data = {
            "Metrics": [
                "Perfect Days",
                "Best Streaks",
                "Total Tasks Completed",
                "Tasks Completed This Month",
                "Overall Rate",
                "Monthly Rate"
            ],
            "Values": [
                "0 Days",
                "0 Days",
                "0",
                "0",
                "0%",
                "0%"
            ]
        }
        st.table(records_data)

    # ---------------- ABOUT ----------------
    elif page == "About":

     st.markdown("<h2 style='text-align:center; color:white;'>About This App</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:white;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='color:white;'>Purpose of the App</h3>", unsafe_allow_html=True)
    st.write(
        "This app is designed to help users organize and monitor their health and daily routines in one platform. "
        "It allows users to set and track personal goals, monitor health metrics such as steps, sleep, BMI, and blood pressure, "
        "and encourages healthy habits through structured inputs and reminders."
    )

    st.markdown("<h3 style='color:white;'>Target Users</h3>", unsafe_allow_html=True)
    st.write(
        "The app is suitable for students, professionals, and anyone aiming to improve their lifestyle. "
        "It supports users who want to maintain consistent health routines, track progress, and achieve specific health goals."
    )

    st.markdown("<h3 style='color:white;'>Inputs Collected</h3>", unsafe_allow_html=True)
    st.write(
        "Users provide their username, password, age, and upload a profile picture during sign-up. "
        "Inside the app, users can input their mood, steps, sleep hours, exercise routines, nutrition goals, "
        "new habits, and yearly personal health goals."
    )

    st.markdown("<h3 style='color:white;'>Outputs Displayed</h3>", unsafe_allow_html=True)
    st.write(
        "The app displays personalized information including the username, profile picture, progress charts for steps, sleep, and BMI, "
        "submitted goals, and health metrics."
    )
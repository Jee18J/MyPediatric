import streamlit as st
import json
import os
import uuid
import hashlib
from datetime import datetime

# Main UI configuration with custom theme
st.set_page_config(
    page_title="Parent Forum Blog",
    layout="wide",
    page_icon="👪",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for better UI ---
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@500&display=swap');
        html, body, [class*="stApp"] {
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
            font-size: 1.08rem;
            color: #22304a;
        }
        :root {
            --primary: #2563eb;
            --secondary: #38bdf8;
            --accent: #22c55e;
            --background: #f4faff;
            --card: #ffffff;
            --text: #22304a;
            --text-light: #4A5568;
            --warning: #ef4444;
            --success: #22c55e;
            --info: #2563eb;
            --border-radius: 16px;
            --box-shadow: 0 4px 24px rgba(37, 99, 235, 0.08);
            --transition: all 0.2s cubic-bezier(.4,0,.2,1);
        }
        .stApp {
            background-color: var(--background) !important;
        }
        .main .block-container {
            background-color: var(--background);
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .header-container {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 2.5rem 1.5rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            box-shadow: var(--box-shadow);
            color: #fff;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .header-container h1, .header-container p {
            color: #fff !important;
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
        }
        .card, .blog-card {
            background: var(--card);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 1.5rem 1.5rem 1.2rem 1.5rem;
            margin-bottom: 1.2rem;
            border: 1px solid #e3eaf3;
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
        }
        .stButton>button {
            background: linear-gradient(90deg, var(--primary) 60%, var(--secondary) 100%);
            color: #fff !important;
            font-size: 1.13rem;
            font-weight: 700;
            border-radius: var(--border-radius);
            padding: 0.85rem 2.2rem;
            border: none;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.10);
            transition: var(--transition);
            letter-spacing: 0.01em;
            outline: none !important;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .stButton>button:hover, .stButton>button:focus {
            background: linear-gradient(90deg, var(--secondary) 0%, var(--primary) 100%);
            color: #fff !important;
            box-shadow: 0 4px 16px rgba(37, 99, 235, 0.18);
            transform: translateY(-2px) scale(1.03);
        }
        .stButton>button:active {
            transform: scale(0.98);
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            border-radius: var(--border-radius) !important;
            padding: 12px 14px !important;
            border: 1.5px solid #dbeafe !important;
            font-size: 1.08rem;
            color: var(--text);
            background: #fff;
            transition: var(--transition);
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.13) !important;
        }
        .notification {
            background: rgba(37, 99, 235, 0.07);
            border-left: 5px solid var(--info);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            color: var(--primary);
            font-weight: 600;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .blog-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 0.5rem;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .blog-meta {
            color: var(--text-light);
            font-size: 0.85rem;
            margin-bottom: 1rem;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .blog-content {
            color: var(--text);
            line-height: 1.6;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .footer {
            text-align: center;
            padding: 1.5rem;
            color: var(--text-light);
            font-size: 0.95rem;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        @media (max-width: 768px) {
            .header-container {
                padding: 1.5rem 0.5rem;
            }
            .card, .blog-card {
                padding: 1rem;
            }
            .stButton>button {
                padding: 0.7rem 1.2rem;
                font-size: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# --- Configuration ---
USERS_FILE = "pages/simulated_users.json"
BLOGS_FILE = "pages/blogs.json"
NOTIFICATIONS_FILE = "pages/simulated_blog_notifications.json"

# --- Load condition list from model prediction classes ---
CONDITIONS = [
    "Common Cold", "Gastroenteritis", "Asthma", "Meningitis",
    "Scarlet Fever", "Eczema", "Croup", "Type 1 Diabetes",
    "Bronchiolitis", "Influenza", "Pneumonia",
    "Allergies", "Ear Infection", "Skin Rash", "Diarrhea", "Fever", "Viral Illness"
]

# --- Helper Functions for Data Persistence ---
def load_data(filename, default_value):
    """Loads data from a JSON file."""
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default_value, f)
        return default_value

    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            if not isinstance(data, type(default_value)):
                st.error(f"Data file {filename} is corrupted or not the expected type. Resetting.")
                data = default_value
                save_data(data, filename)
            return data
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from {filename}. File might be corrupted. Resetting.")
        data = default_value
        save_data(data, filename)
        return data
    except Exception as e:
        st.error(f"An error occurred loading data from {filename}: {e}")
        data = default_value
        save_data(data, filename)
        return data

def save_data(data, filename):
    """Saves data to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"An error occurred saving data to {filename}: {e}")

# --- Simple Password Hashing (for simulation) ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_hash, provided_password):
    return stored_hash == hash_password(provided_password)

# --- Load Data ---
users = load_data(USERS_FILE, {})
blogs_data = load_data(BLOGS_FILE, {})
notifications = load_data(NOTIFICATIONS_FILE, {})

# Ensure all conditions exist in blogs_data
for condition in CONDITIONS:
    if condition not in blogs_data:
        blogs_data[condition] = []
    elif not isinstance(blogs_data[condition], list):
        st.error(f"Data for condition '{condition}' in {BLOGS_FILE} is corrupted or not a list. Resetting.")
        blogs_data[condition] = []
        save_data(blogs_data, BLOGS_FILE)

# --- Initialize Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'show_create_post' not in st.session_state:
    st.session_state.show_create_post = False

# --- Authentication Logic ---
def login_form():
    with st.container():
        st.markdown('<div class="header"><h2>👋 Welcome Back</h2></div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            col1, col2 = st.columns([1, 3])
            with col1:
                login_submitted = st.form_submit_button("Login", type="primary")
            with col2:
                st.write("Don't have an account? Register below.")
            
            if login_submitted:
                if username in users:
                    if check_password(users[username]['password_hash'], password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_id = users[username]['user_id']
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
                else:
                    st.error("Username not found. Please register.")

def register_form():
    with st.container():
        st.markdown('<div class="header"><h2>✍️ Create an Account</h2></div>', unsafe_allow_html=True)
        
        with st.form("register_form"):
            new_username = st.text_input("Choose a Username", key="register_username")
            new_password = st.text_input("Create a Password", type="password", key="register_password")
            
            register_submitted = st.form_submit_button("Register", type="primary")
            
            if register_submitted:
                if not new_username or not new_password:
                    st.warning("Please enter both a username and password.")
                elif new_username in users:
                    st.error("Username already exists. Please choose another.")
                else:
                    user_id = str(uuid.uuid4())
                    users[new_username] = {
                        'user_id': user_id,
                        'password_hash': hash_password(new_password)
                    }
                    save_data(users, USERS_FILE)
                    st.success("Registration successful! You can now log in.")

# --- Helper to get username from user_id ---
def get_username_from_userid(user_id):
    for username, user_info in users.items():
        if user_info.get('user_id') == user_id:
            return username
    return "Unknown User"

# --- Blog Content Display ---
def display_blog_post(blog, condition_to_display):
    with st.expander(f"📌 {blog['title']} - {blog['timestamp']} by {get_username_from_userid(blog['user_id'])}"):
        st.markdown(f'<div class="blog-content">{blog["content"]}</div>', unsafe_allow_html=True)
        
        # Check if user is logged in and hasn't reported this post
        can_report = False
        if st.session_state.logged_in and st.session_state.user_id != blog['user_id']:
            # Disable report if user already reported
            already_reported = st.session_state.user_id in blog.get('reporters', [])
            can_report = not already_reported
            
            if st.button("⚠️ Report This Post", key=f"report_post_{blog['id']}", disabled=already_reported):
                # Report logic
                user_id = st.session_state.user_id
                # Initialize reporters list if not present
                if 'reporters' not in blog:
                    blog['reporters'] = []
                if 'report_count' not in blog:
                    blog['report_count'] = 0
                
                if user_id not in blog['reporters']:
                    # Add user to reporters
                    blog['reporters'].append(user_id)
                    blog['report_count'] = len(blog['reporters'])
                    
                    # Check if report count >= 5
                    if blog['report_count'] >= 5:
                        # Delete post
                        blogs_list = blogs_data[condition_to_display]
                        blogs_data[condition_to_display] = [p for p in blogs_list if p['id'] != blog['id']]
                        save_data(blogs_data, BLOGS_FILE)
                        
                        # Notify the author
                        poster_username = get_username_from_userid(blog['user_id'])
                        if poster_username:
                            notification_message = f"Your post '{blog['title']}' was deleted after multiple reports."
                            notification_id = str(uuid.uuid4())
                            if poster_username not in notifications:
                                notifications[poster_username] = []
                            notifications[poster_username].append({
                                'id': notification_id,
                                'message': notification_message,
                                'read': False,
                                'user_id': blog['user_id']
                            })
                            save_data(notifications, NOTIFICATIONS_FILE)
                        
                        st.success("Post has been deleted due to multiple reports. The author has been notified.")
                        st.rerun()
                    else:
                        # Save report info
                        save_data(blogs_data, BLOGS_FILE)
                        # Optional: Show feedback
                        st.success("Post reported. Thank you for helping keep the community safe.")
                        st.rerun()
                else:
                    st.info("You have already reported this post.")
        elif not st.session_state.logged_in or st.session_state.user_id == blog['user_id']:
            # No report button for author's own posts or if not logged in
            pass

        st.markdown('</div>', unsafe_allow_html=True)

# --- Blog and Notification Logic ---
def show_blog_content():
    # Header
    st.markdown('<div class="header"><h1>👪 Parent Forum Blog</h1></div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #7f8c8d;">Share your experiences and connect with other parents</p>', unsafe_allow_html=True)
    
    current_username = st.session_state.username
    current_user_id = st.session_state.user_id

    # Notifications section - CHANGED THIS PART
    if current_username in notifications:
        user_notifications = notifications[current_username]
        # Only show notifications where the current user is the intended recipient (user_id matches)
        unread_notifications = [n for n in user_notifications if not n['read']]

        if unread_notifications:
            st.markdown('<div class="header"><h3>🔔 Your Notifications</h3></div>', unsafe_allow_html=True)
            for notif in unread_notifications:
                with st.container():
                    st.markdown(f'<div class="notification">{notif["message"]}</div>', unsafe_allow_html=True)
                    if st.button("✔️ Mark as Read", key=f"close_notification_{notif['id']}"):
                        for existing_notif in notifications[current_username]:
                            if existing_notif['id'] == notif['id']:
                                existing_notif['read'] = True
                                break
                        save_data(notifications, NOTIFICATIONS_FILE)
                        st.rerun()

    col1, col2, col3 = st.columns([1, 2, 1])  # Creates a centered column
    with col1:
        pass
    with col2:
        if st.session_state.logged_in:
            if st.button("✍️ Create a New Post sharing you experiences", 
                         key="create_post_toggle",
                         use_container_width=True):
                st.session_state.show_create_post = not st.session_state.show_create_post
                st.rerun()
                with col3:
                    pass

    # Blog Posting Form
    if st.session_state.show_create_post and st.session_state.logged_in:
        with st.container():
            st.markdown('<div class="blog-card">', unsafe_allow_html=True)
            st.markdown('<h3>✏️ Create New Post</h3>', unsafe_allow_html=True)
            
            with st.form("new_post_form"):
                selected_condition_post = st.selectbox("Condition", options=CONDITIONS, key="new_blog_condition")
                new_blog_title = st.text_input("Post Title", key="new_blog_title")
                new_blog_content = st.text_area("Share Your Experience", height=200, key="new_blog_content")
                
                col_submit, col_cancel, _ = st.columns([1, 1, 4])
                with col_submit:
                    submit_post = st.form_submit_button("Publish Post", type="primary")
                with col_cancel:
                    cancel_post = st.form_submit_button("Cancel")
                
                if submit_post:
                    if selected_condition_post and new_blog_title.strip() and new_blog_content.strip():
                        if selected_condition_post not in blogs_data:
                            blogs_data[selected_condition_post] = []

                        blog_entry = {
                            "id": str(uuid.uuid4()),
                            "title": new_blog_title.strip(),
                            "content": new_blog_content.strip(),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "user_id": st.session_state.user_id
                        }
                        blogs_data[selected_condition_post].append(blog_entry)
                        save_data(blogs_data, BLOGS_FILE)
                        st.success("Your post has been published!")
                        st.session_state.show_create_post = False
                        st.rerun()
                    else:
                        st.warning("Please fill in both title and content.")
                
                if cancel_post:
                    st.session_state.show_create_post = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Blog Post Browser
    st.markdown('<div class="header"><h2>🔍 Browse Posts by Condition</h2></div>', unsafe_allow_html=True)
    
    selected_category_browse = st.selectbox(
        "Select a condition to view posts",
        options=["Select a Condition"] + sorted(list(blogs_data.keys())),
        key="browse_category"
    )

    st.markdown("---")

    # Display Blogs for Selected Category
    if selected_category_browse != "Select a Condition":
        condition_to_display = selected_category_browse
        blogs = blogs_data.get(condition_to_display, [])

        if blogs:
            st.markdown(f'<h3>🩺 Posts about {condition_to_display}</h3>', unsafe_allow_html=True)
            
            for blog in reversed(blogs):
                display_blog_post(blog, condition_to_display)
        else:
            st.info(f"No posts yet for '{condition_to_display}'. Be the first to share your experience!")
    else:
        st.info("Select a condition from the dropdown above to view related posts.")

    # Logout Button
    st.markdown("---")
    if st.session_state.logged_in:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.session_state.show_create_post = False
            st.success("Logged out successfully.")
            st.rerun()

# --- Main App Flow ---
if st.session_state.logged_in:
    show_blog_content()
else:
    # Welcome header
    st.markdown("""
    <div class="header-container">
        <h1 style="margin:0;padding:0;">👪 Parent Forum Blog</h1>
        <p style="margin:0;padding-top:0.5rem;font-size:1.1rem;">A safe space for parents to share experiences and support each other</p>
    </div>
    """, unsafe_allow_html=True)

    # Welcome content card
    st.markdown("""
    <div class="card">
        <h2 style="color: var(--primary); margin-bottom: 1rem;">Welcome to Parent Forum</h2>
        <p style="color: var(--text); font-size: 1.1rem; margin-bottom: 1rem;">
            A safe space for parents to share experiences, ask questions, 
            and support each other through childhood health journeys.
        </p>
        <p style="color: var(--text); font-size: 1.1rem;">
            Join our community to connect with other parents facing similar challenges.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Login and Registration in cards
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        login_form()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        register_form()
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Parent Forum Blog | A community support platform</p>
    <p>Powered by Streamlit | All content is user-generated</p>
</div>
""", unsafe_allow_html=True)

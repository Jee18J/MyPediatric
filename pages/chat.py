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
        /* Main container styling */
        .main {
            background-color: #f9f9f9;
        }
        
        /* Header styling */
        .header {
            color: #2c3e50;
            padding: 1rem 0;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Blog post cards */
        .blog-card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .blog-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .blog-title {
            color: #2c3e50;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .blog-meta {
            color: #7f8c8d;
            font-size: 0.85rem;
            margin-bottom: 1rem;
        }
        
        .blog-content {
            color: #34495e;
            line-height: 1.6;
        }
        
        /* Notification styling */
        .notification {
            background-color: #fff8e1;
            border-left: 4px solid #ffc107;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0 4px 4px 0;
        }
        
        /* Form styling */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 8px !important;
            padding: 10px !important;
        }
        
        /* Condition selector */
        .stSelectbox>div>div>select {
            border-radius: 8px !important;
            padding: 8px !important;
        }
        
        /* Footer styling */
        .footer {
            color: #7f8c8d;
            font-size: 0.85rem;
            text-align: center;
            padding: 1.5rem 0;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .blog-card {
                padding: 1rem;
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
    with st.expander(f"📌 {blog['title']} - Posted on {blog['timestamp']} by {get_username_from_userid(blog['user_id'])}"):
        st.markdown(f'<div class="blog-content">{blog["content"]}</div>', unsafe_allow_html=True)
        
        # Report button for other users' posts
        if st.session_state.logged_in and st.session_state.user_id != blog['user_id']:
            if st.button("⚠️ Report This Post", key=f"report_post_{blog['id']}"):
                deleted_post_owner_id = blog['user_id']
                deleted_post_title = blog['title']
                deleted_post_id = blog['id']
                reported_by_username = st.session_state.username

                # Perform deletion
                blogs_data[condition_to_display] = [p for p in blogs_data[condition_to_display] if p['id'] != deleted_post_id]
                save_data(blogs_data, BLOGS_FILE)

                # Create notification
                poster_username = get_username_from_userid(deleted_post_owner_id)

                if poster_username:
                    notification_message = f"Your post '{deleted_post_title}' was reported and removed by {reported_by_username}."
                    notification_id = str(uuid.uuid4())

                    if poster_username not in notifications:
                        notifications[poster_username] = []

                    notifications[poster_username].append({
                        'id': notification_id,
                        'message': notification_message,
                        'read': False,
                        'user_id': deleted_post_owner_id
                    })
                    save_data(notifications, NOTIFICATIONS_FILE)

                    st.success(f"Post reported and removed. The original poster will be notified.")
                    st.rerun()
                else:
                    st.error("Could not find the original poster's username to send a notification.")
                    st.rerun()
        
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
    # Splash page for non-logged-in users
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="padding: 2rem;">
            <h1 style="color: #2c3e50;">👪 Welcome to Parent Forum</h1>
            <p style="color: #7f8c8d; font-size: 1.1rem;">
                A safe space for parents to share experiences, ask questions, 
                and support each other through childhood health journeys.
            </p>
            <p style="color: #7f8c8d; font-size: 1.1rem;">
                Join our community to connect with other parents facing similar challenges.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        login_form()
        st.markdown("---")
        register_form()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Parent Forum Blog | A community support platform</p>
    <p>Powered by Streamlit | All content is user-generated</p>
</div>
""", unsafe_allow_html=True)
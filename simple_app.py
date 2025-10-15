import streamlit as st

st.title("🤖 AI Schedule Assistant")
st.write("Hello! Welcome to the AI Schedule Assistant.")

# Simple input form
user_input = st.text_input("Enter your schedule request:", placeholder="e.g., Hospital appointment 2 hours")

if st.button("Analyze"):
    st.success(f"Your request: {user_input}")
    st.info("AI is analyzing optimal time...")

# Sidebar
with st.sidebar:
    st.header("📅 Current Schedule")
    st.write("No scheduled events for today.")
    
    st.header("⚙️ Settings")
    demo_mode = st.checkbox("Demo mode", value=True)
    if demo_mode:
        st.success("Demo mode is activated.")

# app.py

import streamlit as st
from src.fetch_github import get_repo_details
from src.analyze_readme import summarize_readme
from src.detect_tech import detect_tech_stack

st.title("GitHub Project Analyzer 🚀")

# User input for GitHub repository URL
repo_url = st.text_input("Enter GitHub Repository URL:")

if st.button("Analyze"):
    if repo_url:
        with st.spinner("Fetching project details..."):
            readme_content, stats, contributors, file_list = get_repo_details(repo_url)
            summary = summarize_readme(readme_content)
            tech_stack = detect_tech_stack(readme_content, file_list)  # Pass file_list here
            # Display results
            st.subheader("📖 Project Summary")
            st.write(summary)

            st.subheader("🛠 Tech Stack")
            st.write(tech_stack)

            st.subheader("📊 Popularity Metrics")
            st.json(stats)

            st.subheader("👨‍💻 Top Contributors")
            st.write(", ".join(contributors) if contributors else "No contributors found.")

            st.subheader("📂 Repository Files")
            if file_list:
                st.write("\n".join(file_list))
            else:
                st.write("No files found or error fetching file list.")
    else:
        st.warning("⚠️ Please enter a valid GitHub repository URL.")
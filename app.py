# app.py

import streamlit as st
from src.fetch_github import get_repo_details
from src.analyze_readme import summarize_readme, summarize_file
from src.detect_tech import detect_tech_stack

st.title("GitHub Project Analyzer 🚀")

# User input for GitHub repository URL
repo_url = st.text_input("Enter GitHub Repository URL:")

# Comprehensive list of coding file extensions
CODING_EXTENSIONS = {
    # Python
    '.py', '.pyw',
    # R
    '.r', '.R',
    # JavaScript/TypeScript
    '.js', '.jsx', '.ts', '.tsx',
    # Java
    '.java',
    # C/C++
    '.c', '.cpp', '.cxx', '.cc', '.h', '.hpp', '.hxx',
    # C#
    '.cs',
    # Ruby
    '.rb',
    # Go
    '.go',
    # Rust
    '.rs',
    # PHP
    '.php', '.phtml',
    # Swift
    '.swift',
    # Kotlin
    '.kt', '.kts',
    # Scala
    '.scala', '.sc',
    # Perl
    '.pl', '.pm',
    # Lua
    '.lua',
    # Shell/Bash
    '.sh', '.bash',
    # SQL
    '.sql',
    # Haskell
    '.hs',
    # Dart
    '.dart',
    # Julia
    '.jl',
    # MATLAB/Octave
    '.m',
    # Fortran
    '.f', '.for', '.f90',
    # Assembly
    '.asm', '.s',
    # Groovy
    '.groovy',
    # Elixir
    '.ex', '.exs',
    # Clojure
    '.clj', '.cljs', '.cljc'
    # Add more as needed
}

if st.button("Analyze"):
    if repo_url:
        with st.spinner("Fetching and analyzing project details..."):
            readme_content, stats, contributors, file_contents = get_repo_details(repo_url)
            summary = summarize_readme(readme_content)
            tech_stack = detect_tech_stack(readme_content, list(file_contents.keys()))

            # Filter for coding files and summarize non-empty ones
            file_summaries = {}
            for file_path, content in file_contents.items():
                # Check if it's a coding file
                if any(file_path.lower().endswith(ext) for ext in CODING_EXTENSIONS):
                    # Skip if content is empty or only whitespace
                    if content.strip():
                        file_summaries[file_path] = summarize_file(file_path, content)

        # Display results
        st.subheader("📖 Project Summary")
        st.write(summary)

        st.subheader("🛠 Tech Stack")
        st.write(tech_stack)

        st.subheader("📊 Popularity Metrics")
        st.json(stats)

        st.subheader("👨‍💻 Top Contributors")
        st.write(", ".join(contributors) if contributors else "No contributors found.")

        st.subheader("📂 Detailed File Overview (Coding Files Only)")
        if file_summaries:
            # Prioritize main.py or app.py
            main_files = ['main.py', 'app.py']
            ordered_files = []
            for main_file in main_files:
                if main_file in file_summaries:
                    ordered_files.append(main_file)
            # Add remaining coding files
            ordered_files.extend([f for f in file_summaries.keys() if f not in main_files])

            for file_path in ordered_files:
                with st.expander(f"File: {file_path}"):
                    st.write(file_summaries[file_path])
        else:
            st.write("No non-empty coding files found or error fetching contents.")
    else:
        st.warning("⚠️ Please enter a valid GitHub repository URL.")
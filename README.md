# GitHub Project Analyzer

![GitHub Project Analyzer](https://img.shields.io/badge/Streamlit-App-blue) ![Python](https://img.shields.io/badge/Python-3.8+-yellow) ![License](https://img.shields.io/badge/License-MIT-green)

A Streamlit-based web application that analyzes GitHub repositories by fetching and summarizing their contents. It provides insights into the project's README, tech stack, popularity metrics, contributors, and a detailed overview of coding files.

## Features

- **README Summary**: Generates a concise summary of the repository's README using the Groq API.
- **Tech Stack Detection**: Identifies programming languages and technologies used in the repo based on file extensions and README content.
- **Popularity Metrics**: Displays stars, forks, and watchers from GitHub.
- **Top Contributors**: Lists up to 5 top contributors to the repository.
- **Coding Files Overview**: Summarizes the purpose of non-empty coding files (e.g., `.py`, `.R`, `.js`), prioritizing `main.py` or `app.py`.

## Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system.
- **Git**: Required to clone and manage the repository.
- **API Keys**:
  - **GitHub API Key**: For fetching repository data.
  - **Groq API Key**: For summarizing content.

## Setup

Follow these steps to set up and run the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/tulsicodes/Project-Analyzer-From-Github.git
   cd Project-Analyzer-From-Github

2. **Install Dependencies: Install the required Python packages:**:
   ```bash
   pip install -r requirements.txt

**The requirements.txt file contains**:
streamlit
requests
python-dotenv

3. **Set Up Environment Variables: Create a .env file in the project root with your API keys**:
    ```bash
    echo GITHUB_API_KEY=your_github_token > .env
    echo GROQ_API_KEY=your_groq_token >> .env
4. **Run the Application**:
    ```bash
    streamlit run app.py
5. **Commit and Push**:
    ```bash
    git add .
    git commit -m "Adding all the files"
    git push origin main
## Images of the Project
![image](https://github.com/user-attachments/assets/649c052f-cd4f-4cf0-a6a2-8d3691f266f7)
![image](https://github.com/user-attachments/assets/3586e1f4-130a-43b1-8732-531968118320)


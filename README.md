# Reddit Data Collection

## Assignment Overview
This assignment demonstrates how to collect Reddit posts using the Reddit API and the PRAW library. It retrieves trending posts and keyword-based search results from selected subreddits, extracts relevant metadata, and exports the cleaned dataset to a CSV file for further analysis.

---

## How to Run

### Prerequisites
Before you begin, make sure you have the following installed:
- **Python 3.8+**
- **pip** (Python package manager)
- A valid Reddit Developer Account to generate API credentials

---

## Installation
Clone or download this repository, then install all required dependencies:

**pip install -r requirements.txt**

---

## Configuration
You need to create a .env file in the same directory as your script to store your Reddit API credentials securely.

**CLIENT_ID**=Your Reddit app's client ID (found under your app name)
**CLIENT_SECRET**=Your Reddit app's client secret (the secret key)
**USERNAME**=Your Reddit username
**PASSWORD**=Your Reddit password
**USER_AGENT**=User agent string (describe your app) 
Format: "AppName/Version by YourUsername"

---

## Execution

To run the Reddit data collection script, use the following command in your terminal

**python reddit_code.py**

The script will:
Collect trending posts from your selected subreddits.
Perform keyword-based searches (e.g., "GPT-4").
Clean and deduplicate the data.
Save all results to a CSV file named reddit_data.csv

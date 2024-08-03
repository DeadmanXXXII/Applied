# Applied

## Job Application Automation Script

This Python script automates job applications by monitoring your Gmail account for job posting emails and filling out application forms using information from your GitHub profile.

## Prerequisites

### Gmail API Setup

1. **Create a Project in Google Developer Console**:
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Click on the project drop-down and select "New Project".
    - Enter a name for your project and click "Create".

2. **Enable the Gmail API**:
    - In the Google Cloud Console, go to the [API Library](https://console.cloud.google.com/apis/library).
    - Search for "Gmail API" and click on it.
    - Click "Enable".

3. **Create Credentials**:
    - In the left sidebar, click on "Credentials".
    - Click on "Create Credentials" and select "OAuth Client ID".
    - If prompted to set up the OAuth consent screen, click on "Configure consent screen".
        - Choose "External" for the user type.
        - Fill out the necessary fields (e.g., application name) and save.
    - Select "Desktop app" as the application type.
    - Click "Create".

4. **Download Credentials**:
    - After creating the OAuth Client ID, you'll be shown a dialog with your client ID and client secret.
    - Click "Download" to save the credentials file (`credentials.json`) to your computer.
    - Move the `credentials.json` file to your project directory where your script is located.

### GitHub API Setup

1. **Generate a Token**:
    - Go to [GitHub settings](https://github.com/settings/tokens).
    - Click "Generate new token".
    - Give your token a name (e.g., "Job Application Script").
    - Select the necessary scopes (for basic profile information, you usually only need `read:user`).
    - Click "Generate token".
    - Copy the generated token and save it securely. You won't be able to see it again.

### Install Required Libraries

Install the required Python libraries using pip:

```sh
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib selenium requests beautifulsoup4
```

### Install WebDriver

Download and install the Chrome WebDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/) and ensure it's in your PATH.

## Usage

1. **Configure the Script**:
    - Replace `"DeadmanXXXII"` with your GitHub username.
    - Replace `"your_github_token_here"` with your GitHub API token.
    - Ensure the `credentials.json` file is in the same directory as the script.

2. **Run the Script**:
    ```sh
    python your_script.py
    ```
    - The first time you run the script, it will open a browser window for you to authorize access to your Gmail account.
    - Once authorized, it will save the credentials and begin monitoring your Gmail for job application emails.

## Script Overview

The script performs the following steps:

1. **Authenticate with Gmail API**:
    - Uses OAuth 2.0 to authenticate and access your Gmail account.

2. **Monitor for Job Posting Emails**:
    - Checks for new emails with the subject "Job Posting" every 60 seconds.

3. **Parse Job Details**:
    - Extracts job details (company, position, application link) from the email snippet.

4. **Fetch GitHub Profile Information**:
    - Uses the GitHub API to fetch your profile information (name, bio, email, company, location, website).

5. **Fill Out Application Form**:
    - Uses Selenium to open the job application link and fill out the form with your GitHub profile information.

6. **Submit Application**:
    - Automatically submits the job application form.

## Important Notes

- Ensure your GitHub profile information is up-to-date.
- The script relies on the structure of the job application form. It may need adjustments for different form structures.
- The script saves your Gmail API credentials in a `token.pickle` file. Keep this file secure.

import base64
import os
import pickle
import re
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Gmail API setup
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

GITHUB_USERNAME = "DeadmanXXXII"
GITHUB_API_TOKEN = "your_github_token_here"  # Replace with your GitHub API token

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def check_new_job_emails(service):
    results = service.users().messages().list(userId='me', q='subject:Job Posting').execute()
    messages = results.get('messages', [])
    for msg in messages:
        msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        msg_snippet = msg['snippet']
        if 'apply now' in msg_snippet.lower():
            apply_for_job(msg)

def apply_for_job(message):
    job_details = parse_job_details(message['snippet'])
    github_info = get_github_info(GITHUB_USERNAME, GITHUB_API_TOKEN)
    submit_application(job_details, github_info)

def parse_job_details(message_snippet):
    job_details = {}
    job_details['company'] = re.search(r'Company:\s*(.*)', message_snippet).group(1)
    job_details['position'] = re.search(r'Position:\s*(.*)', message_snippet).group(1)
    job_details['application_link'] = re.search(r'apply here:\s*(http[s]?://\S+)', message_snippet).group(1)
    return job_details

def get_github_info(username, token):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Authorization": f"token {token}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
    github_info = {
        "name": data.get("name", ""),
        "bio": data.get("bio", ""),
        "email": data.get("email", ""),
        "company": data.get("company", ""),
        "location": data.get("location", ""),
        "website": data.get("blog", "")
    }
    return github_info

def submit_application(job_details, github_info):
    driver = webdriver.Chrome()
    driver.get(job_details['application_link'])
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'form')))
        form_fields = driver.find_elements(By.TAG_NAME, 'input')
        
        for field in form_fields:
            field_name = field.get_attribute('name').lower()
            if 'name' in field_name and github_info['name']:
                field.send_keys(github_info['name'])
            elif 'email' in field_name and github_info['email']:
                field.send_keys(github_info['email'])
            elif 'company' in field_name and github_info['company']:
                field.send_keys(github_info['company'])
            elif 'location' in field_name and github_info['location']:
                field.send_keys(github_info['location'])
            elif 'website' in field_name or 'url' in field_name and github_info['website']:
                field.send_keys(github_info['website'])
            elif 'bio' in field_name or 'about' in field_name and github_info['bio']:
                field.send_keys(github_info['bio'])
        
        submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
        submit_button.click()
    finally:
        driver.quit()

def main():
    service = get_gmail_service()
    while True:
        check_new_job_emails(service)
        time.sleep(60)

if __name__ == '__main__':
    main()

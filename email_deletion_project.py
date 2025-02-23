from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle
import tomli

def get_gmail_service(secrets_file="secrets.toml"):
    """Set up Gmail API service"""
    # Update SCOPES to include full mail access for deletion
    SCOPES = [
        'https://mail.google.com/',           # Full mail access
        'https://www.googleapis.com/auth/gmail.modify',  # Ability to modify mail
        'https://www.googleapis.com/auth/gmail.labels'   # Access to labels/categories
    ]
    
    try:
        # Load client credentials from secrets.toml
        with open(secrets_file, "rb") as f:
            secrets = tomli.load(f)
            
        client_id = secrets.get("oauth", {}).get("client_id")
        client_secret = secrets.get("oauth", {}).get("client_secret")
        
        if not client_id or not client_secret:
            print("Error: OAuth credentials missing in secrets file")
            return None
            
        creds = None
        
        # Load existing credentials if available
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials if needed
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json',
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
                
            # Save credentials for future use
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        # Build and return the Gmail service
        return build('gmail', 'v1', credentials=creds)
        
    except Exception as e:
        print(f"Error setting up Gmail service: {e}")
        return None

def delete_category_emails(service, category='promotions'):
    """Delete emails from specified category (promotions or social)"""
    try:
        total_deleted = 0
        next_page_token = None
        
        while True:
            # Search for emails in specified category
            results = service.users().messages().list(
                userId='me',
                q=f'category:{category}',
                maxResults=500,
                pageToken=next_page_token
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                if total_deleted == 0:
                    print(f'No {category} emails found.')
                break
                
            batch_size = 100
            current_batch_total = len(messages)
            
            # Delete messages in batches of 100
            for i in range(0, current_batch_total, batch_size):
                batch = messages[i:i + batch_size]
                batch_ids = {'ids': [msg['id'] for msg in batch]}
                
                service.users().messages().batchDelete(
                    userId='me',
                    body=batch_ids
                ).execute()
                
                total_deleted += len(batch)
                print(f'Deleted {total_deleted} {category} emails so far...')
            
            # Check if there are more pages
            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break
                
        print(f'Successfully deleted all {total_deleted} {category} emails.')
        
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    print("Gmail Category Cleanup")
    print("-----------------------")
    
    # Get Gmail service
    service = get_gmail_service()
    
    if service:
        print("Successfully connected to Gmail API")
        # Delete social emails
        delete_category_emails(service, 'social')
    else:
        print("Failed to set up Gmail service. Check your credentials.")

if __name__ == '__main__':
    main()
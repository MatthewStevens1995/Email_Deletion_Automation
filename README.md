```markdown
# Gmail Category Cleanup

A Python script that helps you bulk delete emails from Gmail's category tabs (Promotions and Social). This tool uses the Gmail API to efficiently delete hundreds or thousands of emails in batches, helping you clean up your inbox quickly and safely.

## Features

- Bulk delete emails from Gmail's Promotions tab
- Bulk delete emails from Gmail's Social tab
- Efficient batch processing (deletes emails in batches of 100)
- Pagination support (can handle any number of emails)
- Progress tracking during deletion
- Secure OAuth2 authentication
- Credentials persistence for convenience

## Prerequisites

- Python 3.6 or higher
- A Gmail account
- Google Cloud OAuth credentials (instructions below)

## Required Python Packages

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib tomli
```

## Setup

1. Clone or download this repository
2. Create a `secrets.toml` file in the project directory:
```toml
[oauth]
client_id = "your-client-id"
client_secret = "your-client-secret"
```

3. Set up Google Cloud OAuth:
   - Go to the [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable the Gmail API for your project
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop application"
   - Download the client secret file
   - Rename it to `client_secret.json` and place it in the project directory

## Usage

Run the script with Python:

```bash
python gmail_cleanup.py
```

On first run:
1. The script will open your default web browser
2. Log in to your Gmail account
3. Grant the requested permissions
4. The script will save the authentication token for future use

## File Structure

```
project_folder/
├── gmail_cleanup.py     # Main script
├── secrets.toml         # Your OAuth credentials
├── client_secret.json   # Downloaded from Google Cloud Console
└── token.pickle        # Generated after first authentication
```

## How It Works

The script:
1. Authenticates with Gmail using OAuth2
2. Searches for emails in the specified category (Promotions or Social)
3. Retrieves emails in batches of 500
4. Deletes them in smaller batches of 100
5. Continues until all matching emails are deleted
6. Provides progress updates throughout the process

## Security

- Uses OAuth2 for secure authentication
- No password storage required
- Credentials are stored locally
- Limited scope permissions (only what's needed for email deletion)

## Troubleshooting

1. If you get a "client_secret.json not found" error:
   - Make sure you've downloaded and correctly placed the OAuth credentials file
   - Ensure it's named exactly `client_secret.json`

2. If you get a permissions error:
   - Delete the `token.pickle` file
   - Run the script again
   - Re-authorize with the correct permissions

3. If the script seems to stop at 500 emails:
   - This is normal! The script processes emails in pages
   - It will automatically continue to the next page until all emails are deleted

## Contributing

Feel free to:
- Fork the repository
- Create a feature branch
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Disclaimer

Use this script responsibly. Deleted emails cannot be recovered. It's recommended to verify the script's behavior with a small number of emails first.
```

This README provides a comprehensive guide for users to understand, set up, and use the script effectively. It includes all necessary information while maintaining a professional and clear structure. Let me know if you'd like me to add or modify any sections!

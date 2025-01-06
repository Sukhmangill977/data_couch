# data_couch
 
# Email Training Request Automation

This project automates the process of handling training requests sent via email. It extracts relevant details, creates a Trello card for tracking, and sends email notifications to both the instructor and the client. The script leverages IMAP for email handling, NLP for extracting information, and Trello API for task management.

## Features

- **Email Processing**: Reads unseen emails from Gmail.
- **Natural Language Processing**: Extracts training type and proposed dates using spaCy.
- **Trello Integration**: Creates cards for training requests on a Trello board.
- **Email Notifications**: Sends confirmation emails to both the instructor and the client.

## Technologies Used

- **Python Libraries**: 
  - `imaplib`, `email`: Email handling.
  - `spacy`: Natural language processing.
  - `requests`: API communication with Trello.
  - `smtplib`, `email.mime`: Sending emails.
  - `re`: Regular expressions for date extraction.
  - `dotenv`: Loading environment variables.
- **Trello API**: Task management.
- **Gmail IMAP/SMTP**: Email fetching and sending.

## Prerequisites

1. **Python**: Install Python 3.8 or higher.
2. **Environment Variables**: Create a `.env` file in the root directory with the following variables:
   ```env
   EMAIL=<your-email-address>
   PASSWORD=<your-email-password>
   TRELLO_API_KEY=<your-trello-api-key>
   TRELLO_TOKEN=<your-trello-token>
   TRELLO_LIST_ID=<your-trello-list-id>
   BOARD_ID=<your-trello-board-id>
spaCy Model: Install the English NLP model for spaCy:
bash
Copy code
python -m spacy download en_core_web_sm
Installation
Clone this repository:
bash
Copy code
git clone https://github.com/your-repo/email-training-automation.git
Navigate to the project directory:


cd email-training-automation
Install dependencies:

pip install -r requirements.txt
Usage
Update the instructor's email in the script:
python

INSTRUCTOR_EMAIL = "example@gmail.com"
Run the script:

python script_name.py
The script will:
Fetch unseen emails from Gmail.
Extract training-related information.
Create Trello cards for valid requests.
Notify the instructor and client via email.
Error Handling
The script prints error messages for issues like:
Email fetching errors.
Trello API request failures.
Email sending errors.

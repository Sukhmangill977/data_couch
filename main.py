import imaplib
import email
from email.header import decode_header
import spacy
import re
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Gmail and Trello credentials from environment variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_LIST_ID = os.getenv("TRELLO_LIST_ID")
BOARD_ID = os.getenv("BOARD_ID")
INSTRUCTOR_EMAIL = "sukhmangill944@gmail.com"  # Update with instructor email

# Load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def extract_training_request(body):
    """
    Extract training-related details from the email body.
    """
    doc = nlp(body)
    training_details = {"training_type": None, "dates": None}

    # Look for training-related keywords
    for sentence in doc.sents:
        if "training" in sentence.text.lower():
            training_details["training_type"] = sentence.text.strip()

        # Basic date extraction
        date_match = re.search(r"\b(?:\d{1,2}(?:st|nd|rd|th)?[-/ ]?[A-Za-z]+[-/ ]?\d{4}|\b[A-Za-z]+\s\d{1,2},\s\d{4})\b", sentence.text)
        if date_match:
            training_details["dates"] = date_match.group(0)

    return training_details

def create_trello_card(title, description):
    """
    Create a new card on Trello.
    """
    url = "https://api.trello.com/1/cards"
    query = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
        "idList": TRELLO_LIST_ID,
        "name": title,
        "desc": description
    }

    response = requests.post(url, params=query)

    if response.status_code == 200:
        print("Card created successfully!")
    else:
        print("Failed to create card on Trello.")
        print("Response:", response.text)

def send_email(to_email, subject, body):
    """
    Send an email notification to the instructor or client.
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        
        text = msg.as_string()
        server.sendmail(EMAIL, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def read_emails():
    """
    Read unseen emails from Gmail and process training requests.
    """
    try:
        # Connect to the Gmail IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")  # Select the inbox

        # Search for all unseen emails
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        for e_id in email_ids:
            # Fetch the email
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Parse the email
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    sender = msg["From"]
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    print(f"From: {sender}")
                    print(f"Subject: {subject}")

                    # Email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                    else:
                        body = msg.get_payload(decode=True).decode()

                    print(f"Body: {body}")

                    # Process the email body to extract training request details
                    training_details = extract_training_request(body)
                    if training_details["training_type"]:
                        print(f"Training Type: {training_details['training_type']}")
                        print(f"Training Dates: {training_details['dates']}")

                        # Structure details for Trello card
                        title = f"Training Request: {training_details['training_type']}"
                        description = (
                            f"Request from: {sender}\n\n"
                            f"Details:\n{training_details['training_type']}\n"
                            f"Proposed Dates: {training_details['dates']}\n\n"
                            f"Full Email:\n{body}"
                        )

                        # Create a Trello card
                        create_trello_card(title, description)

                        # Send email to instructor
                        instructor_subject = "New Training Request"
                        instructor_body = f"A new training request has been received from {sender}.\n\nDetails:\n{training_details['training_type']}\nProposed Dates: {training_details['dates']}\n\nPlease review and confirm."
                        send_email(INSTRUCTOR_EMAIL, instructor_subject, instructor_body)

                        # Send email to the client confirming receipt
                        client_subject = "Training Request Received"
                        client_body = f"Dear {sender},\n\nThank you for your training inquiry. We have received your request for the training:\n{training_details['training_type']}\nProposed Dates: {training_details['dates']}\n\nOur team will get back to you soon with the available dates."
                        send_email(sender, client_subject, client_body)

                    else:
                        print("No training request detected.")

        # Close the connection
        mail.logout()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    read_emails()

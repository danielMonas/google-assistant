""" An automatic mail sorter using Gmail's API
# Made by Daniel Monastirski, January 2019 """

import os
import sys
import pickle
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from whitelist import Whitelist

class Sorter:
    """ Main class responsible for using Gmail's api directly """

    def __init__(self):
        self.scopes = 'https://www.googleapis.com/auth/gmail.modify'
        self.whitelist = Whitelist()
        self.service = build('gmail', 'v1', credentials=self.get_credentials())


    def get_credentials(self):
        """ Gets valid user credentials from storage. If nothing has been stored, or
            if the stored credentials are invalid, new credentials are created. """
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no valid credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.scopes)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def get_filtered_ids(self, query, label, user="me"):
        """ List all Messages of the user's mailbox matching the query.
            service: Authorized Gmail API service object.
            user_id: User's email address.
            query:   String to filter the messages by. """
        query = "from: {0} OR to: {0}".format(query)
        response = self.service.users().messages().list(userId=user, q=query).execute()
        ids = []
        if 'messages' in response:
            response = response['messages']
            ids.extend([msg['id'] for msg in response if not self.is_labeled(msg['id'], label)])
        while 'nextPageToken' in response:
            token = response['nextPageToken']
            response = self.service.users().messages().list(
                userId=user, q=query, pageToken=token).execute()['messages']
            ids.extend([msg['id'] for msg in response if not self.is_labeled(msg['id'], label)])
        return ids

    def is_labeled(self, msg_id, label, user_id="me"):
        """ Check if the message is already labeled """
        message = self.service.users().messages().get(userId=user_id, id=msg_id).execute()
        return label in message['labelIds']

    def init_queries(self, user="me"):
        """ Main feauture of the program - tag emails according to the settings file."""
        # Setting up data
        results = self.service.users().labels().list(userId='me').execute()
        labels = dict([l['name'], l['id']] for l in results.get('labels', []))
        settings = self.whitelist.get_dict()

        for query in settings.keys():
            print("\n\n[+] Current email query: " + query)
            msg_ids = self.get_filtered_ids(query, labels[settings[query]], user)
            print("[!] Located {0} messages: tagging as {1}".format(len(msg_ids), settings[query]))
            new_tags = {'removeLabelIds': [], 'addLabelIds': [labels[settings[query]]]}

            for index, msg in enumerate(msg_ids):
                try:
                    self.service.users().messages().modify(
                        userId=user, id=msg, body=new_tags).execute()
                    self.update_progress(len(msg_ids), index + 1)
                except errors.HttpError as error:
                    print('An error occurred: ' + error)

    def update_progress(self, total, completed):
        """ Generating a progress bar """
        bar_len = 50
        progress = round((completed / total) * 100, 2)
        block = int(bar_len * progress / 100)

        sys.stdout.write("\rProgress: [{0}]".format("#" * block + "-" * (bar_len - block)))
        if progress == 100.0:
            sys.stdout.write(" Completed.")
        else:
            sys.stdout.write(" {0}%".format(progress))
        sys.stdout.flush()

def main():
    """ Main function."""
    sorter = Sorter()
    sorter.init_queries()

if __name__ == '__main__':
    main()

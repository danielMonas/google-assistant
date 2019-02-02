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

    def get_filtered_ids(self, query, label):
        """ List all Messages of the user's mailbox matching the query.
            service: Authorized Gmail API service object.
            user_id: User's email address.
            query:   String to filter the messages by. """
        query = "from: {0} OR to: {0}".format(query)
        response = self.service.users().messages().list(userId='me', q=query).execute()
        ids = []
        if 'messages' in response:
            response = response['messages']
            ids.extend([msg['id'] for msg in response if not self.is_labeled(msg['id'], label)])
        while 'nextPageToken' in response:
            response = self.service.users().messages().list(
                userId='me', q=query, pageToken=response['nextPageToken']).execute()['messages']
            ids.extend([msg['id'] for msg in response if not self.is_labeled(msg['id'], label)])
        return ids

    def is_labeled(self, msg_id, label):
        """ Check if the message is already labeled """
        message = self.service.users().messages().get(userId='me', id=msg_id).execute()
        #print(message['internalDate'])
        return label in message['labelIds']

    def init_queries(self):
        """ Main feauture of the program - tag emails according to the settings file."""
        results = self.service.users().labels().list(userId='me').execute()
        labels = dict([l['name'], l['id']] for l in results.get('labels', []))
        settings = self.whitelist.get_settings()
        for tag, queries in settings.items():
            msg_ids = []
            print("\n\n[+] Current tag query: " + tag)
            for q in queries:
                print("[+] Searching for email query {0} ...".format(q))
                msg_ids += self.get_filtered_ids(q, labels[tag])
            print("[!] Located a total of {0} messages: tagging as {1}".format(len(msg_ids), tag))
            self.tag(msg_ids, {'removeLabelIds': [], 'addLabelIds': [labels[tag]]})

    def tag(self, msg_ids, new_tags):
        """ Tagging messages with new tags """
        for index, msg in enumerate(msg_ids):
            try:
                self.service.users().messages().modify(userId='me', id=msg, body=new_tags).execute()
                self.update_progress(len(msg_ids), index + 1)
            except errors.HttpError as error:
                print('An error occurred: ' + str(error))

    def update_progress(self, total, completed):
        """ Generating a progress bar """
        bar_len = 50
        progress = round((completed / total) * 100, 2)
        block = int(bar_len * progress / 100)
        # Creating a progress bar per each tagging query
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

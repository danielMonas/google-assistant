# Gmail assistant functions, using the Gmail API. May 2018
import httplib2
import os,sys
from apiclient import discovery,errors
from oauth2client import client,tools
from oauth2client.file import Storage
import argparse

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-assistant.json
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail assistant'
WHITELIST_FILE = os.path.dirname(os.path.abspath(__file__)) + "\\whitelist.dat"

def get_whitelist():
	"""Read from the whitelist data file and translate the data into a dictionary.
	The whitelist is data file containing the whitelist.Note that each line in the whitelist data file is excepted to be in the following format: <email address>,<label>"""
	file = open(WHITELIST_FILE,"r")
	file_txt = file.read().replace(',','\n').split("\n")
	file.close()
	return dict(zip(file_txt[::2],file_txt[1::2]))


def get_filtered_ids(service, query='',user_id="me"):
	"""List all Messages of the user's mailbox matching the query.
	Arguments:
			service: Authorized Gmail API service object.
			user_id: User's email address. The defualt value "me" indicates the authenticated user.
			query:   String to filter the messages by.
	Returns:ids:     A list of Message IDs of messages that match the query."""
	response = service.users().messages().list(userId=user_id,q=query).execute()
	ids = []
	if 'messages' in response:
		ids.extend([msg['id'] for msg in response['messages']])
	while 'nextPageToken' in response:
		page_token = response['nextPageToken']#
		response = service.users().messages().list(userId=user_id, q=query,pageToken=page_token).execute()
		ids.extend([msg['id'] for msg in response['messages']])
	return ids


def get_credentials():
	"""Gets valid user credentials from storage. If nothing has been stored, or if the stored credentials are invalid, the OAuth2 flow is completed to obtain the new credentials.
	Returns: the obtained credential."""
	credential_dir = os.path.join(os.path.expanduser('~'), '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,'gmail-assistant.json')
	store = Storage(credential_path)
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		print("Storing credentials to " + credential_path)
	return credentials


def create_msg_labels(label_id):
	"""Create object to update labels.
	Arguments:	label_id: The ID of the label to add to the message
	Returns: 		A label update object."""
	return {'removeLabelIds': [], 'addLabelIds': [label_id]}


def update_progress(total, completed):
    """ Function creates a loading progress bar.
    Arguments:
        total: the total amount of work to be done, represented as an integer.
        completed: An integer value between 0 and completed (included), representing the precentage completed."""
    barLength = 50
    progress = round((completed/total)*100,2)
    block = int(barLength*progress/100)

    sys.stdout.write("\rProgress: [{0}]".format( "#"*block + "-"*(barLength-block)))
    if progress == 100.0:
        sys.stdout.write(" Completed".format( "#"*block + "-"*(barLength-block)))
    else:
        sys.stdout.write(" {0}%".format(progress))
    sys.stdout.flush()


def init_queries():
	"""Shows basic usage of the Gmail API.
	Creates a Gmail API service object and outputs a list of label names of the user's Gmail account."""
	os.system('cls')
    # Setting up data
	credentials = get_credentials()
	service = discovery.build('gmail', 'v1', http=credentials.authorize(httplib2.Http()))
	labels = service.users().labels().list(userId='me').execute().get('labels', [])
	titles = [labels[x]['name'] for x in range(len(labels))]
	title_ids = [labels[x]['id'] for x in range(len(labels))]
	titles_dict = dict(zip(titles,title_ids))
	whitelist_dict = get_whitelist()

	for address_query in whitelist_dict.keys():
		print("\n\n-Current email query: " + address_query)
		msg_ids = get_filtered_ids(service,address_query)
		print("Located {0} messages:".format(len(msg_ids)))
		new_msg_labels = create_msg_labels(titles_dict[whitelist_dict[address_query]])
		print("Tagging as: " + whitelist_dict[address_query])
		for index in range(len(msg_ids)):
			try:
				service.users().messages().modify(userId="me", id=msg_ids[index],body=new_msg_labels).execute()
				update_progress(len(msg_ids), (index+1))
			except errors.HttpError as error:
				print('An error occurred: %s' % error)


def whitelist_menu():
	os.system('cls')
	menu_functions = [print_entries, add_entry, delete_entry]
	while(True):
		choice = 0
		print("1. Print settings")
		print("2. Add new entry")
		print("3. Delete an entry for future use")
		print("4. Go back")
		while(not(1 <= choice <= 4)):
			choice = int(input("Please choose an option: "))
		if(choice == 4):
			break
		menu_functions[choice - 1]()

def print_entries():
	contents = get_whitelist()
	print("TAG\t\t\tENTRY")
	for entry,tag in contents.items():
		print(tag + "\t"*int(len(tag)/4) + entry)

def add_entry():
	mail = input("Enter an email address: ")
	tag = input("Enter the appropriate tag: ")
	file = open(WHITELIST_FILE,"a+")
	file.write(mail + "," + tag + "\n")
	file.close()

def delete_entry():
	file = open(WHITELIST_FILE,"r+")
	lines = file.readlines()
	file.seek(0)
	unwanted = input("Enter line keywords to delete all matches:")
	for i in lines:
		if unwanted not in i:
			file.write(i)
	file.truncate()
	file.close()


def main():
	print("Hello, welcome to the Gmail Assistant V Beta, made by Daniel Monastirski")
	functions = [whitelist_menu,init_queries]
	while(True):
		user_choice = 0
		os.system('cls')
		print("1. Update settings file")
		print("2. Tag emails")
		print("3. Exit")
		while(not(1 <= user_choice <= 3)):
			user_choice = int(input("Please choose an option: "))
		if( user_choice == 3):
			break
		functions[user_choice-1]()
if __name__ == "__main__":
	main()

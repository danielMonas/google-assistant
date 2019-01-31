# Google Assistant

Several utilities to help the user handle several Google products, namely Gmail and Google Drive. 

## Gmail interface
The program uses the Gmail API to tag a user's mails automatically. 
You can choose what to tag and how, using the file ```settings.json```.
The file contains a json, constructed in the following format:
```json
{  
    "Tag": ["email1", "email2" ... ],  
    "AnotherTag": ["email3"]  
    ...  
}  
```
Notice the emails do not have to contain the entire email. For example, to tag 
```foo@bar.com```, ```foo123@bar.com```, and ```bar@baz.org``` under the tag "Work":
The following will search any email address containing the word "bar".
```json
{  
    "Work": ["bar"]  
}
```

"""
ShuttleCloud challenge: generate vCard for a given username and password from miniBook provider contact data
By Óscar Otero Martínez

"""

import requests
from bs4 import BeautifulSoup
import vobject

print(__doc__)

class Login(object):
    """
    Class that manages the log into MiniBook agenda for given username and password
    """

    def __init__(self):
        self.username = input('Usename: ')
        self.password = input('Password: ')
        self.url = 'https://minibook.improffice.com/accounts/login/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.s = requests.Session()

    def get_csf(self):
        """Get the needen csftoken to do the login
        :return: csftoken
        """
        # GET request to url
        r = self.s.get(self.url, headers=self.headers)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.find(type='hidden')['value'] if soup.find(type='hidden')['name'] == 'csrfmiddlewaretoken' else None

        return csrf

    def login_agenda(self):
        """Do POST request for the login
        :return: html agenda
        """
        # Generate user data
        data = dict(username=self.username, password=self.password, csrfmiddlewaretoken=self.get_csf())
        # Do post request
        page = self.s.post(url=self.url, data=data, headers=self.headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        # Feedback
        if 'Log Out' in soup.get_text():
            print('\nYou have successfully logged in!\n')
        else:
            raise ValueError('The Log In operation failed. Make sure your user data is right')

        return soup

class ParseHTML(object):
    """
    Parse the given html to obtain all the contacts
    """
    def __init__(self, page):
        self.page = page

    def get_contacts(self):
        """Get all the contacts information
        :return: list of dictionaries, each dictionary has each contact data
        """
        # Get all div elements
        divs = self.page.find_all('div')
        # Get the div where the contact info is stored
        contacts = [divs[i] for i in range(len(divs)) if
                    list(divs[i].attrs.keys())[0] == 'class' and divs[i].attrs['class'] == ['card-body']]
        # If the contacts list is empty then return
        if not contacts:
            print('There are no contacts stored!\n')
            return contacts
        # Get each contact information
        contacts_data = []
        for cn in contacts:
            contact = {}
            # get name
            contact.update({'name':cn.h5.string})
            # Get the data in array format
            arr = cn.get_text().split('\n')
            # Get phone and email (it is possible that the contact has none of this categories)
            for el in arr:
                if 'Number:' in el:
                    number = el.split('Number: ')
                    contact.update({'number':number[len(number)-1]})
                if 'Email:' in el:
                    email = el.split('Email: ')
                    contact.update({'email':email[len(email)-1]})

            # Store contact data
            contacts_data.append(contact)

        return contacts_data


    def convert(self, list):
        """Convert the given dictionary into vCard format
        :param list: list of dictionaries in which each dictionary has one contact data
        :return: vCard data in the proper format vobject
        """
        data_list = []
        # Iterate over contacts data
        for dict in list:
            # Sort the dictionary in the proper way
            if 'number' in dict.keys() and 'email' in dict.keys():
                number = dict.pop('number')
                dict.update({'number':number})
            # Start contact
            data_list.append('BEGIN:VCARD')
            data_list.append('VERSION:3.0')
            for key in dict:
                # Check the kind of data and add it to the list
                if key == 'name': data_list.append('FN:' + dict[key])
                if key == 'email': data_list.append('EMAIL;TYPE=INTERNET:' + dict[key])
                if key == 'number': data_list.append('TEL:' + dict[key])
            # Close contact
            data_list.append('END:VCARD')
        # Generate string from list
        data_str = '\n'.join(data_list)
        print('Data in string format:\n', data_str, '\n')
        # Convert to vobject
        vcard = vobject.readComponents(data_str)

        return vcard



if __name__ == '__main__':

    # Do the login
    obj = Login()
    # Parse html data to obtain contacts info
    parser = ParseHTML(obj.login_agenda())
    contacts = parser.get_contacts()
    if contacts:
        # Generate vcard
        vcard = parser.convert(contacts)
        # Check result
        print('Data in vobject format: \n')
        for cont in vcard: cont.prettyPrint()


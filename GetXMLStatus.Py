#Obtains Tableau Server Status XML and saves to the running Dirctory

import requests
import tableauserverclient as TSC
from tableauserverclient import TableauAuth

#Parameters for Geting Status xml. Admin account is needed.
BaseURL='https://tableau.example.com'
USERNAME = ""
PASSWORD = ""
File = 'systeminfo.xml'

#Create Tableau Server Auth Session
def create_tableau_connection(username, password):
    tableau_auth = TableauAuth(username, password)
    server = TSC.Server(BaseURL)
    server.add_http_options(options_dict={'verify': False})
    server.version = '3.11'
    return server, tableau_auth

def getxml(BaseURL, USERNAME, PASSWORD, File):
    server, tableau_auth = create_tableau_connection(USERNAME, PASSWORD)
    with server.auth.sign_in(tableau_auth):
        URL = BaseURL+"/admin/systeminfo.xml"
        response = requests.get(URL, verify=False)
        with open(File, 'wb') as file:
            file.write(response.content)

import json
import os
import argparse

from shareplum.site import Site
from shareplum.site import Version
from shareplum.office365 import Office365

# Creating parameter parser
parser = argparse.ArgumentParser()

# Creating argument PARAM_FILE (Contains access credentials)
parser.add_argument(
    '--param_file', '-pf',
    help='Enter Sharepoint parameters JSON file name. It defaults to a local file titled shpt_param.json',
    default='./shpt_param.json'
)

# Creating argument FILE (To be downloaded)
parser.add_argument(
    '--file', '-f',
    help='Enter the file name to download. It defaults to config.ini.',
    default='config.ini'
)
# Parsing all added parameters
args = parser.parse_args()

# Reading parameters into variables
param_file = args.param_file
file_name = args.file

# Setting the root folder path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Read the shpt_param.json file
with open(param_file) as config_file:
    config = json.load(config_file)
    config = config['sharepoint']

USERNAME = config['user']
PASSWORD = config['password']
SHAREPOINT_URL = config['url']
SHAREPOINT_SITE = config['site']
SHAREPOINT_DOC = config['doc_library']


def authenticate_with_sharepoint(my_username: str, my_password: str) -> Site:
    """
    Authenticates with Sharepoint System using User's credentials
    :param my_username: The username for Sharepoint
    :type my_username: str
    :param my_password: The user's password for Sharepoint
    :type my_password: str
    :returns: An authenticated Site object type shareplum.Site
    :rtype: shareplum.Site
    """
    print('')
    print('------------------------------------------------------------------------')
    print('########################################################################')
    print('################# - AUTHENTICATING WITH SHAREPOINT - ###################')
    print('########################################################################')
    print('------------------------------------------------------------------------')
    print('')
    try:
        authcookie = Office365(SHAREPOINT_URL, username=my_username, password=my_password).GetCookies()
        auth_site = Site(SHAREPOINT_SITE, version=Version.v365, authcookie=authcookie)
        if auth_site:
            print('-------------------------- AUTHENTICATION OK! --------------------------')
            return auth_site
    except Exception as e:
        print('Ops, something went wrong!')
        print(e)


def connect_folder(auth_site):
    """
    Connects to a Sharepoint folder
    :param auth_site: Connected and authenticated site from Sharepoint
    :type auth_site: Object type shareplum.Site
    :returns: Returns a folder object from the connected Site object
    :rtype: shareplum.folder._Folder
    """
    print('')
    print('--------------------------------------------------------------')
    print('##############################################################')
    print('################# - LOCATING YOUR FOLDER - ###################')
    print('##############################################################')
    print('--------------------------------------------------------------')
    print('')
    try:
        sharepoint_dir = SHAREPOINT_DOC
        folder = auth_site.Folder(sharepoint_dir)
        if sharepoint_dir:
            print('------------------------ FOLDER - OK! ------------------------')
            print(type(folder))
            return folder
    except Exception as e:
        print('Ops, something went wrong!')
        print(e)


def download_file(my_file: str, folder) -> None:
    """
    Locates a file inside a Sharepoint Site folder and Downloads it locally
    :param my_file: The name of the file to be downloaded
    :type my_file: str
    :param folder: The folder object from the connection to Sharepoint
    :type folder: shareplum.folder._Folder
    :returns: None
    """

    print('')
    print('--------------------------------------------------------------')
    print('##############################################################')
    print('################## - GETTING YOUR FILE - #####################')
    print('##############################################################')
    print('--------------------------------------------------------------')
    print('')
    try:
        sharepoint_file = folder.get_file(my_file)
        if sharepoint_file:
            print('-------------------- FILE - OK! ------------------------------')
            print('')
            print('-------------------- SAVING YOUR FILE... ---------------------')
            with open(file_name, 'wb') as f:
                f.write(sharepoint_file)
            print('')
            print('-------------------- DONE! -----------------------------------')
            print('')
    except Exception as e:
        print('Ops, something went wrong!')
        print(e)


if __name__ == '__main__':
    print("PLEASE SELECT THE LOCATION OF YOUR USER CREDENTIALS", end='\n')
    print("1 - Parameters file;", end='\n')
    print("2 - Environment variable;", end='\n')
    credential_location = input()
    if credential_location == '2':
        username = input("INSERT THE NAME OF VARIABLE FOR THE USER: ")
        password = input("INSERT THE NAME OF VARIABLE FOR THE PASSWORD: ")
        USERNAME = os.environ.get(username.upper())
        PASSWORD = os.environ.get(password.upper())

    sharepoint_authentication = authenticate_with_sharepoint(USERNAME, PASSWORD)
    if sharepoint_authentication:
        folder_connection = connect_folder(sharepoint_authentication)
        download_file(file_name, folder_connection)

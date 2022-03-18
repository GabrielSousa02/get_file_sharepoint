# A Simple Example of [Shareplum](https://github.com/jasonrollins/shareplum) usage in a Python Script

This python script reads credentials from a local parameter file in JSON format, and connects to MS365 - Sharepoint
using the given credentials (JSON file) to download a config.ini file.

This script came from a specific need during the development of a Python project, and it can be used to distribute
config files or other files that are stored within your company's Sharepoint Site, which cannot be added to your code
repo.

## Installation:

### This script only needs python libraries, listed inside *requirements.txt*
### Required libraries:
All required libraries can be installed using pip, through the following command:

    pip install -r requirements.txt

***It's highly recommended to use Python Virtual Environments.***

---
## Example Setup file:
```json
{
    "sharepoint":
        {
            "user": "{USERNAME}",
            "password": "{PASSWORD}",
            "url": "https://{YOUR_DOMAIN}.sharepoint.com",
            "site": "https://{YOUR_DOMAIN}.sharepoint.com/sites/{YOUR_SITE}/",
            "doc_library": "Shared Documents/path/to/your/file.ext"
        }
}
```

---
## Usage:
### This script takes up to two arguments:
1. `--param_file` or `-pf`<br>
Enter Sharepoint parameters JSON file name. It defaults to **'shpt_param.json'**
   
2. `--file` or `-f`<br>
Enter the file name to download. It defaults to **'config.ini'**


    python get_from_sharepoint.py

or you can set your own parameters file and file to download:

    python get_from_sharepoint.py -pf my_parameters.json -f my_config.ini

**NOTE: If no argument is given, the script will fall back to default file names under the working dir.**

The script then will prompt you and ask were are your credentials located, if you're using environment variables or if
it's all inside the parameters file.
```
PLEASE SELECT THE LOCATION OF YOUR USER CREDENTIALS
1 - Parameters file;
2 - Environment variable;
```
If you select option number one, it will scan the JSON file for the "user", and "password" keys and start the normal
download process.

If you select option number two, it will ask you for the names of the local variables.
```
PLEASE SELECT THE LOCATION OF YOUR USER CREDENTIALS
1 - Parameters file;
2 - Environment variable;
> 2
INSERT THE NAME OF VARIABLE FOR THE USER: sharepoint_user
INSERT THE NAME OF VARIABLE FOR THE PASSWORD: sharepoint_password
```

**NOTE: The script will format the variables to uppercase automatically.**

---

# tootdel
## Toot deleter for Mastodon

---

This is a simple Python script that deletes toots from a Mastodon server. 
This was written for deleting toots from counter.social but should work 
for any Mastodon server version 2.8 or greater. This script is not elegant 
Python. __Use at your own risk.__

## Requirements

- Python version 3.7 or greater. It probably works with earlier versions of 
  Python 3 but I have only tested with 3.7 and 3.9.
- Mastodon.py package installed via pip.

## Installation
I highly recommend not messing with whatever default python install you 
might have and instead run this via [pipenv](https://pypi.org/project/pipenv/).

1. Open a command prompt and type `pipenv`. If something comes back you 
   should be good to go. Otherwise install pipenv.
    1. At the same command prompt type `pip3 install pipenv`.
    2. If for some reason that doesn't work use `python3 -m pip install pipenv`
2. Once pipenv is installed just type `pipenv` again to make sure it runs.
3. Either clone this repository to a folder or download `tootdel.py`, `Pipfile`, 
   and `tootdel.cfg`
4. From the directory in step 3 simply run `pipenv install`. This will create a 
   new virtual environment to run the script and automatically install the 
   Mastodon.py dependency.
5. Configure the script as per the section below.

## Configuration
The script comes with a config file pre-populated with the proper keys but 
no values for the secret keys or base url of the server. The items are simply
key=value. Do not include quotes, etc.

You need to configure the following items:

- base_url
    - for example `base_url=https://mastodon.social`
- client_key, client_secret, access_token
    - these all come from your particular profile on your Mastodon server

The following are optional:
- days_to_keep
    - delete anything older than this number
    - defaults to 7 in the script
- sleep_time
    - number of seconds to sleep between toot deletes and between grabbing 
      pages of toots while processing
    - defaults to 5 seconds in the script
    
If you don't include the optional values in `tootdel.cfg` then remove them.

__Note__: tootdel.cfg can either live in the same location as the script 
file itself or inside the `.tootdel` directory that gets created in your 
home directory.


## Running the script
If you used the installation instructions above then from the directory that 
contains the script and pipfile run the command `pipenv shell`. Then run 
`python3 tootdel.py`. 

## Logging
This script creates a directory called `.tootdel` in your home directory and 
writes to a log file there when it runs.
    


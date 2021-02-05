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

## Configuration
You need to configure the following items:

- base_url
    - for example https://mastodon.social
- days_to_keep
    - delete anything older than this number
- client_key, client_secret, access_token
    - these all come from your particular profile on your Mastodon server
    
## Logging
This script creates a directory called `.tootdel` in your home directory and 
writes to a log file there when it runs.
    


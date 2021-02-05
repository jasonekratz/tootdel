from mastodon import Mastodon
from datetime import timedelta, datetime, timezone
from pathlib import Path
import os
import time
import logging

def deletetoot(last_toot_id):
    logging.debug('deleting toot: ' + str(last_toot_id))
    m.status_delete(str(last_toot_id))
    logging.debug('deleted toot: ' + str(last_toot_id))
    logging.debug('sleeping for 5 seconds...')
    time.sleep(5)

def save_last_position(path, last_toot_id):
    logging.debug('saving last position')
    last_toot = Path(path,'last_toot.txt')
    if last_toot.exists():
        os.remove(last_toot)
    last_toot.open(mode='w')
    last_toot.write_text(str(last_toot_id))

def load_last_position(path):
    logging.debug('loading last toot id')
    last_toot = Path(Path.home(), Path('.tootdel'),'last_toot.txt')
    if not last_toot.exists():
        return str(0)
    else:
        last_toot.open(mode='r')
        return last_toot.read_text()

if __name__ == '__main__':

    client_key = ''
    client_secret = ''
    access_token = ''
    base_url = ''
    days_to_keep = 7
    today = datetime.now(tz=timezone.utc)
    delete_prior_to = today - timedelta(days=days_to_keep)
    keep_looping = True
    last_toot_id = ''
    number_toots_deleted = 0

    p = Path(Path.home(), Path('.tootdel'))
    p.mkdir(exist_ok=True)

    logging.basicConfig(filename=Path(p, Path('tootdel.log')), level=logging.DEBUG, format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    m = Mastodon(client_secret=client_secret,access_token=access_token,api_base_url=base_url)
    account = m.account_verify_credentials()

    account_id = account["id"]

    logging.debug('deleting toots prior to: ' + str(delete_prior_to))

    last_toot_id = load_last_position(p)
    logging.debug('loaded last toot id: ' + last_toot_id)

    logging.debug('retrieving toots...')
    if last_toot_id == '0':
        results = m.account_statuses(account_id)
    else:
        results = m.account_statuses(account_id, min_id=last_toot_id)

    logging.debug('deleting toots older than ' + str(days_to_keep) + ' days')
    while keep_looping:
        if len(results) > 0:
            for item in results:
                toot_date = item["created_at"]
                last_toot_id = item["id"]
                if toot_date < delete_prior_to:
                    deletetoot(last_toot_id)
                    number_toots_deleted += 1
            logging.debug('Sleeping for 5 seconds before retrieving more toots...')
            time.sleep(5)
            if number_toots_deleted == 0:
                logging.debug('No toots deleted in current batch')
            logging.debug('Retrieving more toots')
            results = m.account_statuses(account_id, max_id=last_toot_id)
            logging.debug('loaded ' + str(len(results)) + ' toots')
        else:
            keep_looping = False

    logging.debug('deleted ' + str(number_toots_deleted) + ' toots')
    save_last_position(p,last_toot_id)

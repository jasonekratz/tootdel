from mastodon import Mastodon
from datetime import timedelta, datetime, timezone
from pathlib import Path
import time
import logging
import configparser
import sys

def deletetoot(last_toot_id):
    logging.debug('deleting toot: ' + str(last_toot_id))
    m.status_delete(str(last_toot_id))
    logging.debug('deleted toot: ' + str(last_toot_id))
    logging.debug('sleeping...')
    time.sleep(sleep_time)

if __name__ == '__main__':

    p = Path(Path.home(), Path('.tootdel'))
    p.mkdir(exist_ok=True)

    config = configparser.ConfigParser({'days_to_keep': '7', 'sleep_time': '60'})
    config_files = config.read([Path(p, Path('tootdel.cfg')),'tootdel.cfg',])

    if len(config_files) == 0:
        sys.exit("tootdel.cfg not found")

    client_key = config.get('tootdel','client_key')
    client_secret = config.get('tootdel','client_secret')
    access_token = config.get('tootdel','access_token')
    base_url = config.get('tootdel','base_url')
    days_to_keep = config.getint('tootdel','days_to_keep')
    sleep_time = config.getint('tootdel','sleep_time')

    today = datetime.now(tz=timezone.utc)
    delete_prior_to = today - timedelta(days=days_to_keep)
    keep_looping = True
    number_toots_deleted = 0

    logging.basicConfig(filename=Path(p, Path('tootdel.log')), level=logging.DEBUG, format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    m = Mastodon(client_secret=client_secret,access_token=access_token,api_base_url=base_url)
    account = m.account_verify_credentials()

    account_id = account["id"]

    logging.debug('deleting toots prior to: ' + str(delete_prior_to))

    logging.debug('retrieving toots...')
    results = m.account_statuses(account_id)

    logging.debug('deleting toots older than ' + str(days_to_keep) + ' days')
    while keep_looping:
        if len(results) > 0:
            for item in results:
                toot_date = item["created_at"]
                toot_id = item["id"]
                if toot_date < delete_prior_to:
                    deletetoot(toot_id)
                    number_toots_deleted += 1
            logging.debug('Sleeping before retrieving more toots...')
            time.sleep(sleep_time)
            if number_toots_deleted == 0:
                logging.debug('No toots deleted in current batch')
            logging.debug('Retrieving more toots')
            results = m.account_statuses(account_id, max_id=toot_id)
            logging.debug('loaded ' + str(len(results)) + ' toots')
        else:
            keep_looping = False

    logging.debug('deleted ' + str(number_toots_deleted) + ' toots')

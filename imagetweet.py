# -*- coding: utf-8 -*-
from collections import OrderedDict
from utils import printf as print
from configobj import ConfigObj
from threading import Thread
import pathlib
import tweepy
import time
import sys
import os
sys.path.append('plugins/')

account_list = OrderedDict()
api_objects = OrderedDict()
__version__ = '0.1.0'
CHECK_UPDATE = True
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
if os.environ.get('DEBUG') == "travis":
    DEBUG = "travis"
    DEBUG_ACCS = os.environ.get('ACCOUNTS', '').split("||")
    # Download test image for folder testing
    from utils import download_image
    url = "https://www.google.co.uk/images/nav_logo231_hr.png"
    download_image(url)
else:
    # Local testing. Edit this for your own testing.
    DEBUG = False
    DEBUG_ACCS = ["test"]


def latest_ver():
    import urllib.request
    url = "http://ace3df.github.io/AcePictureBot/it_ver.txt"
    try:
        site_ver = urllib.request.urlopen(url).read().strip().decode("utf-8")
        if site_ver != __version__:
            print("!WARNING! A new version is out ({0})!".format(site_ver))
            print("Download it here: http://bombch.us/BWVH")
            print("----------------------------------------\n")
    except:
        # Just in case
        pass


def login(bot):
    creds = OrderedDict((
                k.lower(), v) for k, v in bot[1].items())
    consumer_token = creds['credentials']['consumer key']
    consumer_secret = creds['credentials']['consumer secret']
    access_token = creds['credentials']['access token']
    access_token_secret = creds['credentials']['access token secret']

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def load_accounts():
    accounts = sorted(
        [p for p in pathlib.Path(
            os.path.join(BASE_DIR, 'accounts')).iterdir() if p.is_file()])
    account_count = 0
    print(os.path.join(BASE_DIR, 'accounts'))
    print(accounts)
    for acc in accounts:
        bot_name = os.path.basename(str(acc)).split(".")[0]
        if DEBUG:
            if bot_name not in DEBUG_ACCS:
                continue
        elif not DEBUG:
            if "example" in bot_name.lower():
                continue
        account_count += 1
        account_list[bot_name] = OrderedDict()
        Config = ConfigObj(str(acc))
        has_cred = False
        has_sett = False
        for sec in (Config.iteritems()):
            sec = tuple(sec)
            if sec[0] == "credentials":
                has_cred = True
            elif sec[0] == "settings":
                has_sett = True
            if "-thread" in sec[0]:
                # Start thread import setttings and creds
                pass
            account_list[bot_name][sec[0].lower()] = (sec[1].copy())
        if not has_cred:
            print("Credentials not found for bot: {}".format(bot_name))
            input("Press ENTER to close.")
            sys.exit(0)
        elif not has_sett:
            print("No settings are set for bot: {}".format(bot_name))
            input("Press ENTER to close.")
            sys.exit(0)
        temp = OrderedDict()
        for k, v in account_list[bot_name].items():
            for a, b in v.items():
                a = a.lower()
                try:
                    temp[k][a] = b
                except:
                    temp[k] = {a: b}
        account_list[bot_name] = temp.copy()
        del temp
    print("Running {0} Accounts!\n".format(account_count))
    return(account_list)


def load_plugin(name):
    mod = __import__("%s" % name)
    return mod


def call_plugin(name, *args, **kwargs):
    plugin = load_plugin(name)
    return plugin.main(*args, **kwargs)


def post_tweet(api, msg, image):
    if image:
        image = image.replace("\\", "\\\\")

    if image:
        api.update_with_media(image, status=msg)
    else:
        # Leave this here if someone wants to
        # call it in their plugin or something
        api.update_status(status=msg)


def main_bot(bot):
    bot_name = bot[0]
    bot = OrderedDict(bot[1].items())
    api = bot.get('api')
    try:
        start_delay = int(bot.get('settings').get('start delay'))
    except:
        start_delay = 0
    try:
        time_delay = int(bot.get('settings').get('time delay'))
    except:
        time_delay = 15
    if not DEBUG:
        time.sleep(start_delay * 60)
    while True:
        for plugin in bot.items():
            if "-thread" in plugin[0]:
                continue
            if plugin[0] == "settings":
                continue
            elif plugin[0] == "credentials":
                continue
            elif plugin[0] == "api":
                continue
            plugin_kwgs = OrderedDict((
                k.lower(), v) for k, v in plugin[1].items())
            plugin_kwgs['bot name'] = bot_name
            plugin_kwgs['DEBUG'] = DEBUG
            plugin_kwgs['support webm'] = bot.get(
                'settings').get('support webm')
            plugin_kwgs['webm script'] = bot.get(
                'settings').get('webm script')
            plugin_kwgs['saucenao api'] = bot.get(
                'settings').get('saucenao api')
            p_repeat = bot.get(plugin[0]).get('p_repeat')
            if not p_repeat:
                p_repeat = 1

            for x in range(0, int(p_repeat)):
                try:
                    print("{0}:".format(bot_name))
                    print(time.strftime('%I:%M%p %Z on %b %d, %Y'))
                    if DEBUG:
                        print("\n" + str(plugin_kwgs) + "\n")
                    m, i = (call_plugin(plugin[0], **OrderedDict(plugin_kwgs)))
                    if i == "SKIP":
                        # No need to print that it's skipping as this
                        # should only happen when the user knows it will happen
                        continue
                    elif i:
                        print("Message: {0}\nImage: {1}\n".format(
                            m, i))
                        if not DEBUG:
                            post_tweet(api, m, i)
                        elif DEBUG == "travis":
                            try:
                                if not i:
                                    raise ValueError('empty image')
                            except ValueError as e:
                                print("Failed to get image for: {0}".format(
                                    bot_name))
                        else:
                            sys.exit(0)
                        time.sleep(time_delay * 60)
                    else:
                        # Push to Exeption
                        raise Exception()
                except Exception as e:
                    print("!FAILED POSTING!")
                    print("{0}:".format(bot_name))
                    print(time.strftime('%I:%M%p %Z on %b %d, %Y'))
                    if e == "" or e is None:
                        # Custom message
                        e = "^ Described Above! ^"
                    print("Problem: {0}\n".format(e))
                    if DEBUG:
                        raise Exception()
                    # Make this 30 seconds to give time to read
                    # and maybe make the owner know that something is up
                    # for it being so late. i.e. a PM system/push note
                    time.sleep(30)

if __name__ == '__main__':
    if CHECK_UPDATE:
        latest_ver()
    account_list = load_accounts()
    for bot in account_list.items():
        if not DEBUG:
            bot[1]['api'] = login(bot)
        Thread(name=bot[0], target=main_bot, args=(bot, )).start()
        time.sleep(3)

# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sys
import os
import re
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils import printf as print
import utils


def get_reddit(**kwargs):
    if kwargs.get('used images'):
        txt_name = kwargs.get('used images')
        used_links = open(txt_name, 'r').read().splitlines()
    else:
        txt_name = os.path.join(os.getcwd(), "Used reddit {0}.txt".format(
                                             kwargs['bot name']))
        try:
            used_links = open(txt_name, 'r').read().splitlines()
        except:
            if not os.path.exists(txt_name):
                print("Didn't find any used links! Creating a TXT!")
                print("Set it to:\n{0}".format(txt_name))
                used_links = []
            else:
                used_links = open(txt_name, 'r').read().splitlines()
    try:
        sub = used_links[0]
        used_links = used_links[1:]
    except:
        # Probably doesn't exist (i hope only that)
        pass
    if kwargs.get('save images'):
        if kwargs.get('path'):
            path = kwargs.get('path')
        else:
            path = os.path.abspath(os.path.join(os.getcwd(),
                                                "images"))
            if not os.path.exists(path):
                os.makedirs(path)
    else:
        path = os.path.abspath(os.path.join(os.getcwd()))

    start_url = "https://www.reddit.com/r/"
    subreddits = kwargs.get('subreddits')
    is_random = kwargs.get('random subreddit')
    is_random_link = kwargs.get('random link')
    if subreddits is None:
        return False, False
    if isinstance(subreddits, str):
        subreddits = subreddits.split(", ")
    if utils.is_bool(is_random):
        import random
        sub = random.choice(subreddits)
    else:
        # Get last used sub and + 1
        try:
            sub = open(os.path.join(os.getcwd(), "Used reddit {0}.txt".format(
                                                         kwargs['bot name'])),
                       'r').read().splitlines
            sub = subreddits[(subreddits.index(sub) + 1)]
        except:
            # Doesn't exsist / end of list
            sub = subreddits[0]
    url = start_url + sub + "/.rss"
    soup = utils.scrape_site(url, is_rss=True)
    pic_imgs = []
    for a in soup.find_all('item'):
        img_string = a.find('description').string
        img_title = a.find('title').string
        img_link = a.find('link').string
        img_string = img_string[:img_string.index("[link]")]
        img_string = BeautifulSoup(img_string, 'html5lib').find_all('a')
        for item in img_string:
            if "reddit.com" not in item['href'] and "http" in item['href']:
                pic_imgs.append([item['href'], img_title, img_link])

    if utils.is_bool(is_random_link):
        import random
        image = random.choice(pic_imgs)
    else:
        image = pic_imgs[0]
    safe_break = 0
    count = 0
    while image[0] in used_links:
        if utils.is_bool(is_random_link):
            image = random.choice(pic_imgs)
        else:
            image = pic_imgs[count]
            if image[0] in used_links:
                count += 1
                continue
            break
        safe_break += 1
        if safe_break == 50:
            break
    used_links.append(image[0])
    imgTypes = {"jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "png": "image/png",
                "gif": "image/gif",
                "webm": "video/webm"}
    filepath = urlparse(image[0]).path
    ext = os.path.splitext(filepath)[1].lower()
    if not ext[ext.rfind(".") + 1:] in imgTypes:
        if "imgur" in image[0]:
            # Just make it .png it still returns correct image
            image[0] = "http://i.imgur.com/" + image[0].rsplit(
                       '/', 1)[1] + ".png"
            ext = ".png"

    sn_kwgs = {}
    if "(x-post" in image[1].lower() or "(via" in image[1].lower():
        image[1] = re.sub(r'\([^)]*\)', '', image[1])
    if "sn" in kwargs.get('message'):
        sn_url, sn_kwgs = utils.saucenao(fname=image[0],
                                         api_key=kwargs.get('saucenao api'),
                                         metainfo=True)
    re_dict = {'{url}': image[2],
               '{title}': image[1],
               '{sn title}': sn_kwgs.get('title'),
               '{sn illust id}': sn_kwgs.get('illust id'),
               '{sn illust url}': sn_url,
               '{sn artist}': sn_kwgs.get('artist'),
               '{sn artist id}': sn_kwgs.get('artist id'),
               '{sn artist url}': sn_kwgs.get('artist url')}

    if kwargs.get('filename'):
        filename = utils.replace_all(kwargs.get('filename'), re_dict)
        filename = utils.safe_msg(filename)
    else:
        filename = ""
    if kwargs.get('message'):
        message = utils.replace_all(kwargs.get('message'), re_dict)
        message = utils.safe_msg(message)
    else:
        message = ""
    image = utils.download_image(image[0], path, filename, **kwargs)
    used_links = [sub] + used_links
    with open(txt_name, 'w') as f:
        f.write("\n".join(used_links))
    return message, image


def main(**kwargs):
    message, image = get_reddit(**kwargs)
    return(message, image)

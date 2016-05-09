# -*- coding: utf-8 -*-
import random
import time
import sys
import os
import re
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import utils


def delete_image(image):
    import time
    time.sleep(10)
    os.remove(image)


def tag_clean(tag_html):
    text = tag_html.text
    text = text.rstrip('1234567890.')
    text = text.replace("&#39;", "\'").strip()
    return text


def get_image_online(**kwargs):
    if kwargs.get('used images'):
        txt_name = kwargs.get('used images')
        used_links = open(txt_name, 'r').read().splitlines()
    else:
        txt_name = os.path.join(os.getcwd(), "Used safebooru {0}.txt".format(
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

    if kwargs.get('highest page'):
        high_page = int(kwargs.get('highest page'))
    else:
        high_page = 50

    tried_pages = [high_page]
    cookie_file = None
    try_count = 0
    low_page = 0
    page = 0
    x = None
    no_images = False
    url_start = "http://safebooru.org"
    url_search = "http://safebooru.org/index.php?page=post&s=list&tags="
    if utils.is_bool(kwargs.get('login')):
        cookie_file = "../safebooru.txt"
        url_login = url_start + "/index.php?page=account&s=login&code=00"
        form_num = 0
        form_user = "user"
        form_password = "pass"
        username = kwargs.get('username')
        password = kwargs.get('password')
        if not os.path.exists(cookie_file):
            browser, s = utils.scrape_site(url_login, cookie_file, True)
            form = browser.get_form(form_num)
            form[form_user].value = username
            form[form_password].value = password
            browser.submit_form(form)
            s.cookies.save()

    if utils.is_bool(kwargs.get('save images')):
        if kwargs.get('path'):
            path = kwargs.get('path')
        else:
            path = os.path.abspath(os.path.join(os.getcwd(),
                                                "images"))
            if not os.path.exists(path):
                os.makedirs(path)
    else:
        path = os.path.abspath(os.path.join(os.getcwd()))

    if kwargs.get('tags'):
        if isinstance(kwargs.get('tags'), list):
            tags = '+'.join(kwargs.get('tags'))
        else:
            tags = '+'.join(kwargs.get('tags').split(', '))
    else:
        tags = ""
    if kwargs.get('ignore tags'):
        if isinstance(kwargs.get('ignore tags'), list):
            ignore_tags = kwargs.get('ignore tags')
        else:
            ignore_tags = kwargs.get('ignore tags').split(', ')
    else:
        ignore_tags = []
    if utils.is_bool(kwargs.get('ignore cosplay')):
        ignore_cosplay = utils.is_bool(kwargs.get('ignore cosplay'))
    else:
        ignore_cosplay = False
    if utils.is_bool(kwargs.get('accept webm')):
        accept_webm = utils.is_bool(kwargs.get('accept webm'))
    else:
        accept_webm = False

    tried_pages = [high_page + 41]
    while True:
        while True:
            while True:
                while True:
                    no_images = False
                    try_count += 1
                    if try_count == 15:
                        return False, False
                    page = str(int(random.randint(low_page, high_page) * 40))
                    while int(page) in tried_pages:
                        if int(page) == 0:
                            break
                        if not x:
                            x = high_page
                        page = str(int(
                            random.randint(low_page, high_page) * 1))
                        if int(page) > int(x):
                            continue
                    tried_pages.append(int(page))
                    x = min(tried_pages)
                    page_url = "&pid=" + str(page)
                    url = "%s%s%s" % (url_search, tags, page_url)
                    browser = utils.scrape_site(url, cookie_file)
                    if browser.find('h1', text="Nothing found, try google? "):
                        no_images = True
                    elif len(browser.find_all('img')) < 3:
                        no_images = True
                    time.sleep(1)
                    if not no_images:
                        break
                    elif no_images and int(page) == 0:
                        return False, False
                good_image_links = []
                image_links = browser.find_all('span', class_="thumb")
                for link in image_links:
                    try:
                        link['id']
                    except:
                        continue
                    link = str(link['id'])[1:]
                    good_image_links.append(link)
                if good_image_links == []:
                    return False, False
                random.shuffle(good_image_links)
                url = "%s/index.php?page=post&s=view&id=%s" % (
                    url_start, random.choice(good_image_links))
                try_count = 0
                while url in used_links:
                    url = "%s/index.php?page=post&s=view&id=%s" % (
                        url_start, random.choice(good_image_links))
                    try_count = try_count + 1
                    if try_count == 20:
                        break
                used_links.append(url)
                post_url = url
                browser.open(url)
                image_tags = []
                char_tags = []
                art_tags = []
                sers_tags = []
                tags_tags = []
                site_tag = browser.find('ul', id="tag-sidebar")
                site_tag = site_tag.find_all('li')
                for taga in site_tag:
                    tag = tag_clean(taga)
                    if taga['class'][0] == "tag-type-artist":
                        art_tags.append(tag.title())
                    elif taga['class'][0] == "tag-type-copyright":
                        sers_tags.append(tag.title())
                    elif taga['class'][0] == "tag-type-character":
                        char_tags.append(tag.title())
                    else:
                        tags_tags.append(tag.title())
                    image_tags.append(tag.lower())
                if any([item in [x.lower() for x in ignore_tags]
                        for item in [x.lower() for x in image_tags]]):
                    continue
                if ignore_cosplay:
                    if any(" (cosplay)" in s for s in image_tags):
                        continue
                break
            filename = ""
            if not utils.is_bool(kwargs.get('message')):
                message = ""
            try:
                url = browser.find(
                    'img', attrs={'id': 'image'})['src'].replace("\\\\", "\\")
            except:
                # Flash file
                continue
            sn_kwgs = {}
            sn_url, sn_kwgs = utils.saucenao(url, kwargs['saucenao api'], True)
            re_dict = {'{#artist}': (
                '#' if art_tags else '') + ' #'.join(
                [x.replace(" ", "_") for x in art_tags]),
                       '{#character}': (
                '#' if char_tags else '') + ' #'.join(
                [x.replace(" ", "_") for x in char_tags]),
                       '{#series}': (
                '#' if sers_tags else '') + ' #'.join(
                [x.replace(" ", "_") for x in sers_tags]),
                       '{#tags}': (
                '#' if tags_tags else '') + ' #'.join(
                [x.replace(" ", "_") for x in tags_tags]),
                       '{artist}': ', '.join(art_tags),
                       '{character}': ', '.join(char_tags),
                       '{series}': ', '.join(sers_tags),
                       '{tags}': ', '.join(tags_tags),
                       '{url}': post_url,
                       '{sn title}': sn_kwgs.get('title'),
                       '{sn illust id}': sn_kwgs.get('illust id'),
                       '{sn illust url}': sn_url,
                       '{sn artist}': sn_kwgs.get('artist'),
                       '{sn artist id}': sn_kwgs.get('artist id'),
                       '{sn artist url}': sn_kwgs.get('artist url')}

            if kwargs.get('filename'):
                filename = utils.replace_all(kwargs.get('filename'), re_dict)
                filename = utils.safe_msg(filename)

            if kwargs.get('message'):
                message = utils.replace_all(kwargs.get('message'), re_dict)
                message = utils.safe_msg(message)

            with open(txt_name, 'w') as f:
                f.write("\n".join(used_links))

            tweet_image = utils.download_image(url, path, filename, **kwargs)
            if tweet_image:
                break
        if not utils.is_bool(kwargs.get('save images')):
            from threading import Thread
            Thread(name="Delete Image", target=delete_image, args=(
                tweet_image, )).start()
        return message, tweet_image


def main(**kwargs):
    message, image = get_image_online(**kwargs)
    return(message, image)

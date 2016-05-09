# -*- coding: utf-8 -*-
import sys


def printf(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def replace_all(string, dic):
    if not string:
        return ""
    for i, j in sorted(dic.items()):
        i = str(i)
        j = str(j)
        string = string.replace(i, j)
    return string


def safe_msg(string, trun="..", long=120):
    string = "".join([s for s in string.strip().splitlines(True) if s.strip()])
    return (string[:long] + trun) if len(string) > long else string


def saucenao(fname, api_key, metainfo=False):
    if api_key is None or not api_key:
        if metainfo:
            return "", {}
        else:
            return ""
    from collections import OrderedDict
    from PIL import Image
    import requests
    import json
    import io
    if "http" in fname or ".com" in fname:
        url = "http://saucenao.com/search.php?output_type=2&numres=1" \
              "&minsim=80&dbmask=999&url={0}&api_key={1}".format(
                fname, api_key)
        r = requests.post(url)
    else:
        url = "http://saucenao.com/search.php?output_type=2&numres=1" \
              "&minsim=80&dbmask=999&api_key={0}".format(api_key)
        image = Image.open(fname)
        image.thumbnail((150, 150), Image.ANTIALIAS)
        imageData = io.BytesIO()
        image.save(imageData, format='PNG')
        files = {'file': ("image.png", imageData.getvalue())}
        imageData.close()
        r = requests.post(url, files=files)
    if r.status_code == 403:
        print("!Invalid SauceNao API Key!\n")
        if metainfo:
            return "", {}
        else:
            return ""
    # Don't need to catch any problems as it should only be if saucenao is down
    # or out of searches
    results = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(r.text)
    if not int(results['header']['user_id']) > 0:
        # General issue, api did not respond.
        # Normal site took over for this error state.
        # Issue is unclear, so don't flood requests.
        if metainfo:
            return "", {}
        else:
            return ""
    if int(results['header']['results_returned']) > 0:
        # One or more results were returned
        similarity = float(results['results'][0]['header']['similarity'])
        min_similarity = float(results['header']['minimum_similarity'])
        if similarity > min_similarity:
                illust_id = 0
                index_id = results['results'][0]['header']['index_id']
                if index_id == 5 or index_id == 6:
                    # 5->pixiv 6->pixiv historical
                    illust_id = results['results'][0]['data']['pixiv_id']
                    artist_url = "http://www.pixiv.net/member.php?id=" + \
                                 illust_id
                    a_url = "http://www.pixiv.net/member_illust.php?" \
                            "mode=medium&illust_id={0}".format(illust_id)
                elif index_id == 8:
                    # 8->nico nico seiga
                    illust_id = results['results'][0]['data']['seiga_id']
                    artist_url = ""  # Can't find user page URL??
                    a_url = "http://seiga.nicovideo.jp/seiga/im{0}".format(
                             illust_id)
                elif index_id == 10:
                    # 10->drawr
                    illust_id = results['results'][0]['data']['drawr_id']
                    artist_url = "http://drawr.net/" + \
                                 illust_id
                    a_url = "http://drawr.net/show.php?id={0}".format(
                             illust_id)
                else:
                    # Unknown
                    if metainfo:
                        return "", {}
                    else:
                        return ""
                if metainfo:
                    metainfo = OrderedDict()
                    metainfo['title'] = ""
                    metainfo['illust id'] = ""
                    metainfo['artist'] = ""
                    metainfo['artist id'] = ""
                    metainfo['artist url'] = ""
                    metainfo['title'] = results['results'][0][
                                                'data']['title']
                    metainfo['illust id'] = illust_id
                    metainfo['artist'] = results['results'][0][
                                                 'data']['member_name']
                    metainfo['artist id'] = results['results'][0][
                                                    'data']['member_id']
                    metainfo['artist url'] = artist_url
                    return a_url, metainfo
                else:
                    return a_url
        else:
            # Not similarity enough
            if metainfo:
                return "", {}
            else:
                return ""
    else:
        if metainfo:
            return "", {}
        else:
            return ""


def webm_convert(video, script, save_to):
    import subprocess
    import os
    if "../" in video:
        video = video[3:]
    if ":" not in script:
        script = os.path.dirname(os.path.abspath(__file__)) + "\\" + script
    if save_to == "../":
        save_to = ""
    filename = os.path.join(
        save_to,
        os.path.splitext(os.path.basename(video))[0] + ".gif")
    command = [script,
               video,
               filename]
    DEVNULL = open(os.devnull, 'w')
    pipe = subprocess.Popen(command, stdout=DEVNULL, bufsize=10**8)
    pipe.wait()
    return filename


def is_bool(string):
    if isinstance(string, bool):
        return string
    if isinstance(string, int):
        return string
    try:
        return string.lower() in ['true', '1', 'yes', 'yeah',
                                  'yup', 'certainly', 'uh-huh']
    except:
        # None Type
        return False


def scrape_site(url, cookie_file="", ses=False, is_rss=False):
    from http.cookiejar import LWPCookieJar
    from robobrowser import RoboBrowser
    from requests import Session
    s = Session()
    if cookie_file:
        s.cookies = LWPCookieJar(cookie_file)
        try:
            s.cookies.load(ignore_discard=True)
        except:
            # Cookies don't exsit yet
            pass
    s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; rv:39.0)'
    s.headers['Accept'] = 'text/html'
    s.headers['Connection'] = 'keep-alive'
    if is_rss:
        parser = 'xml'
    else:
        parser = 'html5lib'
    browser = RoboBrowser(session=s,
                          parser=parser)
    browser.open(url)
    if ses:
        return browser, s
    else:
        return browser


def download_image(*args, **kwgs):
    from urllib.parse import urlparse
    from PIL import Image
    import urllib.request
    import hashlib
    import os
    url = args[0]
    try:
        path = args[1]
    except:
        path = os.path.dirname(os.path.realpath(__file__))
    try:
        fname = args[2]
    except:
        fname = ""
    imgTypes = {"jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "png": "image/png",
                "gif": "image/gif",
                "webm": "video/webm"}
    filepath = urlparse(url).path
    ext = os.path.splitext(filepath)[1].lower()
    if not ext[ext.rfind(".")+1:] in imgTypes:
        return False

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
           'Connection': 'keep-alive'}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    data = response.read()

    if not os.path.exists(path):
        os.makedirs(path)

    if fname == "":
        hash = hashlib.md5(data).hexdigest()
        filename = "%s%s" % (hash, ext)
    else:
        filename = fname + ext

    if not os.path.isfile(os.path.join(path, filename)):
        tweet_image = os.path.join(path, filename)
        with open(tweet_image, "wb") as code:
            code.write(data)
    else:
        tweet_image = os.path.join(path, str(filename))

    if "webm" in ext[ext.rfind(".")+1:]:
        webm_old = tweet_image
        tweet_image = webm_convert(tweet_image,
                                   kwgs.get('webm script'), path)
        if not tweet_image:
            os.remove(webm_old)
            return False
        else:
            os.remove(webm_old)

    if ((os.stat(tweet_image).st_size / 1000000) > 2.8):
        # Filesize too big, return False if normal image
        # Try to compress if a gif
        if "gif" in ext[ext.rfind(".")+1:]:
            tweet_image = webm_convert(tweet_image,
                                       kwgs.get('webm script'), path)
            # Still too large
            if ((os.stat(tweet_image).st_size / 1000000) > 2.8):
                os.remove(tweet_image)
                return False
        else:
            os.remove(tweet_image)
            return False

    pil_image = Image.open(tweet_image)
    pil_image.load()
    width, height = pil_image.size
    del pil_image
    if ext == ".gif":
        max_size = -160
        min_size = 610
    else:
        max_size = -610
        min_size = 610
    if (width - height) <= max_size:
        os.remove(tweet_image)
        return False
    elif (width - height) >= min_size:
        os.remove(tweet_image)
        return False

    return tweet_image

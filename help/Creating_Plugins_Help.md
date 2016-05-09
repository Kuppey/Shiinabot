Creating Plugins
======
to lazy to write all this
it's p.simple tho

ALWAYS USE:
```
def main(**kwgs):
    message = ""
    image = ""
    return message, image
```

You can use what is in utils.py and it fully suports signing into a website (look at sankaku.py for logging in example) 

For testing it's best to use the DEBUG option at the top of imagetweet.py

### Things to always do
* Always have a main() function that takes a kwargs
* Always return message first then image (return message, image)
* If you're using the users settings (webm, saucenao api, etc.) take into account that those settings might just be None (i.e. empty)
* Always include a safty check with messages to make sure they don't go over the 140 (120 if with a image) char limit. You can use utils.safe_msg(string) or just manually do ```(string[:long] + '..') if len(string) > long else string```

### Adding basic message replacements
If you want to allow users to do things such as {artist} / {#artist}, etc.

Here is a simple template for you to use. Make sure that you have these variables declared in some way or another.
```
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
```

### Using SauceNAO
If metainfo is True it will (try) to return the title, illust id, artist URL. artist ID/Name, etc.

Example of using saucenao() in a plugin:
```
sn_kwgs = {}
sn_url, sn_kwgs = utils.saucenao(url, kwargs['saucenao api'], metainfo=True)
print(sn_url)  # The URL of the art (pixiv / whatever other site)
print(sn_kwgs['title'])  # The title of the work
print(sn_kwgs['illust id'])  # The work's ID (which is found in the URL)
print(sn_kwgs['artist'])  # The arist's name
print(sn_kwgs['artist id'])  # The artist's user ID
```

If you just want the (i.e. Pixiv) URL, you can just do:
```
sn_url = utils.saucenao(url, kwargs['saucenao api'])
print(sn_url)  # The URL of the art (pixiv / whatever other site)
```

### Creating a plugin with user authorization

If your plugin needs you to create a authorization code through code (like dropbox) please make sure you also create a (for example) dropbox_auth.py for users to follow.
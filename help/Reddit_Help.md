reddit
======
### Third party libraries
* [RoboBrowser](https://github.com/jmcarp/robobrowser)
* [HTML5Lib](https://github.com/html5lib/html5lib-python)
* [lxml](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)
* [Requests](http://www.python-requests.org/en/latest/user/install/#install)
* [Pillow](http://pillow.readthedocs.org/en/latest/installation.html)

### Options
* Subreddits [string]
  * The subreddits you want to grab images from (i.e. ecchi, catgirls)
* Random Subreddit [True or False]
  * If True it will randomly pick one of the subreddits you set in Subreddits, else it will go in order (i.e. ecchi then catgirls, back to ecchi, ect.)
* Random Link [True or False]
  * If True it will randomly pick a link out of the subreddit, else it will go from newest post down.
* Save Images [True or False]
  * Keep images into a folder!
  * If False images will be deleted 10 seconds after downloaded (to give it time to post)
* Path [string]
  * Where images will be saved
  * If nothing it will create a folder called "images"
* Filename ["string"]
  * Name what the downloaded files will be
  * You can use {artist}, {character}, {series} and {tags} to put the image infomation into the filename
* Message ["string"]
  * [b]PUT THIS SETTINGS IN QUOTES (Look at examples)[\b]
  * Include a message in your tweets
  * You can use {title} to use the topic's title and {url} to return the topic reddit URL.
  * If you have set your SauceNAO API you can also use: {sn title}, {sn illust id}, {sn illust url}, {sn artist}, {sn artist id} and {sn artist url}

### Examples

```
[reddit]
Subreddits = ecchi, nekogirls
Random Subreddit = True
Random Link = True
Message = {title} - {url}
```
```
[reddit]
Subreddits = ecchi
Random Link = False
Message = {title}
```
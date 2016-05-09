sankaku, danbooru, safebooru
======
### Third party libraries
* [RoboBrowser](https://github.com/jmcarp/robobrowser)
* [HTML5lib](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)
* [Requests](http://www.python-requests.org/en/latest/user/install/#install)
* [Pillow](http://pillow.readthedocs.org/en/latest/installation.html)

### Options
* Login [True or False]
  * Login on the website (if you want to remove the 2tag limit on danbooru, etc.)
* Username [string]
  * Your username for logging in
* Password [string]
  * Your password for logging in
* Used Images [string]
  * Set the location of your whatever-used-links.txt
  * This will be used so the bot knows what urls have been used to not repost
  * Not setting this will automaticaly create one
* Highest Page [int]
  * The highest page to search for (default: 50)
* Tags [string]
  * The tags you want to search on the site!
  * Separate tags with ", " (1girl, 1boy, smile)
  * Ignore tags with "-" (2girl, -1boy, yuri, -yaoi)
  * For safe-for-work stuff add "rating:safe" (1girl, rating:safe)
     * This is NOT needed for safebooru
  * Search in order of popularity (sankaku: "order:popular", danbooru: "score:100", safebooru: "score:>=10")
     * Feel free to look at their cheat sheet for tags ([sankaku](https://chan.sankakucomplex.com/wiki/show?title=help%3A_quick_guide), [danbooru](https://danbooru.donmai.us/wiki_pages/43049), [safebooru](http://safebooru.org/index.php?page=help&topic=cheatsheet))
  * Note the tag limit for these sites! (sankaku: 5 tags (9 logged in), danbooru: 2 tags (more logged in), safebooru: 9 tags)
* Ignore Tags [string]
  * These tages will be ignored if they are found on the image tag list!
  * Use this if you are limited on doing so many tags.
  * Separate tags with ", " (pony, furry)
* Ignore Cosplay [True or False]
  * If you're making a bot for only some charaters use this!
  * It will ignore cosplayers!
* Accept WebM [True or False]
  * Accept and convert WebMs (make sure you have set up your webm script and script location)
  * This will be ignored with safebooru as it does not have webms
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
  * You can use {artist}, {character}, {series} and {tags} to put the image infomation into your tweet
  * If you want to share the url use {url}
  * You can also use {#artist}, {#character}, {#series} and {#tags} to make each one hashtagged
  * If you have set your SauceNAO API you can also use: {sn title}, {sn illust id}, {sn illust url}, {sn artist}, {sn artist id} and {sn artist url}


### Examples

```
[sankaku]
Highest Page = 100
Tags = 1girl, order:popular, rating:safe, -3d
Ignore Tags = Furry, Pony, My Little Pony, Flash
Accept WebM = True
Save Images = True
Filename = 
Message = "{#tags}"
```
```
[danbooru]
Login = True
Username = my_username
Password = my_password
Tags = 1girl, -1boy
```
```
[safebooru]
tags = 1girl
```

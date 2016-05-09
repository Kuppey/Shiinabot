# this is bad and i'm lost


ImageTweet
======
**ImageTweet** is a simple way to create and manage your Twitter image bots.

For the latest (stable) .zip go to [releases](https://github.com/ace3df/ImageTweet/releases)

## Usage
* Python 3.4+ only
* Download zip or git clone
* Install needed third party libraries (read below)
* Create your account(s) and put them into /acounts/ (it will ignore files with "example" in it)
* Get the requared packages from the plugin(s) you are going to use
* Put the plugin(s) you are going to use into the 'plugins' folder
* Open imagetweet.py
* Enjoy!

### Third party libraries
* [Tweepy](https://github.com/tweepy/tweepy)
    * pip install tweepy
* [ConfigObj](https://pypi.python.org/pypi/configobj/)
    * pip install configobj

### Settings Help
* [For all the settings you can do read this](https://github.com/ace3df/ImageTweet/blob/master/help/Settings_Help.md)
* If you want to repeat a plugin (i.e. folder twice, danbooru once (back to folder twice, etc.)), add P_REPEAT to the plugin options. This works for EVERY plugin including your own. [Example here](https://github.com/ace3df/ImageTweet/blob/master/accounts/Repeating_Example.ini#L14)

### Plugin: folder
* Nothing.

For options with this plugin [read here](https://github.com/ace3df/ImageTweet/blob/master/help/Folder_Help.md)

### Plugin: sankaku, danbooru, safebooru
* [RoboBrowser](https://github.com/jmcarp/robobrowser)
* [HTML5Lib](https://github.com/html5lib/html5lib-python)
* [Requests](http://www.python-requests.org/en/latest/user/install/#install)
* [Pillow](http://pillow.readthedocs.org/en/latest/installation.html)

For options with this plugin [read here](https://github.com/ace3df/ImageTweet/blob/master/help/Imageboard_Help.md)

### Plugin: reddit
* [RoboBrowser](https://github.com/jmcarp/robobrowser)
* [HTML5Lib](https://github.com/html5lib/html5lib-python)
* [lxml](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)

For options with this plugin [read here](https://github.com/ace3df/ImageTweet/blob/master/help/Reddit_Help.md)

## Want to post using X ?
Simple! Either request it in a issue or contact me on Twitter.

You can also create a pullrequest if you have done another way yourself and want to share it (or if you have fixed one of my many; many bugs!

If you do want to create your own [here is a quick help!](https://github.com/ace3df/ImageTweet/blob/master/help/Creating_Plugins_Help.md)

## License 
* see [LICENSE](https://github.com/ace3df/ImageTweet/blob/master/LICENSE.md) file

## Contact 
* Twitter: [@ace3df](https://twitter.com/ace3df)

## Donate
I'm poor, buy me pizza please.

Donations also go into looking at plugins that need to use or have a paid services (like Danbooru and Pixiv)

[Paypal](https://www.paypal.me/ace3df)

[Patreon](https://www.patreon.com/ace3df)


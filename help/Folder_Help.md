folder
======
### Third party libraries
* None

### Options
* Folder [string]
  * Where your images are stored
* After Type [int/string]
  * What happens to the image after it is used
  * Use 1 or "move to folder" to move the image to folder so you know it was used
  * Use 2 or "text file" to add the filename to a .txt so the bot knows what it used
  * This will creat a filenamed Used Images.txt if "used images" is not set
* Move Folder [string]
  * Use only when After Type is 1 or "move to folder"
  * The full path of your folder to where images will be moved at
* Used Images [string]
  * Use only when After Type is 2 or "text file"
  * The full location of your whatever-used-images.txt
  * This holds the filenames of images that have been posted
* Reset Images [True or False]
  * If there are only less than 4 images left it will use one of them and then reset the used links. This is to lower the chance of reuses and not to suddenly stop the bot.
* Message ["string"]
  * [b]PUT THIS SETTINGS IN QUOTES (Look at examples)[\b]
  * Include a message in your tweets
  * You can use {filename clean}, {filename}, {index} or {hash} in your message
  * {filename clean} will clean up your filename replace "_" with a space and converting "(questionmark)" to ? as well as "(star)" to *
  * {filename} will use the raw filename
  * If you have set your SauceNAO API you can also use: {sn title}, {sn illust id}, {sn illust url}, {sn artist}, {sn artist id} and {sn artist url}

### Examples

```
[folder]
Folder = C:\images
After Type = 1
Move Folder = C:\images\used
Message = "[{index}] #moe #cute"
```
```
[folder]
Folder = C:\images
After Type = "text file"
Used Images = C:\images\used images.txt
Message = "Hi twitter!"
```
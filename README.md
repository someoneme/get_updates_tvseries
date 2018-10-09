# Summer Internship Hiring Challenge
## Problem Statement
The script requires the email address and list of favorite TV series for multiple users as input. The prompt needs to be as follows:
- Email address:
- TV Series:
- Store the input data in MySQLdb table(s).

## Desired Output
A single email needs to be sent to the input email address with all the appropriate response for every TV series. The content of the mail could depend on the following use cases:
- An exact date is mentioned for the next episode.
- Only year is mentioned for next season.
- All the seasons are finished and no further details are available.

## Solution
This application is entirely made on python along with many other libraries such as:-
- wxpython for GUI
- email.mime.multipart for email
- email.mime.text for email
- requests for web mining
- re for regular expressions
- BeautifulSoup for web mining
- MySQLdb for MySQLdb

This application can be run in GUI as well as CLI mode. These are the snapshots of this application run on macOS High Sierra. It will take the input of a user, search the web for the release date of that TV show, save it in database and mail the dates to the user.

__Moreover, it can even provide with the time and date if the user has entered the spelling of the tv series wrong, or he may have missed some apostrophe or used short-form of the tv series such as got for the game of thrones__

### GUI MODE
![GUI Mode](https://github.com/someoneme/get_updates_tvseries/blob/master/Screenshots/GUI.png "Get updates")

+ The server email and password will contain the email id and password of the sender. 
+ The email address of the recipient will be contained in the third row. 
+ All the TV Series titles will be written in the box separated by a comma.

![GUI Mode](https://github.com/someoneme/get_updates_tvseries/blob/master/Screenshots/Mail_sent.png "Get updates")

![GUI Mode](https://github.com/someoneme/get_updates_tvseries/blob/master/Screenshots/Mail.png "Get updates")

+ After pressing the send button, a mail will be sent by the server to the recipient. It will contain the list of TV series along with the date/year.

### CLI MODE
![GUI Mode](https://github.com/someoneme/get_updates_tvseries/blob/master/Screenshots/Terminal.png "Get updates")

+ The same application can also be run on the command line where the user has to just enter the email along with his personalized list of TV Series. 

![GUI Mode](https://github.com/someoneme/get_updates_tvseries/blob/master/Screenshots/Mail_terminal.png "Get updates")

+ This way he will get the mail via the command line.

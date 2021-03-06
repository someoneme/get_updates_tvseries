# Source Code
## Mining the web
### Getting the query from user and searching on imdb
```Python
query=Season_split[list_Season].rstrip().lstrip().lower()
data={
  'q': query,
  's': 'tt'
}
r = requests.get('https://www.imdb.com/find/', params=data)
```
### Sorting the TV Series with that name from movies
```Python
for k in soup.find_all("td", {"class": "result_text"}):
  if k.text.split()[-1]=="series)":
    l=k.find_all('a')
    break
```
### Checking if the season is rated or not, i.e. if released or not as well as getting the air date for the next episode
```Python
for i in soup.find_all("div", {"class": "list_item"}):
  for l in i.find_all("span", {"class": "ipl-rating-star__rating"}):
    true_false = l.text=="0"
    break
  if true_false==True: 
    for k in i.find_all("div", {"class": "airdate"}): # Getting the air date for not released episodes.
      date = k.text.lstrip().rstrip()
```
## Using SQL Database
```Python
sql = "INSERT INTO users (email, season) VALUES (%s, %s)"
val = (self.email, self.mov)
cur.execute(sql, val)
```
## Sending Mail
```Python
password = self.spassword
msg['From'] = self.semail
msg['To'] = self.email
msg['Subject'] = "TV Series along with release date"
msg.attach(MIMEText(message, 'plain'))
server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
server.login(msg['From'], password)
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()
```
# Prerequisites
Before being able to run the application, follow these steps:-
+ Remove 2 step verification.
+ Login to your gmail account and allow less secure application. Go to 
https://myaccount.google.com/u/1/lesssecureapps?pageId=none
![GUI Mode](https://github.com/someoneme/get_updates_tvseries/blob/master/Screenshots/less_secure_app.png "Get updates")

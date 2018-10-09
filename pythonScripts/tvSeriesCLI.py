from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import re
from bs4 import BeautifulSoup
import MySQLdb

msg = MIMEMultipart()
message=""
db = MySQLdb.connect(host="localhost",   
                     user="root",       
                     passwd="root",     
                     db="internship") 
cur = db.cursor()
email=[]
tv=[]
n=1
print "Enter Email address : "
email.append(raw_input())
print "Enter TV series name separated by , :"
tv.append(raw_input().split(','))

for list_email in range(n):

	print email[list_email]
	print ""
	sql = "INSERT INTO users (email, season) VALUES (%s, %s)"
    val = (email[list_email], str(tv[list_email]))
    cur.execute(sql, val)

	for list_movie in range(len(tv[list_email])):
		
		query = tv[list_email][list_movie].rstrip().lstrip().lower()
		message = message+"Tv series name: "+query+"\n"
		print "Tv series name: "+query
		month = {"Jan.":"01","Feb.":"02","Mar.":"03","Apr.":"04","May":"05","Jun.":"06","Jul.":"07","Aug.":"08","Sep.":"09","Oct.":"10","Nov.":"11","Dec.":"12"}
		data= {
		    'q': query,
		    's': 'tt'
		    }
		r = requests.get('https://www.imdb.com/find/', params=data)
		soup = BeautifulSoup(r.text.lower() ,'lxml')
		for k in soup.find_all("td", {"class": "result_text"}):
			if k.text.split()[-1]=="series)":
				l=k.find_all('a')
				break

		if len(l)>0:
			new_link = "https://www.imdb.com"+l[0]['href']
			# print("https://www.imdb.com"+l[0]['href'])
		try:
			r = requests.get(new_link)
		except:
			print "Check name"
			exit(0)
		soup = BeautifulSoup(r.text, 'lxml')
		l = soup.find_all('a', href=True)
		for i in l:
			if re.search('season',i['href']):
				latest_season = "https://www.imdb.com/"+i['href']
				# print latest_season
				break

		r = requests.get(latest_season)
		soup = BeautifulSoup(r.text, 'lxml')
		flag=0
		for i in soup.find_all("div", {"class": "list_item"}):
			for l in i.find_all("span", {"class": "ipl-rating-star__rating"}):
				true_false = l.text=="0"
				break
			if true_false==True: 
				for k in i.find_all("div", {"class": "airdate"}):
					date = k.text.lstrip().rstrip()
					if len(date)==4:
						message=message+"Status: The next season begins in "+date+".\n\n"
						print "Status: The next season begins in "+date+".\n"
					else:
						date = date.split()
						if len(date)<1:
							break
						new_date = date[2]+"-"+month[date[1]]+"-"+date[0]
						message=message+"Status: The next episode airs on "+new_date+".\n\n"
						print "Status: The next episode airs on "+new_date+".\n"
					flag=1
					break

			if flag==1:
				break

		if flag==0:
			message=message+"Status: The show has finished streaming all its episodes.\n\n"
			print "Status: The show has finished streaming all its episodes.\n"

password = "your_email_password"
msg['From'] = "your_email_id"
msg['To'] = email[0]
msg['Subject'] = "TV Series along with release date"

if password=="" or msg['From']=="":
	print "Please provide with login Credentials"
 
# add in the message body
msg.attach(MIMEText(message, 'plain'))
 
#create server
server = smtplib.SMTP('smtp.gmail.com: 587')
 
server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 
 
# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
 
server.quit()
 
print "successfully sent email to %s:" % (msg['To'])

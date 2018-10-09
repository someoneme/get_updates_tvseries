import wx
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import re
import time
from bs4 import BeautifulSoup
import MySQLdb

 

class Mywin(wx.Frame): 
    def __init__(self, parent, title):

        db = MySQLdb.connect(host="localhost",   
                     user="root",       
                     passwd="root",     
                     db="internship") 
        cur = db.cursor()
        self.error_flag=0
        self.semail = ""
        self.spassword = ""
        self.email = ""
        self.mov = ""
        super(Mywin, self).__init__(parent, title = title,size = (465,290))
        panel = wx.Panel(self) 
        self.vbox = wx.BoxSizer(wx.VERTICAL) 
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        self.l1 = wx.StaticText(panel, -1, "Server email Address   ")  # Server Email Label 
        self.hbox1.Add(self.l1, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,6) 
        self.t1 = wx.TextCtrl(panel) # Server Email text box
        self.hbox1.Add(self.t1,2,wx.EXPAND|wx.ALIGN_RIGHT|wx.ALL,6)  
        self.vbox.Add(self.hbox1) 
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.l2 = wx.StaticText(panel, -1, "Server email Password ") # Server Email Password
        self.hbox2.Add(self.l2, 1, wx.ALIGN_LEFT|wx.ALL,5) 
        self.t2 = wx.TextCtrl(panel,style = wx.TE_PASSWORD) # Server Email textbox
        self.hbox2.Add(self.t2,2,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.vbox.Add(self.hbox2) 
        self.hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.l5 = wx.StaticText(panel, -1, "Your email Address       ") # Our email Label
        self.hbox5.Add(self.l5, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.t4 = wx.TextCtrl(panel) # Our email textbox
        self.hbox5.Add(self.t4,2,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.vbox.Add(self.hbox5) 
        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL) 
        self.l3 = wx.StaticText(panel, -1, "Season List               ") # Season List Label 
        self.hbox3.Add(self.l3,1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.t3 = wx.TextCtrl(panel,size = (300,100),style = wx.TE_MULTILINE) # Season List Box
        self.hbox3.Add(self.t3,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5) 
        self.vbox.Add(self.hbox3) 
        self.tbtn = wx.Button(panel , -1, "Send me the mail") # Send Button
        self.vbox.Add(self.tbtn,3,wx.EXPAND|wx.ALIGN_CENTER)
        self.tbtn.Bind(wx.EVT_BUTTON,self.OnClicked)
        panel.SetSizer(self.vbox) 
        self.Centre() 
        self.Show() 
        self.Fit()  

    def OnClicked(self,event): 
        self.semail = self.t1.GetValue() # Getting email, passwords and Season names
        self.spassword = self.t2.GetValue()
        self.email = self.t4.GetValue()
        self.mov = self.t3.GetValue()
        self.findSeason() # Finding for Season
        self.cclear() # Clearing screen and displaying next screen

    def cclear(self):
        for child in self.GetChildren():
            child.Destroy() 

        if self.error_flag==0:
            text_print = "Mail Sent"
        else:
            text_print = "  Error  "

        self.hbox6 = wx.BoxSizer(wx.HORIZONTAL) 
        self.l6 = wx.StaticText(self, -1, text_print) # Printing either mail sent or error message
        self.l6.SetFont(wx.Font(100, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.hbox6.Add(self.l6,10, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL,5) 

    def findSeason(self):
        # print self.semail
        # print self.spassword
        # print self.email
        # print self.mov
        sql = "INSERT INTO users (email, season) VALUES (%s, %s)"
        val = (self.email, self.mov)
        cur.execute(sql, val)
        try:
            msg = MIMEMultipart()
            message=""
            Season_split = self.mov.split(',')
            for list_Season in range(len(Season_split)):
                query = Season_split[list_Season].rstrip().lstrip().lower()
                message = message+"Tv series name: "+query+"\n"
                # print "Tv series name: "+query
                month = {"Jan.":"01","Feb.":"02","Mar.":"03","Apr.":"04","May":"05","Jun.":"06","Jul.":"07","Aug.":"08","Sep.":"09","Oct.":"10","Nov.":"11","Dec.":"12"}
                data= {
                    'q': query,
                    's': 'tt'
                    }
                r = requests.get('https://www.imdb.com/find/', params=data) # Searching for Season name on imdb
                soup = BeautifulSoup(r.text.lower() ,'lxml')
                for k in soup.find_all("td", {"class": "result_text"}): # Sorting out TV Series from Movies
                    if k.text.split()[-1]=="series)":
                        l=k.find_all('a')
                        break
                if len(l)>0:
                    new_link = "https://www.imdb.com"+l[0]['href'] # Getting TV Series link
                    # print new_link
                try:
                    r = requests.get(new_link)
                except:
                    exit(0)

                soup = BeautifulSoup(r.text, 'lxml')

                l = soup.find_all('a', href=True)

                for i in l:
                    if re.search('season',i['href']): 
                        latest_season = "https://www.imdb.com/"+i['href'] # Getting link for latest season of that TV Series
                        # print latest_season
                        break


                r = requests.get(latest_season)

                soup = BeautifulSoup(r.text, 'lxml')

                flag=0
                for i in soup.find_all("div", {"class": "list_item"}):
                    for l in i.find_all("span", {"class": "ipl-rating-star__rating"}): # Checking if it is rated or not, i.e. if released or not
                        # print l.text
                        true_false = l.text=="0"
                        # print true_false
                        break


                    if true_false==True: 
                        for k in i.find_all("div", {"class": "airdate"}): # Getting the air date for not released episodes.
                            # print l.text=="0"
                            date = k.text.lstrip().rstrip()
                            # print date
                            if len(date)==4:
                                message=message+"Status: The next season begins in "+date+".\n\n"
                                # print "Status: The next season begins in "+date+".\n"
                            else:
                                date = date.split()
                                if len(date)<1:
                                    break
                                # print date[1]
                                new_date = date[2]+"-"+month[date[1]]+"-"+date[0]
                                message=message+"Status: The next episode airs on "+new_date+".\n\n"
                                # print "Status: The next episode airs on "+new_date+".\n"
                            flag=1
                            break
                    if flag==1:
                        break
                if flag==0:
                    message=message+"Status: The show has finished streaming all its episodes.\n\n"
                    # print "Status: The show has finished streaming all its episodes.\n"

            password = self.spassword # Initializing mail 
            msg['From'] = self.semail
            msg['To'] = self.email
            msg['Subject'] = "TV Series along with release date"
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
            # print "successfully sent email to %s:" % (msg['To'])

        except:
            self.error_flag=1
            # print "Error occured"
		
app = wx.App() 
Mywin(None,  'Summer Internship Hiring Challenge')
app.MainLoop()

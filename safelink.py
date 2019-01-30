#!/usr/bin/env python3

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import urllib

print("Content-type: text/html")
print()



head = """
<!DOCTYPE html>
<html>
	<head>
	<title> Intranet HHS </title>
	<link rel="shortcut icon" href=favicon.ico>
<style>
.row {
  display: flex;
  flex-wrap: wrap;
  padding: 0 4px;
}

/* Create eight equal columns that sits next to each other */
.column {
  flex: 12.5%;
  max-width: 12.5%;
  padding: 0 4px;
}

.column img, iframe { 
  width: 100%;
  max-width: 200px;
  /* margin-top: 8px; */
  vertical-align: middle;
}

/* Responsive layout - makes a two column-layout instead of four columns */
@media screen and (max-width: 1000px) {
  .column {
    flex: 25%;
    max-width: 25%;
  }
}

  /* Responsive layout - makes the two columns stack on top of each other instead of next to each other */
@media screen and (max-width: 800px) {
  .column {
    flex: 50%;
    max-width: 50%;
  }
}

/* Responsive layout - makes the two columns stack on top of each other instead of next to each other */
@media screen and (max-width: 400px) {
  .column {
    flex: 100%;
    max-width: 100%;
  }
}
</style>
	</head>
	
	<body>
		<div class='row'>
			<div class='column'>
				<a href=http://roosters.hhs.nl/ target="_blank"> <img src="afbeeldingen/AlgLesTentRstr.jpg">rooster</a>
				<a href=https://blackboard.hhs.nl target="_blank"> <img src="afbeeldingen/blackboard.jpg" >blackboard</a>
				<a href=http://roosters-reserveer.hhs.nl/ target="_blank"> <img src="afbeeldingen/ReserverenOndRmt.jpg">reserveren ruimten</a>
				<a href=http://roosters-concept.hhs.nl/ target="_blank"> <img src="afbeeldingen/concept-rooster.jpg">concept rooster</a>
			</div>
			<div class='column'>
				<a href=http://docent.osiris.hhs.nl/ target="_blank"> <img src="afbeeldingen/osirisdocent.jpg">osiris</a>
				<a href=https://hhs-onstage.xebic.com/ target="_blank"> <img src="afbeeldingen/onstage.jpg">onstage</a>
				<a href=https://hhs.topdesk.net/tas/public/ target="_blank"> <img src="afbeeldingen/iFrontOffice.jpg">iFrontoffice</a>
			</div>
			<div class='column'>
				<a href=https://desktopmedewerker.hhs.nl/ target="_blank"> <img src="afbeeldingen/applicatieportaal.jpg">desktop</a>
				<a href=https://toetsportaal.hhs.nl/ target="_blank"> <img src="afbeeldingen/toetsportaal.jpg">toetsportaal</a>
				<a href=https://sap-apps.hhs.nl/sap/bc/ui5_ui5/ui2/ushell/shells/abap/FioriLaunchpad.html?sap-language=NL target="_blank"> <img src="afbeeldingen/MijnServiceplein.jpg">mijn serviceplein</a>
				<a href=https://webforms.hhs.nl/private/password/wijzig-wachtwoord.php target="_blank"><img src="afbeeldingen/wachtwoord.png">Wijzig wachtwoord</a>
			</div>
			<div class='column'>
				<a href=https://dehaagsehogeschool.sharepoint.com/sites/medewerkersnet target="_blank"> <img src="afbeeldingen/medewerkersnet.jpg">medewerkersnet</a>
				<a href=https://dehaagsehogeschool.sharepoint.com/sites/studentennet target="_blank"> <img src="afbeeldingen/studentennet.jpg">studentennet (algemeen)</a>
				<a href=https://dehaagsehogeschool.sharepoint.com/sites/TIS_TN-VT target="_blank"> <img src="afbeeldingen/studentennetTN.jpg">studentennet (TN)</a>
				<a href=https://nieuws.hhs.nl target="_blank"><img src="afbeeldingen/hnieuws.jpg">hnieuws</a>
			</div>
			<div class='column'>
				<a href=https://outlook.office365.com/owa/?realm=hhs.nl target="_blank"> <img src="afbeeldingen/outlook.png">webmail</a>
				<a href=https://www.office.com/?auth=2&home=1&from=ShellLogo target="_blank"><img src="afbeeldingen/office365.jpg">office 365</a>
				<a href=https://www.dehaagsehogeschool.nl/studievoorzieningen/bibliotheek target="_blank"><img src="afbeeldingen/bibliotheek.jpg">bibliotheek</a>
			</div>
			<div class='column'>
				<a href=https://www.github.com/hhs-tn target="_blank"><img src="afbeeldingen/github.png">Github TN</a>
				<a href=https://www.masteringphysics.com/site/login.html target="_blank"><img src="afbeeldingen/pearson.jpg">MasteringPhysics login</a>
				<a href=https://hub.docker.com/ target="_blank"><img src="afbeeldingen/docker.jpg">Docker Hub</a>
				<a href=http://quest.eb.com/ target="_blank"><img src="afbeeldingen/britannica.png">Britannica ImageQuest</a>
			</div>
		</div>
"""

foot = """
    </body>
    </html>
    """
   
html_form = """
    <br/>
    Verwijderen van safelinks: <br/>
    <form method="post" action="safelink.py">
    <input type="text" style="width:75%;height:100px;" name="blob"/>
    </form>
    </br/>
"""


#def parse_form(form):
#    for key in form.keys():
#        print(form.getvalue(key))
#        print('<br>')

def parse_blob(blob):
    safe, url = blob.split('url=')
    http = None
    if url.find('^http') > 0:
        http = True
    if http:
        print('<a href="%s" target=_blank>%s</a>'%(url,url))
    else:
        print('<a href="http://%s", target=_blank>%s</a>'%(url,url))

def print_url(data):
    if data.find('url=') < 0:
        print('')
    else:
        safe, url = data.split('url=')
        url = urllib.parse.unquote(url)
        url = url.split('&')[0]
        url = url.strip()
        url = url.lstrip()
        http = None
        if url[0:4].lower() == 'http':
            http = True
        if http:
            print('<a href="%s" target=_blank>%s</a><br/>'%(url,url))
        else:
            print('<a href="http://%s", target="_blank">%s</a><br/>'%(url,url))

    

def parse_form(blob):
    data = blob.split()
    for line in data:
        if line[0:4] == 'http':
            print_url(line)
            print('<br>')

def test_form(form):
    print(head)
    print(html_form)
    if 'blob' in form.keys():
        blob = form['blob']
        parse_form(blob.value)
    print('<br/>')
    print(foot)

if __name__ == '__main__':
    form = cgi.FieldStorage()
    test_form(form)

    #print_front()
    #blob = form['blob']
    #parse_blob(blob.value)
    #print_foot()


'''
Go to https://emea01.safelinks.protection.outlook.com/?url=www.comsol.nl%2Faccess&amp;data=02%7C01%7CD.D.Land%40hhs.nl%7C0cb26f7f42d444bf1d5c08d64efdcfee%7Ca2586b9bf8674b3c93635b435c5dbc45%7C0%7C0%7C636783249358530548&amp;sdata=S2qxv6cx7oxYNtRQpbOOP0Kx%2FXwX1eBhI7WUuMb9zLs%3D&amp;reserved=0 and create an Access Account if you haven't got one already. Once you are logged on, go to https://emea01.safelinks.protection.outlook.com/?url=www.comsol.nl%2Faccess&amp;data=02%7C01%7CD.D.Land%40hhs.nl%7C0cb26f7f42d444bf1d5c08d64efdcfee%7Ca2586b9bf8674b3c93635b435c5dbc45%7C0%7C0%7C636783249358530548&amp;sdata=S2qxv6cx7oxYNtRQpbOOP0Kx%2FXwX1eBhI7WUuMb9zLs%3D&amp;reserved=0. Next, choose “Register your license” and use the license file.
2)      Now you can download via https://emea01.safelinks.protection.outlook.com/?url=www.comsol.nl%2Fproduct-download&amp;data=02%7C01%7CD.D.Land%40hhs.nl%7C0cb26f7f42d444bf1d5c08d64efdcfee%7Ca2586b9bf8674b3c93635b435c5dbc45%7C0%7C0%7C636783249358530548&amp;sdata=LOUgvPVhWs6%2FNmAyDWH6dBsxR44FYBui4Kv53qBf0WI%3D&amp;reserved=0. You can download the DVD image at the bottom of the screen by clicking on “Full DVD download”. During the subsequent installation, a license file will be asked. 
'''


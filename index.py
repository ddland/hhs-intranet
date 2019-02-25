#!/usr/bin/env python3

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import urllib


print("Content-type: text/html")
print()

url_col1 = [
    ('standaard','https://roosters.hhs.nl/','AlgLesTentRstr.jpg','rooster'),
	('standaard','https://blackboard.hhs.nl','blackboard.jpg','blackboard'),
    ('standaard','https://roosters-reserveer.hhs.nl/','ReserverenOndRmt.jpg','reserveren ruimten'),
    ('standaard','https://roosters-concept.hhs.nl/','concept-rooster.jpg','rooster'),
]

url_col2 = [
	('standaard','https://docent.osiris.hhs.nl/','osirisdocent.jpg','osiris'),
    ('standaard','https://hhs-onstage.xebic.com/','onstage.jpg', 'onstage'),
    ('standaard','https://hhs.topdesk.net/tas/public/','iFrontOffice.jpg', 'iFrontoffice'),
]

url_col3 = [
    ('standaard','https://desktopmedewerker.hhs.nl', 'applicatieportaal.jpg', 'desktop'),
    ('standaard','https://toetsportaal.hhs.nl/','toetsportaal.jpg', 'toetsportaal'),
    ('standaard','https://sap-apps.hhs.nl/sap/bc/ui5_ui5/ui2/ushell/shells/abap/FioriLaunchpad.html?sap-language=NL',
        'MijnServiceplein.jpg','Mijn Serviceplein'),
    ('standaard','https://webforms.hhs.nl/private/password/wijzig-wachtwoord.php','wachtwoord.png', 'wijzig wachtwoord'),
]

url_col4 = [
    ('form','https://dehaagsehogeschool.sharepoint.com/sites/medewerkersnet','wiewatwaar.jpg',
        '<form target="_blank" method="get" \
        action="https://dehaagsehogeschool.sharepoint.com/sites/medewerkersnet/_layouts/15/search.aspx/people">\
        <input type="text" name="q"></form>'),
    ('standaard','https://dehaagsehogeschool.sharepoint.com/sites/studentennet', 'studentennet.jpg',
        'studentennet (algemeen)'),
    ('standaard','https://dehaagsehogeschool.sharepoint.com/sites/TIS_TN-VT', 'studentennetTN.jpg',
        'studentennet (TN)'),
    ('standaard','https://nieuws.hhs.nl', 'hnieuws.jpg', 'hnieuws'),
]

url_col5 = [
    ('standaard','https://outlook.office365.com/owa/?realm=hhs.nl','outlook.png','webmail'),
    ('standaard','https://www.office.com/?auth=2&home=1&from=ShellLogo','office365.jpg', 'Office 365'),
    ('standaard','https://www.dehaagsehogeschool.nl/studievoorzieningen/bibliotheek','bibliotheek.jpg','Bibliotheek'),
]

url_col6 = [
    ('standaard','https://www.github.com/hhs-tn','github.png','GitHub TN'),
    ('standaard','https://www.masteringphysics.com/site/login.html','pearson.jpg', 'Mastering Physics'),
    ('standaard','https://hub.docker.com/', 'docker.jpg', 'Docker Hub'),
    ('standaard','http://quest.eb.com/', 'britannica.png', 'Britannica ImageQuest'),
]
 
urls = [url_col1, url_col2, url_col3, url_col4, url_col5, url_col6]
 
head = """
<!DOCTYPE html>
<html>
	<head>
	<title> Intranet HHS </title>
	<link rel="shortcut icon" href=favicon.ico>
    <link rel="stylesheet" type="text/css" href="layout.css">
	</head>
	<body>
"""

foot = """
    </div> <!-- container -->
    </body>
    </html>
    """
   
def print_blocks():
    print(r'<div class="container">')
    for row in urls:
        print(r'<div class="grid-row">')
        for item in row:
            if item[0] == 'standaard':
                print(r'''<div class="grid-item">
                <a href={url} target="_blank">
                <figure>
                <img src="afbeeldingen/{img}">
                <figcaption>{name}</figcaption>
                </figure>
                </a></div>'''.format(url=item[1], img=item[2],name=item[3]))
            elif item[0] == 'form':
                print(r'''<div class="grid-item">
                <figure>
                <a href={url} target="_blank">
                <img src="afbeeldingen/{img}">
                </a>
                <figcaption>{name}</figcaption>
                </figure>
                </div>'''.format(url=item[1], img=item[2],name=item[3]))
        print(r'</div> <!-- grid-row -->')
    print(r'</div> <!-- container -->')

def end_block():
    print(r'''
<div class="full-row">
    Verwijder safelinks: 
    <form method="post">
        <input type="text" style="height:100px;" name="blob"/>
    </form>
</div>
''')
    
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
    print(head)
    print_blocks()
    end_block()
    if 'blob' in form.keys():
        blob = form['blob']
        parse_form(blob.value)
    print(foot)

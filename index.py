#!/usr/bin/env python3

import cgi
#import cgitb; cgitb.enable()
import urllib
import sys
import html_templates

print("Content-type: text/html")
print()

def parse_datafile(data, grid):
    for line in data:
        # skip empty lines and comments
        if line[0] == "#" or line.isspace():
            continue
        cols = line.split(',')
        colnum = int(cols[0])
        deletecolumn = False

        # cleanup whitespace
        for ii, col in enumerate(cols):
            cols[ii] = col.strip()
        if cols[1] == 'standaard':
            htmlstring = [cols[1],html_templates.template_card.substitute(url=cols[3], img=cols[4], text=cols[2])]
        elif cols[1] == 'form':
            htmlstring = [cols[1],html_templates.template_card_form.substitute(url=cols[3], img=cols[4], text=cols[2])]
        elif cols[1] == 'delete':
            deletecolumn = True
            if colnum in grid.keys():
                grid.pop(colnum)
                
        if colnum in grid.keys():
            if not deletecolumn:
                grid[colnum].append(htmlstring)
        else:
            if not deletecolumn:
                grid[colnum] = [htmlstring]

def get_maxrows(grid):
    maxrows = 0
    for key in sorted(grid.keys()):
        if len(grid[key]) > maxrows:
            maxrows = len(grid[key])
    numbercols = sorted(grid.keys())[-1]
    return (maxrows, numbercols+1)

def write_htmlgrid(grid, maxrows, numbercols, outputfile=sys.stdout):
    # get number items, number rows (cols = 12)
    for col in range(numbercols):
        nrows = 0
        if col in grid.keys():
            for line in grid[col]:
                print(line[1], file=outputfile)
                nrows +=1
        while nrows < maxrows:
            print("<div class='card' style='background-color: rgba(158, 167, 0, 0.5);'></div>", file=outputfile)
            nrows +=1
        
def add_userdata(username, data, grid):
    with open("site_%s.md" %(username), "r") as fh:
        data = fh.readlines()
    parse_datafile(data, grid)


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
        return url


def parse_form(blob):
    urls = []
    data = blob.split()
    print("<p>Full text </p>")
    print("""<div class="full-row", style="background-color:rgba(158, 167, 0, 0.5);">""")
    for line in data:
        if line[0:4] == 'http':
            urls.append(print_url(line))
        else:
            line =line.encode('ascii', errors='ignore').decode('ascii')
            print('%s' %str(line), end=' ')
    print("")
    print("</div>")
    print("""<div class="full-row", style="background-color:rgba(158, 167, 0, 0.5);">""")
    print("<p>URLS:</p>")
    for line in urls:
        print(line, "<br>")

if __name__ == "__main__":
    form = cgi.FieldStorage()
    
    filename="default.md"
    htmloutput = sys.stdout #open('script_output.html', 'w')
    grid = {}

    if "sharepoint" in form.keys(): # sharepoint side, geen default!
        sp = form.getvalue("sharepoint")
        if isinstance(sp, str):
            if sp == "derek":
                with open("sharepoint/sharepoint_derek.md", "r") as fh:
                    data = fh.readlines()
                parse_datafile(data, grid)

    if len(grid) < 1: 
        with open(filename, "r") as fh:
            data = fh.readlines()
        parse_datafile(data, grid)


    user = "TN"
    if "user" in form.keys(): # usersettings file detected!
        user = form.getvalue("user")
        if isinstance(user, str):
            if user == "derek":
                add_userdata("derek", data, grid)
            elif user == "voorbeeld":
                add_userdata("voorbeeld", data, grid)
            else:
                user = "TN"


    maxrows, numbercols = get_maxrows(grid)


    print(html_templates.template_header.substitute(
        maxrows  = maxrows,
        maxrows2 = maxrows*2,
        maxrows4 = maxrows*4,
        maxrows8 = maxrows*6,
        user = user.title(),
        ), file=htmloutput)

    write_htmlgrid(grid, maxrows, numbercols, htmloutput)
    print("</div> <!-- card-container -->", file=htmloutput) 

    print(r'''
<div class="full-row" style="background-color:rgba(158, 167, 0, 0.5);">
    Verwijder safelinks: 
    <form method="post">
        <input type="text" style="height:100px;" name="blob"/>
    </form>
</div>
    ''', file=htmloutput)

    if "blob" in form.keys():
        blob = form["blob"]
        parse_form(blob.value)

    print("""
<div class="fullrow" style="background-color:rgba(158, 167, 0, 0.5);"> 
Aanpassingen of gepersonaliseerde omgeving? <a href="mailto:d.d.land@hhs.nl?subject=intranet website">Stuur een mailtje!</a>
</div>""", file=htmloutput)

    print(html_templates.template_footer.substitute(), file=htmloutput)

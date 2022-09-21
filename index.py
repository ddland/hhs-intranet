#!/usr/bin/env python3

import cgi
#import cgitb; cgitb.enable()
from urllib import parse
import sys
import html_templates
import re


bgcolor = "rgba(158, 167, 0, 0.5)"
bgcolordark = "rgba(158, 167, 0)"

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
        elif cols[1] == 'extern':
            htmlstring = [cols[1],html_templates.template_card_extern.substitute(url=cols[3], img=cols[4], text=cols[2])]
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
            print("<div class='card' style='background-color: %s;'></div>" %(bgcolor), file=outputfile)
            nrows +=1
        
def add_userdata(username, data, grid):
    with open("site_%s.md" %(username), "r") as fh:
        data = fh.readlines()
    parse_datafile(data, grid)


def fix_url(url):
    ret = ""
    if url.find('url=') >= 0:
        safe, url = url.split('url=')
        url = parse.unquote(url)
        url = url.split('&')[0]
        url = url.strip()
        ret = url.lstrip()
    return " %s " %(ret), ret


def find_urls(blob):
    p = re.compile("https([^\s]+)")
    pos_urls = []
    start = 0
    i = 0
    all_urls = []
    while i < 100:
        res = re.search(p, blob[start:])
        if not res:
            break
        else:
            sp1 = res.span()
            pos_urls.append((sp1[0]+start, sp1[1]+start))
            start += sp1[1]
        i+= 1
    start = 0
    data = ""
    for pos in pos_urls:
        data += blob[start:pos[0]]
        urls = fix_url(blob[pos[0]:pos[1]])
        all_urls.append(urls[1])
        data += urls[0]
        start = pos[1]
    data += blob[start:]
    return data, all_urls

def print_urls(blob):
    data, urls = find_urls(blob)
    data = data.replace("\n", "<br>")
    data = data.replace("\r", "")
    data = data.encode('ascii', errors='ignore')
    print("""<p>Full text </p>
<div class="full-row", style="background-color:{bgcolor};">
{data}
</div>
<p>URLS:</p>
<div class="full-row", style="background-color:{bgcolor};">
""".format(data=data.decode(), bgcolor=bgcolor))
    for url in urls:
        print("""<a href="%s" target="_blank">%s</a><br>""" %(url, url))
    print("""</div>""")


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
    if "user" in form.keys(): # usersettings file request detected!
        user = form.getvalue("user")
        if isinstance(user, str):
            if user == "derek":
                add_userdata("derek", data, grid)
            elif user == "voorbeeld":
                add_userdata("voorbeeld", data, grid)
            elif user == "sanne":
                bgcolordark = "rgba(160,32,240)"
                bgcolor = "rgba(238, 106, 167)"
            elif user == "thomas":
                bgcolordark = "rgba(0, 172, 193, 0.9)"
                bgcolor = "rgba(178, 235, 242, 0.9)"
                add_userdata("thomas", data, grid)
            else:
                user = "TN"


    maxrows, numbercols = get_maxrows(grid)


    print(html_templates.template_header.substitute(
        maxrows  = maxrows,
        maxrows2 = maxrows*2,
        maxrows4 = maxrows*4,
        maxrows8 = maxrows*6,
        user = user.title(),
	backgroundcolor = bgcolordark,
        ), file=htmloutput)

    write_htmlgrid(grid, maxrows, numbercols, htmloutput)
    print("</div> <!-- card-container -->", file=htmloutput) 

    print(r'''
<div class="full-row" style="background-color:{bgcolor};">
    <form method="post">
        <input type="submit" value="Verwijder safelinks" style="background-color:{bgcolor};"> 
        <textarea wrap="hard" rows=2 style="height:100px;width:100%" name="blob"> </textarea>
    </form>
</div>
    '''.format(bgcolor=bgcolor), file=htmloutput)

    if "blob" in form.keys():
        blob = form["blob"]
        print_urls(blob.value)

    print("""
<br><div class="fullrow" style="background-color:{bgcolor};"> 
Aanpassingen of gepersonaliseerde omgeving? <a href="mailto:d.d.land@hhs.nl?subject=intranet website">Stuur een mailtje!</a>
</div>""".format(bgcolor=bgcolor), file=htmloutput)

    print(html_templates.template_footer.substitute(), file=htmloutput)

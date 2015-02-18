__author__ = 'jamielynch'

from HTMLParser import HTMLParser
import re
import urllib2


class MyHTMLParser(HTMLParser):
    """
    Class for parsing Cheatsheet. The relevant HTML for FA entries currently looks like this:

    <div class="col-md-4 col-sm-6 col-lg-3">
        fa-youtube
        <span class="muted">[&amp;#xf167;]</span>
    </div>
    """

    def __init__(self):
        HTMLParser.__init__(self)

        self.faCodePattern = re.compile("fa-{1}[A-z-]+")
        self.unicodePattern = re.compile("u[A-z0-9]{4}")
        self.tempcode = "none"

        self.famap = {}
        self.tagList = []
        self.isInFaDiv = False

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if "class" == attr[0]:
                currentclass = attr[1]

                if (currentclass == "col-md-4 col-sm-6 col-lg-3"):
                    self.isInFaDiv = True

                if self.isRelevantTag(tag):
                    self.tagList.append(tag)

    def handle_endtag(self, tag):
        if self.isRelevantTag(tag) and self.isInFaDiv:
            self.tagList.pop()

            if "div" == tag:
                self.isInFaDiv = False

    def handle_data(self, data):
        s = re.sub(r'\s+', '', data)

        if (self.isInFaDiv and s != "(alias)"):

            if "div" == self.tagList[-1]:  # Fa code e.g. fa-user
                if len(re.findall(self.faCodePattern, s)) == 1:
                    self.tempcode = s

            elif "span" == self.tagList[-1]:  # in format #xf123;
                s = re.sub(';', '', s)
                s = re.sub('#x', '\u', s)

                if len(re.findall(self.unicodePattern, s)) == 1:
                    self.famap[self.tempcode] = s

    def getFaMap(self):
        return self.famap

    def isRelevantTag(self, tag):
        return "div" == tag or "span" == tag or "i" == tag


def getCheatSheetString():
    """
    Downloads the font awesome cheatsheet from the web and strips unnecessary brackets surrounding unicode
    :return: slightly modified html string of cheatsheet
    """
    try:
        print "Requesting cheatsheet webpage"
        response = urllib2.urlopen("http://fortawesome.github.io/Font-Awesome/cheatsheet/")
        cheatsheet = response.read()
        cheatsheet = re.sub("&amp;", '', cheatsheet)
        cheatsheet = re.sub("[\[\]]", '', cheatsheet)

        print "Successfully read cheatsheet"
        return cheatsheet
    except Exception:
        import traceback

        print "Failed to open URL, aborting program", traceback.format_exc()
        exit(1)


def parseFaCheatSheet():
    parser = MyHTMLParser()
    parser.feed(getCheatSheetString())
    return parser.getFaMap()

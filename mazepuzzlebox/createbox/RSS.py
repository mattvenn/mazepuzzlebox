import feedparser
feed = 'http://www.mattvenn.net/feed/rss/?tag=mazepuzzlebox'
from datetime import date
def getLatestNews():
    ret = []
    channels = feedparser.parse(feed)

    url = ''
    summary = ''
    title = ''
    datepub = ''
    for entry in channels.entries:
        try:
            url = unicode(entry.link, channels.encoding)
            summary = unicode(entry.description, channels.encoding)
            title = unicode(entry.title, channels.encoding)
            #datepub = unicode(entry.date, channels.encoding)
        except:
            url = entry.link
            summary = entry.description
            title = entry.title
            #datepub = entry.date
    
            ret.append( { 'url' : url, 'summary' : summary, 'title' : title , 'date' : datepub } )

    return ret[0:3]

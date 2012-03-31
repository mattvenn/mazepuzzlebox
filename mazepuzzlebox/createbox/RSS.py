import sys
import shelve
from feedcache import cache
from datetime import date

feed = 'http://www.mattvenn.net/feed/rss/?tag=mazepuzzlebox'

def getLatestNews():
    ret = []
    storage = shelve.open('.feedcache' )
    url = ''
    summary = ''
    title = ''
    datepub = ''
    try:
        fc = cache.Cache(storage)
        data = fc.fetch(feed)
        for entry in data.entries:
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
        
    finally:
        storage.close()

    return ret[0:4]

import sys
import shelve
import time
from feedcache import cache
from datetime import date

feed = 'http://www.mattvenn.net/feed/rss2/?tag=mazepuzzlebox'
ttl = 60 * 60 #1 hour
def getLatestNews():
    ret = []
    storage = shelve.open('.feedcache' )
    url = ''
    summary = ''
    title = ''
    datepub = ''
    try:
        fc = cache.Cache(storage,timeToLiveSeconds=ttl)
        data = fc.fetch(feed)
        for entry in data.entries:
            try:
                url = unicode(entry.link, channels.encoding)
                summary = unicode(entry.description, channels.encoding)
                title = unicode(entry.title, channels.encoding)
            except:
                url = entry.link
                summary = entry.description
                title = entry.title
        
            date = entry.updated_parsed
            datestr = time.strftime('%d/%m/%Y',date)
            ret.append( { 'url' : url, 'summary' : summary, 'title' : title , 'date' : datestr } )
        
    finally:
        storage.close()

    return ret[0:4]

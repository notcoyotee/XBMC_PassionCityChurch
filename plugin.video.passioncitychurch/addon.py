import urllib,urllib2,re,xbmcgui,xbmcplugin,time
import HTMLParser
pars = HTMLParser.HTMLParser()
from BeautifulSoup import BeautifulSoup as BeautifulSoup

SpecListOfVideos = [ ]
AllMessages=[ ]
AllSeries=[ ]
AllDates=[ ]

def CATEGORIES():
        addDir("High Quality","http://www.passioncitychurch.com/watch",1,"")
        addDir("Medium Quality","http://www.passioncitychurch.com/watch",1,"")
        addDir("Low Quality","http://www.passioncitychurch.com/watch",1,"")
                       
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        soup = BeautifulSoup(link)
  
        for eachMessage in soup.findAll("td", {"class":"message"}):
            AllMessages.append(eachMessage.text)
        for eachSeries in soup.findAll("td", {"class":"series"}):
            AllSeries.append(eachSeries.text)
        for eachDate in soup.findAll("td", {"class":"date"}):
            AllDates.append(eachDate.text)
        response.close()
        match=re.compile('.*?((?:(?:[1]{1}\\d{1}\\d{1}\\d{1})|(?:[2]{1}\\d{3})))(?![\\d])(\\/)(PCC)(-)(\\d+)(-)((?:[a-z][a-z]*[0-9]+[a-z0-9]*))(-)(High)(\\.)(mov)',re.IGNORECASE).findall(link)
        for s in match:
                specificVideo="".join(map(str,s)).translate(None, "', ()")
                re1='.*?(PCC)(-)(\\d+)(-)(V)(\\d+)'
                rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
                m = rg.search(specificVideo)
                SpecListOfVideos.append(specificVideo)

        for ix in range(len(AllMessages)):
            videoURL= "http://bitcast-g.bitgravity.com/passioncon/passioncitychurch/messages/"+SpecListOfVideos[ix]
            if name=="Medium Quality":
                videoURL=videoURL.replace("High","Medium")
            if name=="Low Quality":
                videoURL=videoURL.replace("High","Low")
            print "GBC : video is :"+videoURL

            messageName=pars.unescape(AllMessages[ix])
            seriesName=AllSeries[ix]
            if not seriesName:
                 seriesName="Generic"
            videoDate=AllDates[ix]
            addLink(seriesName+" : " +messageName+" : " + videoDate,videoURL,'')

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('').findall(link)
        for url in match:
                addLink(name,url,'')
                        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))

from urllib2 import urlopen
from json import load

urlt = 'http://api.citybik.es/sevici.json'
bicis = load(urlopen(urlt))
#print len(bicis)



for i in bicis:
    print i.get('name'),'Identificador:' ,'Número',i.get('number'),'Nº bicis' ,i.get('bikes'),'Libres:',i.get('free')
    print i.get('lat'), i.get('lng')
#print bicis[1].get('name'),'Número :', bicis[1].get('number'), bicis[1].get('bikes'),bicis[1].get('free') 

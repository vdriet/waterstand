""" Ophalen van de waterstand """
import json
from urllib.request import urlopen, Request
from datetime import datetime, timedelta

def leesjson(url):
  """ haal JSON van de URL op """
  req = Request(url=url, headers={'Accept': 'application/json'})
  with urlopen(req) as response:
    contenttekst = response.read().decode('utf-8')
    contentjson = json.loads(contenttekst)
    return contentjson


def leeswaterstandjson(name, abbr):
  """ lees de informatie van bepaalde locatie """
  url = 'https://waterinfo.rws.nl/api/chart/get' + \
       f'?mapType=waterhoogte&locationCode={name}({abbr})&values=-48,48'
  return leesjson(url)


def bepaalstanden(contentjson):
  """ haal de waterstand uit de gegevens """
  laatstetijdgemeten = contentjson['t0']
  gemetenstanden = contentjson['series'][0]['data']
  voorspeldestanden = contentjson['series'][1]['data']

  for stand in gemetenstanden:
    if stand['dateTime'] == laatstetijdgemeten:
      hoogtenu = stand['value']

  if laatstetijdgemeten.endswith('Z'):
    tijdpatroon = '%Y-%m-%dT%H:%M:%SZ'
    deltatijd = 1
  else:
    tijdpatroon = '%Y-%m-%dT%H:%M:%S+02:00'
    deltatijd = 1

  laatstetijdobj = datetime.strptime(laatstetijdgemeten, tijdpatroon) \
                 + timedelta(hours = deltatijd)
  weergavetijd = laatstetijdobj.strftime('%d-%m %H:%M')
  morgenobj = laatstetijdobj + timedelta(days=1)
  morgentekst = morgenobj.strftime(tijdpatroon)

  hoogtemorgen = hoogtenu
  for stand in voorspeldestanden:
    if stand['dateTime'] == morgentekst:
      hoogtemorgen = stand['value']
  returnjson = {}
  returnjson['tijd'] = weergavetijd
  returnjson['nu'] = hoogtenu
  returnjson['morgen'] = hoogtemorgen
  return returnjson

def haalwaterstand(name, abbr):
  """ haal de waterstand van een locatie """
  contentjson = leeswaterstandjson(name, abbr)
  return bepaalstanden(contentjson)

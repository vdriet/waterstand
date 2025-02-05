""" Ophalen van de waterstand """
from datetime import datetime, timedelta

import requests


def leesjson(url):
  """ haal JSON van de URL op """
  try:
    headers = {'Accept': 'application/json'}
    req = requests.get(url, headers=headers, verify=False, timeout=10, allow_redirects=False)
    contentjson = req.json()
    contentjson['resultaat'] = 'OK'
    return contentjson
  except (ConnectionError,
          TimeoutError,
          requests.exceptions.HTTPError,
          requests.exceptions.RequestException) as error:
    return {'resultaat': 'NOK',
            'error': f'Error: Data ophalen mislukt vanwege {error}\nURL: {url}'}


def leeswaterstandjson(name, abbr):
  """ lees de informatie van bepaalde locatie """
  url = 'https://waterinfo.rws.nl/api/chart/get' + \
        f'?mapType=waterhoogte&locationCodes={name}({abbr})&values=-48,48'
  return leesjson(url)


def bepaalstanden(contentjson):
  """ haal de waterstand uit de gegevens """
  if contentjson['resultaat'] == 'NOK':
    return contentjson
  laatstetijdgemeten = contentjson['t0']
  gemetenstanden = contentjson['series'][0]['data']
  voorspeldestanden = contentjson['series'][1]['data']

  hoogtenu = -999
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
                   + timedelta(hours=deltatijd)
  weergavetijd = laatstetijdobj.strftime('%d-%m %H:%M')
  morgenobj = laatstetijdobj + timedelta(days=1)
  morgentekst = morgenobj.strftime(tijdpatroon)

  hoogtemorgen = hoogtenu
  for stand in voorspeldestanden:
    if stand['dateTime'] == morgentekst:
      hoogtemorgen = stand['value']
  returnjson = {'resultaat': 'OK',
                'tijd': weergavetijd,
                'nu': hoogtenu,
                'morgen': hoogtemorgen}
  return returnjson


def haalwaterstand(name, abbr):
  """ haal de waterstand van een locatie """
  contentjson = leeswaterstandjson(name, abbr)
  return bepaalstanden(contentjson)

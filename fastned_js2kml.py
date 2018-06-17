#
# Convert Fastned stations.js file to valid kml.
#

import requests
import json
import re
from datetime import datetime
from jinja2 import Template
from xml.sax.saxutils import escape

url = 'https://route.fastned.nl/stations.js'


def sanitize(obj):
  if isinstance(obj, basestring):
     return escape(obj)
  return obj


def fastned_js2kml():
  r = requests.get(url)
  result = re.search('window\["fastnav"\]\["stations"\]=(.*)\;\}\)\(\)\;$', r.text)
  rawjson = result.group(1)
  stations = json.loads(rawjson)
  exportdate = str(datetime.now().date())

  with open('template.j2', 'r') as f:
    t = Template(f.read())

  filename = 'fastned-{}.kml'.format(exportdate)
  with open(filename, 'w') as f:
    f.write(t.render(exportdate=exportdate,
                     re=re,
                     filter=filter,
                     sanitize=sanitize,
                     stations=stations,
                    ).encode('utf8'))


if __name__ == '__main__':
   fastned_js2kml()

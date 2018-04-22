#
# Convert Fastned stations.js file to valid kml.
#

import requests
import json
import re
from datetime import datetime
from jinja2 import Template

url = 'https://route.fastned.nl/stations.js'


def fastned_js2kml():
  r = requests.get(url)
  js = "["
  js += u'\n'.join(r.text.split('\n')[3:-2])
  js += "]"
  stations = json.loads(js)
  exportdate = str(datetime.now().date())

  with open('template.j2', 'r') as f:
    t = Template(f.read())

  filename = 'fastned-{}.kml'.format(exportdate)
  with open(filename, 'w') as f:
    f.write(t.render(exportdate=exportdate,
                     re=re,
                     filter=filter,
                     stations=stations,
                    ).encode('utf8'))


if __name__ == '__main__':
   fastned_js2kml()

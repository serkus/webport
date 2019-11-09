# -*-  codding: UFT-8 -*-
#/usr/bin/env python3
import requests
from PIL import Image
from io import StringIO 
#req = requests.get('https://api.github.com/events')
payload = {'s': '16'}
req = requests.get('https://iconbird.com/png/download.php?id=15895', params=payload)
#print(r.content)

i = Image.open(StringIO(req.content))

i.save('image')

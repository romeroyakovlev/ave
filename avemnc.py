# -*- coding: utf-8 -*-

from PIL import Image
import StringIO, random, zlib

class myd(dict):
    def __getattr__(self, key):
        return self.get(key,'')
    def __setattr__(self, key, value):
        self[key] = value
    def __add__(self, data):
        return myd(self.items() + data.items())
    def __sub__(self, key):
        return myd((k,v) for (k,v) in self.items() if k != key)

def _loadpic(who,typ,pic):
    return Image.open("./s/avem/%s%s%s.png" % ('' if typ=='bg' else  who+'/', 'hair' if who=='boy' and typ=='head' else typ, pic) ).convert("RGBA")

def img(kv,typ):
    if typ=='bg':
        return _db.bg[int(kv.bg)]
    else:
        return _loadpic(kv.who,typ,int(kv[typ])+1)

_max, _db = myd(), myd(bg=[])
_max['girl'] = myd(bg=5,face=4,clothes=59,mouth=17,head=33,eye=53)
_max['boy'] = myd(bg=5,face=4,clothes=65,mouth=26,head=36,eye=32)

for n in range(6):
    _db.bg.append( Image.open("./s/avem/bg%s.png" % n ).convert("RGBA") )

def compose_image(kv):
    im_base = img(kv,'bg').copy()
    for comp in ('face', 'clothes', 'mouth', 'head', 'eye'):
        p = img(kv,comp)
        im_base.paste(p, (0,0), p)
    return im_base

def draw_item(kv):
    im = compose_image(kv)
    width = kv.get('width',400)
    if width: width = int(width)
    if width < 400:
        im = im.resize((width, width), Image.BICUBIC)
    if kv.gray:
        im = im.convert("LA")
    output = StringIO.StringIO()
    im.save(output, 'PNG')
    contents = output.getvalue()
    output.close()
    return contents

def draw_byhash(kv,newseed=None):
    if kv.hash:
        newseed = zlib.crc32(kv.get('hash'),0)
    elif kv.seed:
        newseed = int(kv.seed)
    if newseed:
        l = []
        for n in sorted(kv.items()):
            l.append('/%s/%s' % n)
        lnk = ''.join(l)
    if not newseed: newseed = random.randrange(0,99999999)
    random.seed(newseed)
    kv.update(seed=newseed)
    for k,v in _max[kv.who].items():
        if not k in kv: 
            if k=='bg': kv[k] = random.randrange(v) + 1
            else: kv[k] = random.randrange(v)
    dat = draw_item(kv)
    return dat

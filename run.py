# -*- coding: utf-8 -*-

import avemnc, exp2
from bottle import route, run, request, response, template, hook, local, static_file, post, redirect


@route('/<who:re:boy|girl>')
@route('/<who:re:boy|girl>/<kv:path>')
def boy_girl(who,kv=''):
    response.content_type = 'image/png'
    mkv = mkkv(kv)+{'who': who}
    cache = 0
    if 'hash' in mkv or 'seed' in mkv: cache = 1
    if 'bg' in mkv and 'face' in mkv and 'clothes' in mkv and 'mouth' in mkv and 'head' in mkv and 'eye' in mkv: cache = 1
    if cache == 1:
        expires, cc = exp2.eh()
        response.set_header('Expires', expires)
        response.set_header('Cache-Control', cc)
    return avemnc.draw_byhash(mkv)


@route('/')
def test_page():
    return '''
<html><head><title>ave api</title>
<style>
.imgfr { margin:0 0 10px 0; padding:6px; border:1px solid #CCCCCC; background-color:#FFFFFF; border-radius:50% }
.img { border-radius:50%;background-color:#EEEEEE }
</style>
</head><body bgcolor="#F2F2F2">
<table width="100%"><tr><td width="1%">
<div class="imgfr"><img src="/boy/bg/0/gray/1/width/200" class="img"></div>
</td>
<td align="center">ave api</td><td width="1%">
<div class="imgfr"><img src="/girl/bg/0/width/200" class="img"></div>
</td></tr></table>
<p><b>/girl</b>/параметры или <b>/boy</b>/параметры, где:</p>
<p><b>/width/400</b> - размер квадрата, до 400 px.</p>
<p><b>/bg/0</b> - нулевой фон (прозрачный)</p>
<p><b>/gray/1</b> - обесцвечивание</p>
<p><b>/hash/строка</b> - строка, по которой строится зерно. одна и та же строка всегда будет давать одну и ту же картинку</p>
<p><b>/seed/число</b> - контрольная сумма, которая получается по хэш-строке. можно задать напрямую, например:

<pre>import zlib
print zlib.crc32('123',0)
# -2008521774</pre>
можно сравнить <a href="/boy/hash/123">hash/123</a> и <a href="/boy/seed/-2008521774">seed/-2008521774</a>

<p>На основе http://8biticon.com/, иконки взяты на основе лицензии MIT</p>
</body></html>
'''

def mkkv(k):
    a = k.split('/')
    if a[-1] == '': a.pop()
    return avemnc.myd(zip(a[0::2], a[1::2]))

run(host='127.0.0.1',port=40000)

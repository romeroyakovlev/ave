from datetime import datetime, timedelta, tzinfo

class GMT(tzinfo):
  def utcoffset(self, dt):
    return timedelta(hours=10) # + self.dst(dt)
  def tzname(self, dt):
    return "GMT"
  def dst(self, dt):
    return timedelta(0)

DELTA = timedelta(days=30)
DELTA_SECONDS = DELTA.days * 86400 + DELTA.seconds
gmt = GMT()
EXPIRATION_MASK = "%a, %d %b %Y %H:%M:%S %Z"


def eh():
    expiration = datetime.now()
    expiration = expiration.replace(tzinfo=gmt)
    expiration = expiration + DELTA
    return expiration.strftime(EXPIRATION_MASK), "public,max-age=%s" % DELTA_SECONDS
from PIL import Image, ImageDraw
from time import time

__bitmapRenderCache: dict[str, dict] = {}
__addedToCacheAt: dict[int, str] = {}


def clearBitmapCache():
    global __bitmapRenderCache, __addedToCacheAt

    now = int(time())

    # Remove all entries older than 24h
    cutoff = now - 86400

    for t in list(__addedToCacheAt.keys()):
        if t < cutoff:
            k = __addedToCacheAt[t]
            del __addedToCacheAt[t]
            del __bitmapRenderCache[k]


def cachedBitmapText(text: str, font) -> tuple[int, int, Image.Image]:
    global __bitmapRenderCache, __addedToCacheAt

    # cache the bitmap representation of the stations string
    nameTuple = font.getname()
    fontKey = ""
    for item in nameTuple:
        fontKey = fontKey + item
    key = text + fontKey
    if key in __bitmapRenderCache:
        # found in cache; re-use it
        pre = __bitmapRenderCache[key]
        bitmap = pre["bitmap"]
        txt_width = pre["txt_width"]
        txt_height = pre["txt_height"]
    else:
        # not cached; create a new image containing the string as a monochrome bitmap
        _, _, txt_width, txt_height = font.getbbox(text)
        bitmap = Image.new("L", (txt_width, txt_height), color=0)
        pre_render_draw = ImageDraw.Draw(bitmap)
        pre_render_draw.text((0, 0), text=text, font=font, fill=255)
        # save to render cache
        __bitmapRenderCache[key] = {
            "bitmap": bitmap,
            "txt_width": txt_width,
            "txt_height": txt_height,
        }
        # Add current timestamp and key to cache index
        __addedToCacheAt[int(time())] = key
    return txt_width, txt_height, bitmap

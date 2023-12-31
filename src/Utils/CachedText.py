from PIL import Image, ImageDraw

bitmapRenderCache: dict[str, dict] = {}


def cachedBitmapText(text: str, font) -> tuple[int, int, Image.Image]:
    # cache the bitmap representation of the stations string
    nameTuple = font.getname()
    fontKey = ""
    for item in nameTuple:
        fontKey = fontKey + item
    key = text + fontKey
    if key in bitmapRenderCache:
        # found in cache; re-use it
        pre = bitmapRenderCache[key]
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
        bitmapRenderCache[key] = {
            "bitmap": bitmap,
            "txt_width": txt_width,
            "txt_height": txt_height,
        }
    return txt_width, txt_height, bitmap

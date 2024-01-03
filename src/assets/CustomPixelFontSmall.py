from PIL import ImageFont
import os

SmallFont_Size = 13
SmallFont = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), "./CustomPixelFontSmall.ttf"),
    SmallFont_Size,
    layout_engine=ImageFont.Layout.BASIC,
)

from PIL import ImageFont

SmallFont_Size = 13
SmallFont = ImageFont.truetype(
    "./assets/CustomPixelFontSmall.ttf",
    SmallFont_Size,
    layout_engine=ImageFont.Layout.BASIC,
)

from PIL import ImageFont

CustomPixelFont_Size = 19
CustomPixelFont = ImageFont.truetype(
    "./assets/CustomPixelFont.ttf",
    CustomPixelFont_Size,
    layout_engine=ImageFont.Layout.BASIC,
)

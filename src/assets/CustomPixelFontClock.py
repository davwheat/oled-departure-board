from PIL import ImageFont

ClockFont_Size = 15
ClockFont = ImageFont.truetype(
    "./assets/CustomPixelFontClock.ttf",
    ClockFont_Size,
    layout_engine=ImageFont.Layout.BASIC,
)

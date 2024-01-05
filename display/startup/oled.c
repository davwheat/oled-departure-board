#include <bcm2835.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include "ssd1322.h"

#define SCREEN_WIDTH 256
#define SCREEN_HEIGHT 64

uint8_t calculate_centred_text_x(char *text)
{
  const int textLength = strlen(text);

  uint8_t x = (SCREEN_WIDTH - (textLength * AsciiLibCharWidth)) / 2;

  return x;
}

void oled_centred_text(char *text, uint8_t y)
{
  uint8_t x = calculate_centred_text_x(text);
  er_oled_string(x, y, text, 0);
}

int main(int argc, char **argv)
{
  time_t now;
  struct tm *timenow;

  printf("** Starting display **\n");

  if (!bcm2835_init())
  {
    printf("BCM2835 init failed\n");
    return -1;
  }

  er_oled_begin();
  er_oled_clear();

  oled_centred_text("Starting departure board", 0);
  oled_centred_text("This will take a few minutes", AsciiLibCharHeight);

  // uint8_t clockY = SCREEN_HEIGHT - AsciiLibCharHeight + 3;
  // char timeStr[9] = "";

  // while (1)
  // {
  //   time(&now);
  //   timenow = localtime(&now);

  //   sprintf(timeStr, "%02d:%02d:%02d", timenow->tm_hour, timenow->tm_min, timenow->tm_sec);

  //   // +3 due to spacing at bottom of digits
  //   oled_centred_text(timeStr, clockY);
  // }

  bcm2835_spi_end();
  bcm2835_close();

  return 0;
}

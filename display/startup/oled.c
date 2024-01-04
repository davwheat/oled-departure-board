#include <bcm2835.h>
#include <stdio.h>
#include <time.h>
#include "ssd1322.h"

int main(int argc, char **argv)
{
  time_t now;
  struct tm *timenow;

  if (!bcm2835_init())
  {
    printf("bcm2835 init failed\r\n");
    return -1;
  }

  er_oled_begin();
  er_oled_clear();

  while (1)
  {
    time(&now);
    timenow = localtime(&now);

    er_oled_string(56, 32, "Starting display", 0);

    char str[] = sprintf("%2d:%2d:%2d", timenow->tm_hour, timenow->tm_min, timenow->tm_sec);
    er_oled_string(96, 16, str, 0);

    // er_oled_char(96, 16, value[timenow->tm_hour / 10], 0);
    // er_oled_char(104, 16, value[timenow->tm_hour % 10], 0);
    // er_oled_char(112, 16, ':', 0);
    // er_oled_char(120, 16, value[timenow->tm_min / 10], 0);
    // er_oled_char(128, 16, value[timenow->tm_min % 10], 0);
    // er_oled_char(136, 16, ':', 0);
    // er_oled_char(144, 16, value[timenow->tm_sec / 10], 0);
    // er_oled_char(152, 16, value[timenow->tm_sec % 10], 0);
  }

  bcm2835_spi_end();
  bcm2835_close();
  return 0;
}

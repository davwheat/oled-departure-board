/***************************************************
//Web: http://www.buydisplay.com
EastRising Technology Co.,LTD
Examples for ER-OLEDM032-1
Display is Hardward SPI 4-Wire SPI Interface 
Tested and worked with: 
Works with Raspberry pi
****************************************************/

#include <bcm2835.h>
#include <stdio.h>
#include <time.h>
#include "ssd1322.h"

char value[10] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
int main(int argc, char **argv)
{
    time_t now;
    struct tm *timenow;


    if(!bcm2835_init()) {
        printf("bcm2835 init failed   !!! \r\n");
        return -1;
    } else {
        printf("bcm2835 init success  !!! \r\n");
    }

    printf("OLED begin\r\n");
    er_oled_begin();
    printf("OLED clear\r\n");
    er_oled_clear();
    printf("OLED bitmap-grqy\r\n");
    er_oled_bitmap_gray(PIC1);
    bcm2835_delay(3000);
    printf("OLED clear\r\n");
    er_oled_clear();
    printf("OLED bitmap-grqy\r\n");
    er_oled_bitmap_gray(PIC2);
    bcm2835_delay(3000);
    printf("OLED clear\r\n");
    er_oled_clear();
    printf("OLED bitmap-monochrome\r\n");
    er_oled_bitmap_mono(PIC3);
    bcm2835_delay(3000);
 

    printf("OLED clear\r\n"); 
    er_oled_clear(); 

    printf("OLED string move\r\n"); 
    er_oled_string(0, 0, "********************************",0);  
    er_oled_string(32, 16, "EastRising Technology",  0); 
    er_oled_string(40, 32, "www.buydisplay.com",  1); 
    er_oled_string(0, 48, "********************************",0); 
    uint8_t i;
    for(i=0;i<=48;i++)
    {
    er_oled_command(0xa1); //start line
    er_oled_data(i);
    delay(100);
    }
    for(i=48;i>0;i--)
    {
    er_oled_command(0xa1); //start line
    er_oled_data(i);
    delay(100);
    }
  

    printf("OLED clear\r\n"); 
    er_oled_clear(); 

    printf("OLED display time\r\n");
    while(1)
    {
        time(&now);
        timenow = localtime(&now);

	if((timenow->tm_sec % 2)==0)
        er_oled_string(56, 32, "www.buydisplay.com", 0); 
        else
        er_oled_string(56, 32, "www.buydisplay.com", 1); 

        er_oled_char(96, 16, value[timenow->tm_hour / 10], 0);
        er_oled_char(104, 16, value[timenow->tm_hour % 10], 0);
        er_oled_char(112, 16, ':', 0);
        er_oled_char(120, 16, value[timenow->tm_min / 10], 0);
        er_oled_char(128, 16, value[timenow->tm_min % 10], 0);
        er_oled_char(136, 16, ':', 0);
        er_oled_char(144, 16, value[timenow->tm_sec / 10], 0);
        er_oled_char(152, 16, value[timenow->tm_sec % 10], 0);
             
    }
    bcm2835_spi_end();
    bcm2835_close();
    return 0;
}


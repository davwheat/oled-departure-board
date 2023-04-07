#include <bcm2835.h>
#include <stdio.h>
#include "ssd1322.h"
#define WIDTH 256
#define HEIGHT 64

#define RST 25
#define DC  24

void er_oled_command(char cmd) {
    bcm2835_gpio_write(DC, LOW);
    bcm2835_spi_transfer(cmd);
}

void er_oled_data(char dat) {
    bcm2835_gpio_write(DC, HIGH);
    bcm2835_spi_transfer(dat);
}

void er_oled_begin()
{
    bcm2835_gpio_fsel(RST, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(DC, BCM2835_GPIO_FSEL_OUTP);

    bcm2835_spi_begin();
    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);     //The default
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);                  //The default
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_2048);  //The default
    bcm2835_spi_chipSelect(BCM2835_SPI_CS0);                     //The default
    bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);     //the default

    bcm2835_gpio_write(RST, HIGH);
    bcm2835_delay(10);
    bcm2835_gpio_write(RST, LOW);
    bcm2835_delay(10);
    bcm2835_gpio_write(RST, HIGH);

    
    er_oled_command(0xFD); /*SET COMMAND LOCK*/ 
    er_oled_data(0x12); /* UNLOCK */ 
    er_oled_command(0xAE); /*DISPLAY OFF*/ 
    er_oled_command(0xB3);/*DISPLAYDIVIDE CLOCKRADIO/OSCILLATAR FREQUANCY*/ 
    er_oled_data(0x91); 
    er_oled_command(0xCA); /*multiplex ratio*/ 
    er_oled_data(0x3F); /*duty = 1/64*/ 
    er_oled_command(0xA2); /*set offset*/ 
    er_oled_data(0x00);
    er_oled_command(0xA1); /*start line*/ 
    er_oled_data(0x00); 
    er_oled_command(0xA0); /*set remap*/
    er_oled_data(0x14); 
    er_oled_data(0x11);
  	
    er_oled_command(0xAB); /*funtion selection*/ 
    er_oled_data(0x01); /* selection external vdd */ 
    er_oled_command(0xB4); /* */ 
    er_oled_data(0xA0);
    er_oled_data(0xfd); 
    er_oled_command(0xC1); /*set contrast current */ 
    er_oled_data(0x80); 
    er_oled_command(0xC7); /*master contrast current control*/ 
    er_oled_data(0x0f); 
  	
    er_oled_command(0xB1); /*SET PHASE LENGTH*/
    er_oled_data(0xE2); 
    er_oled_command(0xD1); /**/
    er_oled_data(0x82); 
    er_oled_data(0x20); 
    er_oled_command(0xBB); /*SET PRE-CHANGE VOLTAGE*/ 
    er_oled_data(0x1F);
    er_oled_command(0xB6); /*SET SECOND PRE-CHARGE PERIOD*/
    er_oled_data(0x08); 
    er_oled_command(0xBE); /* SET VCOMH */ 
    er_oled_data(0x07); 
    er_oled_command(0xA6); /*normal display*/ 
    er_oled_command(0xAF); /*display ON*/   

}


void er_oled_SetWindow(uint8_t Xstart, uint8_t Ystart, uint8_t Xend, uint8_t Yend)
{ 
  er_oled_command(0x15);
  er_oled_data(Xstart+0x1c);
  er_oled_data(Xend+0x1c);
  er_oled_command(0x75);
  er_oled_data(Ystart);
  er_oled_data(Yend);
  er_oled_command(0x5c);//write ram command
}

void er_oled_clear()
{int i,row;
  er_oled_command(0x15);
  er_oled_data(0x00); //col start
  er_oled_data(0x77); //col end 
  er_oled_command(0x75);
  er_oled_data(0x00); //row start
  er_oled_data(0x7f);  //row end 
  er_oled_command(0x5c); 
  for (row = 0; row < 128; row++) {              
        for(i = 0; i< 240; i++ ) {
          er_oled_data(0x00);// write data       
        }        
  }
}

void er_oled_char(uint8_t x, uint8_t y,  char  acsii, uint8_t mode)
{ uint8_t i, str ;uint16_t OffSet;
  x=x/4;
  OffSet = (acsii - 32)*16;
  er_oled_SetWindow(x, y, x+1, y+15);
  for (i=0;i<16;i++)
  {     str =AsciiLib[OffSet + i];  
        if(mode) str=~str;
         er_oled_Data_processing (str);             
  }
}



void er_oled_string(uint8_t x, uint8_t y, char *pString,  uint8_t Mode)
{     
  while(1)
  {
        if (*pString == 0)
        {
            return;
        }
            er_oled_char(x, y, *pString,Mode);
            x += 8;
            pString += 1;              
  }   
}

void er_oled_Data_processing(uint8_t temp)  //turns 1byte B/W data to 4 bye gray data  with 8 Pixel
{uint8_t temp1,temp2;

  if(temp&0x80)temp1=0xf0;
  else temp1=0x00;
  if(temp&0x40)temp2=0x0f;
  else temp2=0x00;
  temp1=temp1|temp2;
  er_oled_data(temp1); //Pixel1,Pixel2
  if(temp&0x20)temp1=0xf0;
  else temp1=0x00;
  if(temp&0x10)temp2=0x0f;
  else temp2=0x00;
  temp1=temp1|temp2;
  er_oled_data(temp1);  //Pixel3,Pixel4                
  if(temp&0x08)temp1=0xf0;
  else temp1=0x00;
  if(temp&0x04)temp2=0x0f;
  else temp2=0x00;
  temp1=temp1|temp2;
  er_oled_data(temp1);  //Pixel5,Pixel6               
  if(temp&0x02)temp1=0xf0;
  else temp1=0x00;
  if(temp&0x01)temp2=0x0f;
  else temp2=0x00;
  temp1=temp1|temp2;
  er_oled_data(temp1);  //Pixel7,Pixel8               
}

void er_oled_bitmap_mono(const uint8_t  * pBuf)
{ uint8_t row,col; 
  er_oled_SetWindow(0, 0, 255/4, 63);
  for (row = 0; row < 64; row++) {              
        for(col = 0;col<256/8; col++ ) {      
       er_oled_Data_processing(pBuf[col+row*32]);              
        }
  }    	
}

void er_oled_bitmap_gray(const uint8_t  * pBuf)
{   uint8_t row,col; 
  er_oled_SetWindow(0, 0, 255/4, 63);
  for (row = 0; row < 64; row++) {              
        for(col = 0;col<128; col++ ) {
        er_oled_data(pBuf[col+row*128]);     
        }
  }    	
}
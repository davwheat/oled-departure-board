CC         = gcc

# Compiler flags to compile for code size
CFLAGS    += -O0 -flto -Wall -ffunction-sections -fdata-sections -fno-builtin

oled:oled.o ssd1322.o
	$(CC) $(CFLAGS) -Wall -o oled oled.o ssd1322.o -lbcm2835
ssd1322.o:ssd1322.c ssd1322.h
	$(CC) $(CFLAGS) -Wall -c ssd1322.c -lbcm2835
oled.o:oled.c ssd1322.h 
	$(CC) $(CFLAGS) -Wall -c oled.c -lbcm2835
clean:
	rm ssd1322.o oled.o oled

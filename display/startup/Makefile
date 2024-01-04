oled:oled.o ssd1322.o
	gcc -Wall -o oled oled.o ssd1322.o -lbcm2835
ssd1322.o:ssd1322.c ssd1322.h
	gcc -Wall -c ssd1322.c -lbcm2835
oled.o:oled.c ssd1322.h 
	gcc -Wall -c oled.c -lbcm2835
clean:
	rm ssd1322.o oled.o oled

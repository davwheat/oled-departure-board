# OLED departure board

## Equipment

- Raspberry Pi 4
- [256x64 SPI OLED display](https://www.buydisplay.com/yellow-3-2-inch-arduino-raspberry-pi-oled-display-module-256x64-spi)

## Setup instructions

### Install BCM2835 C library

The BCM2835 was used on the 1st gen Raspberry Pis but future models have maintained backwards compatibility in terms of GPIO access to the extent that the kernel developers have chosen to [report the BCM2835 as used in even modern Pis](https://forums.raspberrypi.com/viewtopic.php?t=245384).

We need to install a C library in order to access the GPIO pins and other features of the Pi within our application.

```
cd reference/bcm2835-1.71
./configure
make
sudo make check
sudo make install
```

These commands will build, test, and install the BCM2835 C library onto your Raspberry Pi.

### Test the OLED

If you're using the same OLED display as me, the seller provides a test program which you can use.

You'll need the BCM2835 library from the last step already installed.

```
cd reference/SPI_Interface
make
sudo ./oled
```

The test app should cycle through various monochrome bitmaps, before displaying the time and an cycling advert for "www.buydisplay.com".

<details>
<summary>Pictures of the test script running on the display.</summary>

![Display showing an image of various pandas, alongside text "www.buydisplay.com"](./docs/img/oled_test/pandas.jpg)

![Display the current time, alongside text "www.buydisplay.com"](./docs/img/oled_test/time.jpg)

</details>
# AutoCAN_Compute

A CAN bus connected Raspberry Pi to perform the tasks that are not so easy to do with an Arduino-like device.

### Hardware used
* [NTSC display](https://www.adafruit.com/product/911)
* [6v Voltage regulator](https://www.amazon.com/Converter-DROK-Regulator-Waterproof-Efficiency/dp/B00CGQRIFG/) for display
* [Raspberry Pi 4 Model B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
* [Raspberry Pi UPS HAT](https://www.pishop.us/product/raspberry-pi-ups-hat/)
* [PiCAN3 CAN Bus Board](https://copperhilltech.com/pican3-can-bus-board-for-raspberry-pi-4-with-3a-smps-and-rtc/)
* [Alpine HCE-C1100 camera](https://www.crutchfield.com/p_500HCEC110/Alpine-HCE-C1100.html)
* [Audiovox ACA800 camera](https://www.crutchfield.com/p_220ACA800/Audiovox-ACA800.html)
* [BOYO VTSW4](https://visiontechamerica.com/products/vtsw4-4-channel-video-switcher) video switcher
* 2x [BOSS Audio Systems BVAM5](https://bossaudio.com/product/bvam5/) Video Signal Amplifier
* [EchoMaster DVR-20M](https://catalog.echomaster.com/catalog/dash-cams-dvrs/dvr-20m) 2 channel DVR

### Software used
* [Raspberry Pi OS (32-bit) Lite](https://www.raspberrypi.org/downloads/raspberry-pi-os/)
* [FIM](https://www.nongnu.org/fbi-improved/) image viewer
* [SQLite](https://www.sqlite.org/index.html) 

### Raspberry Pi GPIO
| GPIO Pin | Usage                      |
|----------|----------------------------|
|4         |PiCAN LED                   |
|16        |Video splitter output #4    |
|17        |UPS check for power failure |
|18        |UPS check for shutdown      |
|20        |Video splitter output #3    |
|21        |Video splitter output #2    |
|25        |PiCAN Rx interrupt          |
|27        |UPS heartbeat toggle        |

# AutoCAN_Imaging

Process multiple automotive camera feeds to include with data logs while simultaneously displaying video to the driver.

### Principle of operation

The car will be equipped with a traditional aftermarket backup camera, plus an additional camera mounted on the front of the car. The signal from both cameras will be fed to the Raspberry Pi to collect as dashcam data. The Raspberry Pi will collect real time engine stats and sensor readings from MegaSquirt and AutoCAN_SensorHub via CAN bus. The video feeds and CAN bus readings will be combined into a unified data log. For example, it could be useful to see exactly how fast your car was going at the moment of impact in a rear-end collision.

A video switcher will send video to the dashboard. When the car is being driven normally, the display will show a static image from the Raspberry Pi. When the car is stopped or moving forward below 10mph, the display will show the forward camera (to assist with parking, etc). When the car is in reverse, the backup camera will be shown on the display.

### Hardware used
* [NTSC display](https://www.adafruit.com/product/911)
* [6v Voltage regulator](https://www.amazon.com/Converter-DROK-Regulator-Waterproof-Efficiency/dp/B00CGQRIFG/) for display
* [Raspberry Pi 4 Model B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
* [Raspberry Pi UPS HAT](https://www.pishop.us/product/raspberry-pi-ups-hat/)
* [PiCAN3 CAN Bus Board](https://copperhilltech.com/pican3-can-bus-board-for-raspberry-pi-4-with-3a-smps-and-rtc/)
* [Alpine HCE-C1100 camera](https://www.crutchfield.com/p_500HCEC110/Alpine-HCE-C1100.html)
* [Audiovox ACA800 camera](https://www.crutchfield.com/p_220ACA800/Audiovox-ACA800.html)
* [BOYO VTSW4](https://visiontechamerica.com/products/vtsw4-4-channel-video-switcher) video switcher
* 2x [REDGO](https://www.amazon.com/REDGO-Video-Capture-Converter-Adapter/dp/B01E5ITE2W) brand composite video to USB capture cards
* 2x [BOSS Audio Systems BVAM5](https://bossaudio.com/product/bvam5/) Video Signal Amplifier

### Software used
* [Raspberry Pi OS (32-bit) Lite](https://www.raspberrypi.org/downloads/raspberry-pi-os/)
* [FIM](https://www.nongnu.org/fbi-improved/) image viewer
* [OpenCV](https://opencv.org/) computer vision library (Python port)
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

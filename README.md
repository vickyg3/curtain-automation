## Smart Wifi Enabled Curtains

This projects provides instructions on how to build a smart wifi enabled system
for your existing rod based curtains.

The original blog post can be found here: http://vignesh.foamsnet.com/2018/06/v20-ok-google-open-my-curtains.html

#### Hardware Links

Item | Amazon | Ebay
---|---|---
Nema 17 stepper motor | [$13.99](https://goo.gl/zhExnz) | [$6.99](https://goo.gl/6VtwWh)
TB6600 stepper motor driver | [$13.20](https://goo.gl/Ug8veP) | [$9.96](https://goo.gl/ygEP1a)
Vibration dampener | [$11.45](https://goo.gl/t85HoR) | [$2.98](https://goo.gl/94HCxL)
Mounting bracket | [$6.50](https://goo.gl/nDU3Uv) | [$2.82](https://goo.gl/PP4awi)
Timing belt pulley kit | [$12.98](https://goo.gl/p9WV6L) | [$8.79](https://goo.gl/5bcmr7)
NodeMCU (ESP8266) microcontroller | [$5.98](https://goo.gl/k4mkt8) | [$5.80](https://goo.gl/fPnhYX)
12V DC power supply | [$7.77](https://goo.gl/vhGfyw) | [$8.99](https://goo.gl/m2cnQQ)
Total Cost | **$71.87** | **$46.33**

#### Programming the NodeMCU

The arduino sketch for the microcontroller that controls the curtain is found in [curtain_control.ino](curtain_control.ino). It can be compiled using the [Arduino IDE](https://www.arduino.cc/en/Main/Software).

#### Home Assistant

This repository contains a custom component for home assistant which exposes the
curtain as a `cover`.

Please see [home_assistant/README.md](home_assistant/README.md) for more instructions on how to use it.

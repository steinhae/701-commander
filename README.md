# Architecture
- Husqvarna 701 6 pin OBD -> 6 pin to standard OBD cable -> white panda -> USB to Raspberry Pi micro USB
- Raspberry Pi runs husq_reader.py to read CAN data via USB and panda
- Raspberry Pi hosts MQTT broker and nginx for the dashboard
- husq_reader.py -> publish sensor data to MQTT
- d3-car-dashboard subscribes to MQTT topics to display sensor data

# Hardware
- [comma ai white panda](https://comma.ai/shop/products/panda)
- [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
- [Motorcycle 6 Pin to OBD Diagnostic Cable](https://www.amazon.com/dp/B083JTR84L?psc=1&ref=ppx_yo2ov_dt_b_product_details)
- Device with wifi/web browser/display to show interface mounted to the bike
- Optional: [USB-A power outlet kit](https://www.husqvarna-motorcycles.com/en-hr/technical-accessories/lenker-instrumente-elektrik-1001563559/instrumente-elektrik-1001563596/usb-power-outlet-kit-1001463809.prod.html)

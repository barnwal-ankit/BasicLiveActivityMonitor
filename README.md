# BasicLiveActivityMonitor

## Overview
This project uses an ESP8266 microcontroller and an ADXL345 accelerometer to detect basic activities like running, standing, and sitting. The data is processed using Edge Impulse, and the activity status is displayed live on a website via serial data.

## Components
- ESP8266: Handles processing and communication.
- ADXL345: A 3-axis accelerometer used for detecting motion.
- Edge Impulse: For training and running the activity detection model.
- Website: Displays real-time activity data.

## Features
- Detects 4 activities (running, standing, sitting, and one additional activity).
- Live data visualization on a website.
- Anomaly detection to flag unexpected movements.

## Setup
1. Connect the ADXL345 accelerometer to the ESP8266.
2. Upload the firmware to the ESP8266.
3. Ensure the Edge Impulse model is properly trained and integrated.
4. Visit the live website to see the activity status updated in real-time.

## Datasheet
https://www.analog.com/media/en/technical-documentation/data-sheets/ADXL345.pdf - Provides detailed specifications and pinout of the ADXL345 sensor.\n
https://www.espressif.com/sites/default/files/documentation/0a-esp8266ex_datasheet_en.pdf - Provides detailed specifications of ESP8266.

## DataSet
RealWorld (HAR) (2016) url: https://www.uni-mannheim.de/dws/research/projects/activity-recognition/dataset/dataset-realworld/ \n
Here only Forearm Dataset has been used.

## License
This project is open-source under the MIT license.

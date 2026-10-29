# Smart Drone for Crop Monitoring

An open-source software scaffold for agricultural crop-monitoring drones. This repository includes multispectral NDVI analysis, survey mission waypoint planning, telemetry and LiPo battery monitoring with automated return-to-home (RTH) failsafes, and sample flight log data.

All tools are implemented in Python using the standard library without external dependencies.

---

## Repository Structure

```text
drone_for_crops/
├── README.md                  # Project overview and usage guide
├── ndvi/
│   └── ndvi.py                # NDVI calculation and vegetation health classification
├── mission/
│   └── waypoints.py           # Lawnmower flight survey path generator
├── telemetry/
│   └── battery_monitor.py     # 3S LiPo ADC voltage divider reader & RTH failsafe monitor
└── data/
    └── sample_flight_log.csv  # 12-row sample telemetry and NDVI mission flight log
```

---

## Modules & Features

### 1. NDVI Calculation & Classification (`ndvi/ndvi.py`)
- Calculates the Normalized Difference Vegetation Index: `NDVI = (NIR - Red) / (NIR + Red)`.
- Handles zero-division edge cases safely.
- Classifies vegetation condition:
  - `NDVI < 0.2`: **Stressed**
  - `0.2 <= NDVI < 0.5`: **Moderate**
  - `NDVI >= 0.5`: **Healthy**
- Includes a self-contained demonstration on a 3x3 pixel grid.

### 2. Survey Waypoint Planning (`mission/waypoints.py`)
- Generates a lawnmower (boustrophedon) path covering a 100x100 m crop field at 20 m altitude.
- Configured for camera HFOV of 73.7° and 70% side overlap.
- Automatically determines track spacing, swath width, and sequential waypoint coordinates.

### 3. Battery Monitor & Failsafe (`telemetry/battery_monitor.py`)
- Simulates reading a 3S LiPo pack via a voltage divider into a 12-bit ADC (3.3 V reference, R1 = 30 kΩ, R2 = 7.5 kΩ, ratio = 5.0).
- Maps pack voltage (~9.0 V empty to 12.6 V full) to percentage (0–100%).
- Implements a Return-to-Home (RTH) failsafe flag triggered when battery drops below 20%.

### 4. Sample Flight Log (`data/sample_flight_log.csv`)
- 12 rows of simulated flight telemetry containing timestamps, GPS coordinates (latitude/longitude), altitude (m), ground speed (m/s), battery percentage, and mean NDVI readings.

---

## How to Run Each Script

Run the scripts directly using standard Python 3:

### Run the NDVI Processor
```bash
python3 ndvi/ndvi.py
```

### Run the Survey Path Generator
```bash
python3 mission/waypoints.py
```

### Run the Telemetry Battery Monitor
```bash
python3 telemetry/battery_monitor.py
```

### Inspect Flight Log Data
```bash
# View the sample flight log
head -n 15 data/sample_flight_log.csv
```

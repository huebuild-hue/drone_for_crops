"""
Telemetry Battery Monitor for 3S LiPo.

Hardware characteristics:
- ADC: 12-bit (0-4095 counts)
- V_ref: 3.3 V
- Voltage divider: R1 = 30k Ohm, R2 = 7.5k Ohm
- Battery: 3S LiPo (~9.0 V empty to 12.6 V fully charged)
- Failsafe: Return-to-Home (RTH) triggered when battery < 20%
"""

# Circuit parameters
R1 = 30000.0  # Ohms (top resistor connected to battery positive)
R2 = 7500.0   # Ohms (bottom resistor connected to ground)
V_REF = 3.3   # Volts (ADC reference voltage)
ADC_MAX = 4095  # 12-bit ADC (2^12 - 1)

# Voltage divider ratio: V_adc = V_in * (R2 / (R1 + R2))
# Therefore: V_in = V_adc * (R1 + R2) / R2
DIVIDER_RATIO = (R1 + R2) / R2  # (30000 + 7500) / 7500 = 5.0

# 3S LiPo parameters (3 cells in series)
CELL_MIN_V = 3.0   # Volts per cell (0% capacity threshold)
CELL_MAX_V = 4.2   # Volts per cell (100% capacity threshold)
LIPO_MIN_V = 3 * CELL_MIN_V  # 9.0 V
LIPO_MAX_V = 3 * CELL_MAX_V  # 12.6 V
RTH_THRESHOLD_PCT = 20.0     # Return-to-home trigger threshold (%)


def adc_to_voltage(adc_raw):
    """
    Convert raw 12-bit ADC reading to the actual 3S battery pack voltage.
    """
    # Clamping raw ADC reading to valid 12-bit range
    adc_clamped = max(0, min(ADC_MAX, adc_raw))
    v_adc = (adc_clamped / ADC_MAX) * V_REF
    pack_voltage = v_adc * DIVIDER_RATIO
    return round(pack_voltage, 2)


def voltage_to_percentage(pack_voltage):
    """
    Map battery voltage to remaining capacity percentage (0 - 100%).
    """
    if pack_voltage <= LIPO_MIN_V:
        return 0.0
    if pack_voltage >= LIPO_MAX_V:
        return 100.0
    pct = ((pack_voltage - LIPO_MIN_V) / (LIPO_MAX_V - LIPO_MIN_V)) * 100.0
    return round(pct, 1)


def check_failsafe(battery_pct):
    """
    Check if battery level requires Return-To-Home (RTH).
    """
    return battery_pct < RTH_THRESHOLD_PCT


def evaluate_telemetry(adc_raw):
    """
    Evaluate telemetry from ADC raw reading and report status.
    """
    voltage = adc_to_voltage(adc_raw)
    pct = voltage_to_percentage(voltage)
    rth = check_failsafe(pct)
    return {
        "adc_raw": adc_raw,
        "voltage_v": voltage,
        "battery_pct": pct,
        "rth_triggered": rth,
    }


def main():
    print("=== 3S LiPo Telemetry & Battery Monitor ===")
    print(f"ADC: 12-bit (0-{ADC_MAX}), Vref: {V_REF}V, Divider: R1={R1/1000}k, R2={R2/1000}k (ratio: {DIVIDER_RATIO})")
    print(f"3S Voltage Range: {LIPO_MIN_V}V (0%) - {LIPO_MAX_V}V (100%), RTH Failsafe: < {RTH_THRESHOLD_PCT}%")
    print("-" * 60)
    print(f"{'ADC Raw':<10} | {'Voltage (V)':<12} | {'Battery (%)':<12} | {'Status':<15}")
    print("-" * 60)

    # Test samples ranging from fully charged to critical low
    sample_adcs = [3128, 2900, 2600, 2410, 2300, 2100]
    for adc in sample_adcs:
        telem = evaluate_telemetry(adc)
        status = "FAILSAFE: RTH!" if telem["rth_triggered"] else "NORMAL"
        print(f"{telem['adc_raw']:<10} | {telem['voltage_v']:<12.2f} | {telem['battery_pct']:<12.1f} | {status:<15}")


if __name__ == "__main__":
    main()

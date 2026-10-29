"""
Lawnmower survey flight path generator for crop monitoring.
Calculates path over a 100x100 m field at 20 m altitude with 70% side overlap,
using a camera horizontal field of view (HFOV) of 73.7 degrees.
"""

import math


def calculate_footprint_width(altitude_m, hfov_deg):
    """
    Calculate camera ground footprint width in meters.
    width = 2 * altitude * tan(HFOV / 2)
    """
    hfov_rad = math.radians(hfov_deg)
    return 2.0 * altitude_m * math.tan(hfov_rad / 2.0)


def calculate_track_spacing(footprint_width_m, side_overlap_ratio):
    """
    Calculate distance between adjacent flight tracks based on side overlap.
    spacing = footprint_width * (1 - overlap)
    """
    return footprint_width_m * (1.0 - side_overlap_ratio)


def generate_lawnmower_waypoints(field_width_m=100.0, field_length_m=100.0,
                                altitude_m=20.0, hfov_deg=73.7,
                                side_overlap_ratio=0.70):
    """
    Generate a lawnmower (boustrophedon) waypoint list covering the field.
    Coordinates are in local frame (x_m east, y_m north, z_m altitude up).
    """
    footprint_w = calculate_footprint_width(altitude_m, hfov_deg)
    spacing = calculate_track_spacing(footprint_w, side_overlap_ratio)

    # Generate track x positions across the field width
    x_coords = []
    curr_x = spacing / 2.0
    while curr_x < field_width_m:
        x_coords.append(curr_x)
        curr_x += spacing

    # Ensure the far edge is covered
    if not x_coords or x_coords[-1] < field_width_m - (spacing / 2.0):
        x_coords.append(field_width_m - (spacing / 2.0))

    waypoints = []
    direction_north = True

    for idx, x in enumerate(x_coords):
        if direction_north:
            waypoints.append((x, 0.0, altitude_m))
            waypoints.append((x, field_length_m, altitude_m))
        else:
            waypoints.append((x, field_length_m, altitude_m))
            waypoints.append((x, 0.0, altitude_m))
        direction_north = not direction_north

    return waypoints, footprint_w, spacing


def print_waypoints(waypoints, footprint_w, spacing):
    print(f"Ground Footprint Width: {footprint_w:.2f} m")
    print(f"Track Spacing (70% overlap): {spacing:.2f} m")
    print(f"Total Waypoints Generated: {len(waypoints)}\n")
    print(f"{'Waypoint':<10} | {'X (m)':<10} | {'Y (m)':<10} | {'Alt (m)':<10}")
    print("-" * 46)
    for i, (x, y, z) in enumerate(waypoints, start=1):
        print(f"{i:<10} | {x:<10.2f} | {y:<10.2f} | {z:<10.2f}")


if __name__ == "__main__":
    print("--- Crop Survey Lawnmower Waypoints ---")
    wps, fp_w, trk_sp = generate_lawnmower_waypoints(
        field_width_m=100.0,
        field_length_m=100.0,
        altitude_m=20.0,
        hfov_deg=73.7,
        side_overlap_ratio=0.70
    )
    print_waypoints(wps, fp_w, trk_sp)

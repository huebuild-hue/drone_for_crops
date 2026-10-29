"""
NDVI (Normalized Difference Vegetation Index) calculation and classification.
Standard library implementation operating on 2D grid/band data.
"""

def calculate_ndvi(nir_band, red_band):
    """
    Calculate NDVI matrix given NIR and Red 2D bands.
    NDVI = (NIR - Red) / (NIR + Red)
    Handles zero-division by returning 0.0 when (NIR + Red) == 0.
    """
    rows = len(nir_band)
    cols = len(nir_band[0]) if rows > 0 else 0
    ndvi_matrix = []

    for r in range(rows):
        ndvi_row = []
        for c in range(cols):
            nir = float(nir_band[r][c])
            red = float(red_band[r][c])
            denominator = nir + red
            if denominator == 0:
                ndvi_val = 0.0
            else:
                ndvi_val = (nir - red) / denominator
            ndvi_row.append(round(ndvi_val, 4))
        ndvi_matrix.append(ndvi_row)

    return ndvi_matrix


def classify_ndvi(value):
    """
    Classify a single NDVI value into vegetation health status:
      - Stressed: < 0.2
      - Moderate: 0.2 <= value < 0.5
      - Healthy:  >= 0.5
    """
    if value < 0.2:
        return "Stressed"
    elif value < 0.5:
        return "Moderate"
    else:
        return "Healthy"


def classify_ndvi_grid(ndvi_matrix):
    """Classify every cell in a 2D NDVI grid."""
    return [[classify_ndvi(val) for val in row] for row in ndvi_matrix]


def main():
    # Tiny sample run on a 3x3 crop grid (reflectance / digital numbers)
    nir_sample = [
        [0.45, 0.60, 0.70],
        [0.25, 0.35, 0.65],
        [0.10, 0.20, 0.55],
    ]
    red_sample = [
        [0.10, 0.12, 0.10],
        [0.18, 0.20, 0.12],
        [0.22, 0.15, 0.10],
    ]

    print("--- NDVI Crop Monitoring Grid Run (3x3) ---")
    ndvi = calculate_ndvi(nir_sample, red_sample)
    classification = classify_ndvi_grid(ndvi)

    for r in range(len(ndvi)):
        for c in range(len(ndvi[0])):
            val = ndvi[r][c]
            status = classification[r][c]
            print(f"Cell ({r}, {c}): NDVI = {val:+.4f} -> {status}")


if __name__ == "__main__":
    main()

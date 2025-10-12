# utils/weather_estimator.py
import cv2
import numpy as np

def estimate_weather_and_time(image_path):
    """Estimate approximate weather and time of day from an image."""
    img = cv2.imread(image_path)
    if img is None:
        return {"time_of_day": "Unknown", "weather": "Unknown"}

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    brightness = np.mean(hsv[:, :, 2])
    sky_region = hsv[: img.shape[0] // 3, :, :]  # top third = sky
    avg_hue = np.mean(sky_region[:, :, 0])
    avg_sat = np.mean(sky_region[:, :, 1])

    # Time of day by brightness
    if brightness < 60:
        time = "Night"
    elif brightness < 150:
        time = "Evening / Dusk"
    else:
        time = "Day"

    # Weather by color tone
    if avg_sat < 40:
        weather = "Cloudy / Overcast"
    elif avg_hue < 20:
        weather = "Sunset / Warm light"
    else:
        weather = "Clear sky"

    return {"time_of_day": time, "weather": weather}

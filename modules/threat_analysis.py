# modules/threat_analysis.py
import os
import re

def run_threat_scan(image_path):
    """Detect embedded files, steganography traces, or watermark-like regions."""
    result = {
        "embedded_files": [],
        "possible_steg": False,
        "visible_watermark": False,
    }

    try:
        with open(image_path, "rb") as f:
            data = f.read()

        # Detect hidden ZIP or JPG inside
        if b"PK\x03\x04" in data:
            result["embedded_files"].append("ZIP archive detected")
        if b"\xFF\xD8\xFF" in data[100:]:  # JPG inside JPG
            result["embedded_files"].append("Nested JPG detected")

        # Watermark detection (simple heuristic)
        import cv2
        import numpy as np

        img = cv2.imread(image_path, 0)
        edges = cv2.Canny(img, 50, 150)
        ratio = (edges > 0).mean()
        if ratio < 0.005:
            result["visible_watermark"] = False
        elif ratio > 0.05:
            result["visible_watermark"] = True

        # Steganography heuristic
        if re.search(rb"\x00{3,}", data):
            result["possible_steg"] = True

    except Exception as e:
        result["error"] = str(e)

    return result

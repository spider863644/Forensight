# modules/report_summary.py
import json

def summarize_report(report: dict) -> str:
    """Generate a short, human-readable summary of the analysis."""
    try:
        faces = len(report.get("face_boxes", []))
        objs = len(report.get("objects", []))
        weather = report.get("weather_estimation", {}).get("weather", "Unknown")
        time_of_day = report.get("weather_estimation", {}).get("time_of_day", "Unknown")
        scene_guess = report.get("scene_estimation", {}).get("guess", "Unknown")
        threats = report.get("threat_analysis", {}).get("embedded_files", [])
        text = report.get("ocr_text", "").strip()[:80]

        summary = (
            f"The image likely depicts a scene around {scene_guess}. "
            f"Time appears to be {time_of_day.lower()} with {weather.lower()} conditions. "
            f"Detected {objs} objects and {faces} faces. "
            + (f"Found potential hidden data: {', '.join(threats)}. " if threats else "")
            + (f"OCR text snippet: '{text}'." if text else "No visible text detected.")
        )
        return summary

    except Exception as e:
        return f"Summary generation failed: {e}"

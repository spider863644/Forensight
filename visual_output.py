# visual_output.py
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_visual_output_dir(base_dir: str) -> str:
    visual_dir = os.path.join(base_dir, "visuals")
    os.makedirs(visual_dir, exist_ok=True)
    return visual_dir

def save_annotated_image(image_path: str, detections: list, face_boxes: list, ocr_lines: list = None, out_path: str = None):
    """
    Draws object boxes, face boxes, and optional OCR text on image.
    Saves to out_path.
    """
    img = cv2.imread(image_path)

    # 🩻 Fallback for AVIF and unsupported formats
    if img is None:
        try:
            from PIL import Image
            pil_img = Image.open(image_path).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            print(f"[INFO] Loaded AVIF image via PIL: {image_path}")
        except Exception as e:
            print(f"[ERROR] Cannot read image: {image_path} — {e}")
            return None

    # Draw object boxes
    for det in detections:
        x1, y1, x2, y2 = map(int, det['bbox'])
        label = det.get('label', 'object')
        conf = det.get('confidence', 0)
        color = (0, 255, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, f"{label} {conf:.2f}", (x1, max(y1 - 5, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Draw face boxes
    for (left, top, right, bottom) in face_boxes:
        color = (255, 0, 0)
        cv2.rectangle(img, (left, top), (right, bottom), color, 2)

    # Optional: overlay OCR text at top-left
    if ocr_lines:
        y_offset = 20
        for ln in ocr_lines[:5]:
            cv2.putText(img, ln, (5, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            y_offset += 20

    # Save annotated image
    if out_path is None:
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        out_path = os.path.join(os.path.dirname(image_path), f"annotated_{base_name}.jpg")

    ok = cv2.imwrite(out_path, img)
    if not ok:
        print(f"[ERROR] cv2 failed to write annotated image to {out_path}")
    else:
        print(f"[OK] Annotated image saved: {out_path}")

    return out_path


def save_color_swatch(colors: list, out_path: str, width: int = 300, height: int = 50):
    """
    Create a horizontal swatch image showing dominant colors.
    """
    if not colors:
        return None
    n = len(colors)
    swatch = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(swatch)
    seg_width = width // n
    for i, col in enumerate(colors):
        draw.rectangle([i*seg_width, 0, (i+1)*seg_width, height], fill=col)
    swatch.save(out_path)
    return out_path

def generate_visuals(report: dict, out_dir: str):
    """
    Generates and saves all visual outputs for a given report.
    """
    visual_dir = create_visual_output_dir(out_dir)
    image_path = report["image_path"]
    detections = report.get("objects", [])
    face_boxes = report.get("face_boxes", [])
    ocr_text = report.get("ocr_text", "")
    ocr_lines = [ln.strip() for ln in ocr_text.splitlines() if ln.strip()]
    
    # Annotated image
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    annotated_path = os.path.join(visual_dir, f"annotated_{base_name}.jpg")

    save_annotated_image(image_path, detections, face_boxes, ocr_lines, annotated_path)
    
    # Dominant color swatch
    colors = report.get("dominant_colors", [])
    swatch_path = os.path.join(visual_dir, f"colors_{os.path.basename(image_path)}.jpg")
    save_color_swatch(colors, swatch_path)
    
    return {
        "annotated_image": annotated_path,
        "color_swatch": swatch_path
    }

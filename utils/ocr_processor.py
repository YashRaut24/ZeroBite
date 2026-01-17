import re
from datetime import datetime, timedelta
import pytesseract
from PIL import Image
import io
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_file):
    """
    Extract text from image using pytesseract (text-based OCR only).
    No computer vision or image classification.
    
    Args:
        image_file: File object from Flask upload
        
    Returns:
        dict with extracted_text and status
    """
    try:
        image = Image.open(image_file)
        extracted_text = pytesseract.image_to_string(image)
        
        if not extracted_text.strip():
            return {
                'success': False,
                'extracted_text': '',
                'error': 'No text found in image. Please ensure the label is clear and legible.'
            }
        
        return {
            'success': True,
            'extracted_text': extracted_text.strip(),
            'error': None
        }
    except Exception as e:
        return {
            'success': False,
            'extracted_text': '',
            'error': f'OCR processing failed: {str(e)}'
        }


def detect_expiry_date(text):
    """
    Detect expiry date from OCR-extracted text using pattern matching.
    
    Patterns searched:
    - DD/MM/YYYY
    - DD-MM-YYYY
    - MM/YYYY
    - Month Year
    
    Args:
        text: OCR extracted text
        
    Returns:
        dict with detected_date and confidence
    """
    text_lower = text.lower()
    
    # Keywords that indicate expiry information
    expiry_keywords = ['exp', 'expiry', 'best before', 'use before', 'best by', 'consume by']
    
    # Check if text contains expiry-related keywords
    has_expiry_keyword = any(keyword in text_lower for keyword in expiry_keywords)
    
    # Pattern: DD/MM/YYYY
    pattern_ddmmyyyy = r'\b(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})\b'
    matches = re.findall(pattern_ddmmyyyy, text)
    
    if matches:
        for day, month, year in matches:
            try:
                date_obj = datetime(int(year), int(month), int(day))
                return {
                    'detected_date': date_obj.strftime("%d/%m/%Y"),
                    'date_object': date_obj,
                    'confidence': 'high' if has_expiry_keyword else 'medium'
                }
            except ValueError:
                continue
    
    # Pattern: MM/YYYY (month and year only)
    pattern_mmyyyy = r'\b(\d{1,2})[/\-](\d{4})\b'
    matches = re.findall(pattern_mmyyyy, text)
    
    if matches:
        for month, year in matches:
            try:
                # Assume last day of month
                date_obj = datetime(int(year), int(month), 1) + timedelta(days=32)
                date_obj = date_obj.replace(day=1) - timedelta(days=1)
                return {
                    'detected_date': f"{date_obj.strftime('%m/%Y')} (end of month)",
                    'date_object': date_obj,
                    'confidence': 'medium' if has_expiry_keyword else 'low'
                }
            except ValueError:
                continue
    
    return {
        'detected_date': None,
        'date_object': None,
        'confidence': None
    }


def determine_food_status(expiry_date_obj):
    """
    Determine if food is safe, expiring soon, or expired.
    
    Args:
        expiry_date_obj: datetime object of expiry date
        
    Returns:
        dict with status and days_remaining
    """
    if not expiry_date_obj:
        return {
            'status': 'UNKNOWN',
            'status_badge': '❓',
            'color': 'gray',
            'days_remaining': None,
            'message': 'Expiry date not detected'
        }
    
    today = datetime.now()
    days_remaining = (expiry_date_obj - today).days
    
    if days_remaining < 0:
        return {
            'status': 'EXPIRED',
            'status_badge': '⚠️',
            'color': 'red',
            'days_remaining': days_remaining,
            'message': f'Expired {abs(days_remaining)} days ago'
        }
    elif days_remaining == 0:
        return {
            'status': 'EXPIRES TODAY',
            'status_badge': '🔴',
            'color': 'orange',
            'days_remaining': 0,
            'message': 'Expires today'
        }
    elif days_remaining <= 3:
        return {
            'status': 'EXPIRING SOON',
            'status_badge': '🟠',
            'color': 'orange',
            'days_remaining': days_remaining,
            'message': f'Expires in {days_remaining} day{"s" if days_remaining != 1 else ""}'
        }
    else:
        return {
            'status': 'SAFE',
            'status_badge': '✅',
            'color': 'green',
            'days_remaining': days_remaining,
            'message': f'Safe for {days_remaining} more days'
        }


def process_ocr_image(image_file):
    """
    Complete OCR pipeline:
    1. Extract text
    2. Detect expiry date
    3. Determine status
    
    Args:
        image_file: File object from Flask upload
        
    Returns:
        dict with all processing results
    """
    # Step 1: Extract text
    extraction = extract_text_from_image(image_file)
    
    if not extraction['success']:
        return {
            'success': False,
            'error': extraction['error'],
            'extracted_text': None,
            'detected_expiry': None,
            'food_status': None
        }
    
    extracted_text = extraction['extracted_text']
    
    # Step 2: Detect expiry date
    expiry_detection = detect_expiry_date(extracted_text)
    
    # Step 3: Determine status
    food_status = determine_food_status(expiry_detection['date_object'])
    
    return {
        'success': True,
        'error': None,
        'extracted_text': extracted_text,
        'detected_expiry': expiry_detection['detected_date'],
        'expiry_confidence': expiry_detection['confidence'],
        'food_status': food_status
    }

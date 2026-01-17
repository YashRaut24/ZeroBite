# ZeroBite - OCR Expiry Detection Setup

## Installation Steps

### 1. Install Tesseract OCR (System Level)

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install to: `C:\Program Files\Tesseract-OCR`

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Tesseract Path (if needed)

If Tesseract is not in default path, edit `utils/ocr_processor.py`:

```python
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 4. Run the Application

**Terminal 1: Start Ollama**
```bash
ollama serve
```

**Terminal 2: Start Flask Server**
```bash
python app.py
```

**Terminal 3: Open Browser**
```
http://localhost:5000
```

## Features

✅ **OCR Expiry Detection:**
- Upload food label image
- Extract text using pytesseract
- Parse expiry date from text
- Determine food status (Safe / Expiring Soon / Expired)
- Get AI recommendation from Ollama

✅ **Text-Based Only:**
- No computer vision
- No image classification
- Pure text extraction and pattern matching

✅ **AI Integration:**
- Ollama provides reasoning over extracted text
- Safety-focused recommendations
- Waste reduction suggestions

## How It Works

1. **Upload Image** → Drag or click to select food label
2. **Extract Text** → OCR reads text from image
3. **Parse Dates** → Pattern matching finds expiry dates
4. **Determine Status** → Compare with current date
5. **AI Analysis** → Ollama provides recommendations

## Supported Date Formats

- DD/MM/YYYY (e.g., 25/12/2024)
- DD-MM-YYYY (e.g., 25-12-2024)
- MM/YYYY (e.g., 12/2024)

## Output Display

- ✅ Detected expiry date
- 🟢 Food status (Safe / Expiring Soon / Expired)
- 💡 AI recommendation
- 📄 Extracted text (expandable)

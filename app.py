from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from agents.planner_agent import planner_agent
from agents.expiry_agent import expiry_agent
from agents.recipe_agent import recipe_agent
from agents.audit_agent import audit_agent
from agents.final_agent import final_agent
from agents.ocr_expiry_agent import ocr_expiry_agent
from utils.ocr_processor import process_ocr_image
from utils.ollama_client import ask_ollama
import os
# import pytesseract
# from PIL import Image
# import re
# from datetime import datetime
# from ocr_agent import ocr_expiry_agent


app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    try:
        data = request.json
        ingredients = data.get('ingredients', [])
        expiring = data.get('expiring', [])
        dietary_preference = data.get('dietary_preference', 'both')
        
        if not ingredients or not expiring:
            return jsonify({'error': 'Please provide both ingredients and expiring items'}), 400
        
        # Optimized single agent approach for faster response
        from langchain_ollama import OllamaLLM
        llm = OllamaLLM(model="mistral", base_url="http://localhost:11434")

        dietary_rules = {
            'veg': 'STRICTLY VEGETARIAN - No meat, chicken, fish, eggs, or animal products',
            'non-veg': 'CAN INCLUDE meat, chicken, fish, eggs, and animal products',
            'both': 'FLEXIBLE - vegetarian or non-vegetarian recipes'
        }

        combined_prompt = f"""You are a food waste reduction expert. Provide a complete meal plan in one response.

DIETARY RULE: {dietary_rules.get(dietary_preference, dietary_rules['both'])}

Available ingredients: {ingredients}
Expiring soon: {expiring}

Provide:

PLANNING STRATEGY:
- Problem with expiring items
- Goal for waste reduction
- Key priorities

EXPIRY ANALYSIS:
- Which items to use first
- How to use them in cooking

MEAL PLAN (4-5 simple meals):
- Use expiring items first
- Follow dietary rule strictly
- Realistic recipes

WASTE AUDIT:
- Missing essential items
- Shopping recommendations

Keep each section brief and practical."""

        result = llm.invoke(combined_prompt)

        # Parse the combined response into sections
        sections = result.split('\n\n')
        plan = sections[0] if len(sections) > 0 else "Planning strategy generated"
        expiry_analysis = sections[1] if len(sections) > 1 else "Expiry analysis completed"
        meals = sections[2] if len(sections) > 2 else "Meal plan generated"
        audit = sections[3] if len(sections) > 3 else "Waste audit completed"
        final_output = sections[4] if len(sections) > 4 else "Shopping list created"
        
        return jsonify({
            'success': True,
            'data': {
                'dietary_preference': dietary_preference,
                'plan': plan,
                'expiry': expiry_analysis,
                'meals': meals,
                'audit': audit,
                'final': final_output
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')

        if not message:
            return jsonify({'error': 'Please provide a message'}), 400

        # Get response from Ollama
        response = ask_ollama(message)

        return jsonify({
            'success': True,
            'response': response
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ocr-expiry', methods=['POST'])
def process_ocr_expiry():
    """
    Process uploaded image using OCR text extraction.
    Returns expiry information and AI recommendation.
    """
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Allowed file extensions
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
        file_ext = image_file.filename.split('.')[-1].lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Please upload jpg, png, or gif'}), 400
        
        # Process image with OCR
        ocr_result = process_ocr_image(image_file)
        
        if not ocr_result['success']:
            return jsonify({'error': ocr_result['error']}), 400
        
        # Get AI recommendation
        ai_recommendation = ocr_expiry_agent(
            ocr_result['extracted_text'],
            ocr_result['detected_expiry'],
            ocr_result['food_status']['status']
        )
        
        return jsonify({
            'success': True,
            'data': {
                'extracted_text': ocr_result['extracted_text'],
                'detected_expiry': ocr_result['detected_expiry'],
                'expiry_confidence': ocr_result['expiry_confidence'],
                'food_status': ocr_result['food_status'],
                'ai_recommendation': ai_recommendation
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

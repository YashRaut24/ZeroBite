# ZeroBite - Google Gemini API Setup Guide

## What You Need
- Google Account (free)
- This project folder

## Complete Setup Process

### 1. CREATE YOUR API KEY (2 minutes)

**Option A: Quick Free Tier (Recommended)**
```
1. Go to: https://aistudio.google.com/app/apikeys
2. Click "Create API Key"
3. Select "Create API key in new Google Cloud project"
4. Click "Create API key"
5. COPY the key immediately (it won't show again)
```

**Option B: Google Cloud Console (Advanced)**
```
1. Go to: https://console.cloud.google.com/
2. Create new project
3. Enable "Generative Language API"
4. Create API Key in Credentials section
5. Copy the key
```

---

### 2. ADD KEY TO YOUR PROJECT

**On Windows:**

1. Open your project folder:
   ```
   c:\Code\Agentic ai\OpenAI\ZeroBite\
   ```

2. Create a new file called `.env` (exactly this name)
   - Right-click → New File
   - Name it `.env`

3. Open `.env` in VS Code and add:
   ```
   GOOGLE_API_KEY=your_actual_key_here
   ```

4. Replace `your_actual_key_here` with your actual key (keep it on one line)

5. Save the file (Ctrl+S)

**Example:**
```
GOOGLE_API_KEY=AIzaSyD_X_Q_Z_6_Y_7_a_b_c_d_e_f_g_h_i_j_k_l
```

---

### 3. VERIFY IT WORKS

Run this command in PowerShell from your project folder:

```powershell
python verify_api_key.py
```

**Expected Output:**
```
✅ API Key found (length: 39 chars)
✅ LLM Connection: SUCCESS
✅ Embeddings: SUCCESS
✅ Vector Store: SUCCESS
✅ ALL CHECKS PASSED - System is ready to use!
```

---

## Important Security Notes

### ⚠️ NEVER Commit Your API Key

Add to `.gitignore`:
```
.env
```

Check your `.gitignore` file exists in the root folder with `.env` listed.

### 🔒 Key Safety
- ✅ Store only in `.env` file
- ✅ Load with `python-dotenv`
- ✅ Add `.env` to `.gitignore`
- ❌ Never paste in code
- ❌ Never commit to GitHub
- ❌ Never share with others

---

## Troubleshooting

### Error: "GOOGLE_API_KEY not found"
- Solution: Create `.env` file with your key
- Check file is named exactly `.env` (not `.env.txt`)

### Error: "Invalid API key"
- Solution: Double-check you copied the full key correctly
- Solution: Regenerate key from https://aistudio.google.com/app/apikeys

### Error: "API key has exceeded quota"
- Free tier has rate limits
- Wait a moment and retry
- Upgrade to paid plan if needed

### Error: "Authentication failed"
- Solution: Make sure `load_dotenv()` is called in main.py (already done)
- Solution: Restart Python/Terminal after adding .env

---

## Components Using Your API Key

Your key powers all these:

1. **Expiry Agent** - Analyzes expiring ingredients
   - Uses: Gemini 1.5 Flash LLM

2. **Meal Agent** - Creates meal plans
   - Uses: Gemini 1.5 Flash LLM

3. **Audit Agent** - Validates meal plans
   - Uses: Gemini 1.5 Flash LLM

4. **Vector Store** - Searches recipes
   - Uses: Google Embeddings API

---

## Free Tier Limits

- **Request rate**: 15 requests per minute
- **Monthly quota**: 1.5 million requests
- **Tokens**: Generous daily limits
- Sufficient for development & testing

Upgrade to paid if you need higher limits.

---

## Testing Your Setup

After verification passes, test the full API:

```powershell
python -m uvicorn app.main:app --reload
```

Then visit: http://localhost:8000/docs

Try the `/plan` endpoint with sample data!

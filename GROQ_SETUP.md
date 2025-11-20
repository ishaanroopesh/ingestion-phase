# Groq API Setup Guide

This application now uses **Groq API** instead of Ollama for LLM inference. Groq provides fast, cloud-based inference with the `meta-llama/llama-4-maverick-17b-128e-instruct` model.

## Prerequisites

1. Python 3.8 or higher
2. A Groq API account (free tier available)
3. Internet connection (Groq is a cloud service)

## Step 1: Get Your Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account (or log in if you already have one)
3. Navigate to **API Keys** section: https://console.groq.com/keys
4. Click **"Create API Key"**
5. Copy your API key (you'll only see it once, so save it securely)

## Step 2: Set Up Environment Variables

### Option A: Using .env file (Recommended for Development)

1. Create a `.env` file in the `ingestion-phase` directory:

```bash
# Windows (PowerShell)
cd ingestion-phase
New-Item -Path .env -ItemType File

# Linux/Mac
cd ingestion-phase
touch .env
```

2. Add your API key to the `.env` file:

```env
GROQ_API_KEY=your_actual_api_key_here
```

**Important:** Never commit the `.env` file to git! It's already in `.gitignore`.

### Option B: Using System Environment Variables (Recommended for Production)

#### Windows (PowerShell):
```powershell
$env:GROQ_API_KEY="your_actual_api_key_here"
```

#### Windows (Command Prompt):
```cmd
set GROQ_API_KEY=your_actual_api_key_here
```

#### Linux/Mac:
```bash
export GROQ_API_KEY="your_actual_api_key_here"
```

To make it permanent, add to your `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export GROQ_API_KEY="your_actual_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

## Step 3: Install Dependencies

```bash
cd ingestion-phase
pip install -r requirements.txt
```

This will install:
- `groq>=0.4.0` - Groq API client
- `python-dotenv>=1.0.0` - For loading .env files
- All other required dependencies

## Step 4: Verify Setup

### Test API Key

You can test your API key by running:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key set: {bool(api_key)}")
print(f"API Key length: {len(api_key) if api_key else 0}")
```

### Start the Application

1. **Start FastAPI Backend:**
```bash
python start_api.py
```

2. **Start Streamlit Frontend (in another terminal):**
```bash
streamlit run app.py
```

3. **Check Health Endpoint:**
Visit: http://localhost:8000/health

You should see:
```json
{
  "status": "healthy",
  "groq": "connected",
  "groq_model": "meta-llama/llama-4-maverick-17b-128e-instruct",
  "api_key_set": true
}
```

## Configuration

The Groq API configuration is in `config.py`:

```python
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
```

You can change the model if needed, but `meta-llama/llama-4-maverick-17b-128e-instruct` is recommended for this application.

## Production Deployment

### Environment Variables for Production

For production deployments (Heroku, AWS, Docker, etc.), set the environment variable:

```bash
GROQ_API_KEY=your_production_api_key
```

### Docker Example

```dockerfile
ENV GROQ_API_KEY=your_api_key_here
```

### Heroku Example

```bash
heroku config:set GROQ_API_KEY=your_api_key_here
```

### AWS/EC2 Example

Add to your systemd service file or use AWS Systems Manager Parameter Store.

## Troubleshooting

### Error: "GROQ_API_KEY environment variable is not set"

**Solution:** Make sure you've set the environment variable:
- Check if `.env` file exists and contains `GROQ_API_KEY=...`
- Verify the variable is set: `echo $GROQ_API_KEY` (Linux/Mac) or `echo %GROQ_API_KEY%` (Windows)
- Restart your terminal/IDE after setting the variable

### Error: "Invalid Groq API key"

**Solution:**
- Verify your API key is correct at https://console.groq.com/keys
- Make sure there are no extra spaces or quotes around the key
- Regenerate the key if needed

### Error: "Groq API rate limit exceeded"

**Solution:**
- You've hit the rate limit for your tier
- Wait a few minutes and try again
- Consider upgrading your Groq plan for higher limits
- The code includes automatic retry logic with exponential backoff

### Error: "Request to Groq API timed out"

**Solution:**
- Check your internet connection
- The request might be too large - try reducing `max_tokens` in the request
- Groq API might be experiencing issues - check https://status.groq.com/

## Benefits of Groq API

1. **No Local Setup Required** - No need to install or run Ollama locally
2. **Fast Inference** - Groq's specialized hardware provides very fast responses
3. **Scalable** - Automatically scales with your usage
4. **Production Ready** - Built for production deployments
5. **Cost Effective** - Free tier available, pay-as-you-go pricing

## Migration from Ollama

If you were previously using Ollama:
- ✅ No code changes needed - the migration is complete
- ✅ Just set your `GROQ_API_KEY` environment variable
- ✅ Ollama is no longer required
- ✅ All features work the same way

## Support

- Groq Documentation: https://console.groq.com/docs
- Groq Community: https://groq.com/community/
- API Status: https://status.groq.com/


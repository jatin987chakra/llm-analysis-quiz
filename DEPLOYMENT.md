# Deployment Guide

This guide explains how to deploy the LLM Analysis Quiz project to various platforms.

## Prerequisites

- GitHub account with repository set up
- API keys configured (OpenAI)
- Student credentials (email and secret)

## Deployment Options

### 1. Heroku (Recommended)

**Steps:**

1. Install Heroku CLI:
   ```bash
   brew install heroku/brew/heroku  # macOS
   # or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. Login to Heroku:
   ```bash
   heroku login
   ```

3. Create a new app:
   ```bash
   heroku create your-app-name
   ```

4. Set environment variables:
   ```bash
   heroku config:set STUDENT_EMAIL="your@email.com"
   heroku config:set SECRET_KEY="your_secret"
   heroku config:set OPENAI_API_KEY="sk-..."
   heroku config:set OPENAI_MODEL="gpt-4o-mini"
   ```

5. Add buildpacks for Chrome/Selenium:
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome
   heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver
   ```

6. Deploy:
   ```bash
   git push heroku main
   ```

7. Your endpoint URL will be: `https://your-app-name.herokuapp.com/quiz`

### 2. Railway

**Steps:**

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `llm-analysis-quiz` repository
5. Add environment variables in the "Variables" tab:
   - `STUDENT_EMAIL`
   - `SECRET_KEY`
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL`
6. Railway will automatically detect the Python app and deploy it
7. Get your endpoint URL from the "Deployments" tab

### 3. Render

**Steps:**

1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click "New" → "Web Service"
4. Connect your `llm-analysis-quiz` repository
5. Configure:
   - **Name**: llm-analysis-quiz
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add environment variables:
   - `STUDENT_EMAIL`
   - `SECRET_KEY`
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL`
7. Click "Create Web Service"
8. Your endpoint URL will be: `https://your-app-name.onrender.com/quiz`

### 4. PythonAnywhere

**Steps:**

1. Create account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Go to "Web" tab → "Add a new web app"
3. Choose "Flask" and Python 3.10
4. Upload your files or clone from GitHub:
   ```bash
   git clone https://github.com/jatin987chakra/llm-analysis-quiz.git
   ```
5. Install requirements in bash console:
   ```bash
   cd llm-analysis-quiz
   pip install -r requirements.txt
   ```
6. Configure WSGI file to point to your app
7. Set environment variables in WSGI configuration
8. Reload the web app
9. Your endpoint URL will be: `https://yourusername.pythonanywhere.com/quiz`

**Note**: PythonAnywhere free tier doesn't support Selenium. You may need a paid plan.

### 5. Google Cloud Run

**Steps:**

1. Install Google Cloud SDK
2. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   
   # Install Chrome dependencies
   RUN apt-get update && apt-get install -y \
       wget \
       gnupg \
       unzip \
       && rm -rf /var/lib/apt/lists/*
   
   # Install Chrome
   RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
       && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
       && apt-get update \
       && apt-get install -y google-chrome-stable \
       && rm -rf /var/lib/apt/lists/*
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   
   CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
   ```

3. Build and deploy:
   ```bash
   gcloud run deploy llm-analysis-quiz \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. Set environment variables in Cloud Run console

## Testing Your Deployment

After deployment, test your endpoint:

```bash
python test_endpoint.py
# Enter your deployed URL when prompted
```

Or use curl:

```bash
curl -X POST https://your-endpoint.com/quiz \
  -H "Content-Type: application/json" \
  -d '{
    "email":"your@email.com",
    "secret":"your_secret",
    "url":"https://tds-llm-analysis.s-anand.net/demo"
  }'
```

## Monitoring

- Check application logs regularly
- Monitor response times (must be under 3 minutes)
- Test with the demo endpoint before submission

## Troubleshooting

### Chrome/Selenium Issues
- Ensure buildpacks are added correctly
- Check Chrome and ChromeDriver versions match
- Try headless mode: set `HEADLESS_BROWSER=True`

### Timeout Issues
- Increase worker timeout settings
- Optimize LLM calls (reduce max_tokens if needed)
- Use faster models for parsing tasks

### Memory Issues
- Use smaller models (gpt-4o-mini instead of gpt-4)
- Limit concurrent processing
- Clean up downloaded files after processing

## Cost Optimization

- Use `gpt-4o-mini` for most tasks (cheaper than gpt-4)
- Set reasonable `max_tokens` limits
- Cache results when possible
- Clean up temporary files regularly

## Security

- Never commit `.env` file
- Use environment variables for all secrets
- Validate all inputs
- Sanitize file paths to prevent directory traversal
- Set request timeouts to prevent resource exhaustion
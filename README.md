# LLM Analysis Quiz

An automated quiz solver that uses LLMs to solve data analysis tasks involving sourcing, preparation, analysis, and visualization.

## Project Overview

This project is built for the TDS course LLM Analysis Quiz assignment. It includes:
- A Flask API endpoint to receive quiz tasks
- Automated quiz solving using LLMs and web scraping
- System and user prompts for prompt injection testing
- Support for various data analysis tasks

## Features

- **API Endpoint**: Receives POST requests with quiz tasks
- **Web Scraping**: Handles JavaScript-rendered pages using Selenium
- **Data Processing**: Supports PDF, CSV, Excel, and various data formats
- **LLM Integration**: Uses OpenAI GPT models for problem-solving
- **Visualization**: Generates charts and graphs as required
- **Automatic Submission**: Submits answers within the 3-minute time limit

## Setup

1. Clone the repository:
```bash
git clone https://github.com/jatin987chakra/llm-analysis-quiz.git
cd llm-analysis-quiz
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```
SECRET_KEY=your_secret_string_here
STUDENT_EMAIL=your_email@example.com
OPENAI_API_KEY=your_openai_api_key
PORT=5000
```

5. Run the application:
```bash
python app.py
```

## API Endpoint

The endpoint accepts POST requests at `/quiz` with the following payload:

```json
{
  "email": "your email",
  "secret": "your secret",
  "url": "https://example.com/quiz-834"
}
```

## Deployment

For production deployment, you can use:
- **Heroku**: `git push heroku main`
- **Railway**: Connect your GitHub repo
- **Render**: Connect your GitHub repo
- **PythonAnywhere**: Upload files and configure WSGI

## Testing

Test your endpoint with:
```bash
curl -X POST https://your-endpoint.com/quiz \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","secret":"your_secret","url":"https://tds-llm-analysis.s-anand.net/demo"}'
```

## License

MIT License - see LICENSE file for details

## Author

Created for IIT Madras BS Data Science Program - TDS Course
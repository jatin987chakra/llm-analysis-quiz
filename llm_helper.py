import logging
import openai
import json

logger = logging.getLogger(__name__)

class LLMHelper:
    """Helper class for LLM interactions"""
    
    def __init__(self, config):
        self.config = config
        openai.api_key = config.OPENAI_API_KEY
        self.model = config.OPENAI_MODEL
    
    def get_completion(self, prompt, system_message=None, temperature=0.1):
        """Get completion from OpenAI"""
        try:
            messages = []
            
            if system_message:
                messages.append({
                    'role': 'system',
                    'content': system_message
                })
            else:
                messages.append({
                    'role': 'system',
                    'content': 'You are a helpful AI assistant that solves data analysis tasks accurately and concisely.'
                })
            
            messages.append({
                'role': 'user',
                'content': prompt
            })
            
            logger.info(f'Requesting completion from {self.model}')
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            logger.info(f'Received completion: {len(content)} characters')
            
            return content
            
        except Exception as e:
            logger.error(f'Error getting LLM completion: {str(e)}')
            return None
    
    def extract_json_from_text(self, text):
        """Extract JSON object from text"""
        try:
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return None
        except Exception as e:
            logger.error(f'Error extracting JSON: {str(e)}')
            return None
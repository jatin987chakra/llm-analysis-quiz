import logging
import time
import requests
import json
import traceback
from browser_handler import BrowserHandler
from data_processor import DataProcessor
from llm_helper import LLMHelper

logger = logging.getLogger(__name__)

class QuizSolver:
    """Main class for solving quiz tasks"""
    
    def __init__(self, config):
        self.config = config
        self.browser = BrowserHandler(config)
        self.data_processor = DataProcessor(config)
        self.llm = LLMHelper(config)
        self.start_time = None
        
    def solve_quiz_chain(self, url, email, secret):
        """Solve a chain of quiz questions"""
        self.start_time = time.time()
        current_url = url
        attempt_count = 0
        max_attempts = 10  # Prevent infinite loops
        
        while current_url and attempt_count < max_attempts:
            attempt_count += 1
            logger.info(f'Attempt {attempt_count}: Processing {current_url}')
            
            try:
                # Check if we're within time limit
                elapsed = time.time() - self.start_time
                if elapsed > self.config.MAX_QUIZ_TIME:
                    logger.warning(f'Time limit exceeded: {elapsed:.2f}s')
                    break
                
                # Solve the current quiz
                result = self.solve_single_quiz(current_url, email, secret)
                
                if result and 'url' in result:
                    current_url = result['url']
                    logger.info(f'Moving to next quiz: {current_url}')
                else:
                    logger.info('Quiz chain completed')
                    break
                    
            except Exception as e:
                logger.error(f'Error in quiz chain: {str(e)}')
                logger.error(traceback.format_exc())
                break
        
        self.browser.close()
        return {'completed': True, 'attempts': attempt_count}
    
    def solve_single_quiz(self, quiz_url, email, secret):
        """Solve a single quiz question"""
        try:
            # Step 1: Get the quiz content using browser
            logger.info(f'Fetching quiz from: {quiz_url}')
            quiz_content = self.browser.get_page_content(quiz_url)
            
            if not quiz_content:
                logger.error('Failed to fetch quiz content')
                return None
            
            logger.info(f'Quiz content retrieved: {quiz_content[:200]}...')
            
            # Step 2: Parse the quiz to extract task and submit URL
            task_info = self.parse_quiz_content(quiz_content)
            
            if not task_info:
                logger.error('Failed to parse quiz content')
                return None
            
            logger.info(f'Task: {task_info["task"]}')
            logger.info(f'Submit URL: {task_info["submit_url"]}')
            
            # Step 3: Solve the task using LLM and data processing
            answer = self.solve_task(task_info)
            
            if answer is None:
                logger.error('Failed to generate answer')
                return None
            
            logger.info(f'Generated answer: {answer}')
            
            # Step 4: Submit the answer
            result = self.submit_answer(
                task_info['submit_url'],
                email,
                secret,
                quiz_url,
                answer
            )
            
            return result
            
        except Exception as e:
            logger.error(f'Error solving quiz: {str(e)}')
            logger.error(traceback.format_exc())
            return None
    
    def parse_quiz_content(self, content):
        """Extract task description and submit URL from quiz content"""
        try:
            # Use LLM to parse the quiz content
            parse_prompt = f"""Extract the following information from this quiz content:
1. The main task/question being asked
2. The submit URL where the answer should be posted
3. Any file URLs that need to be downloaded
4. The expected answer format (boolean, number, string, base64, or JSON)

Quiz content:
{content}

Respond with a JSON object:
{{
    "task": "the main question",
    "submit_url": "the submit endpoint",
    "file_urls": ["url1", "url2"],
    "answer_format": "type of answer expected"
}}"""
            
            response = self.llm.get_completion(parse_prompt)
            
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
            if json_match:
                task_info = json.loads(json_match.group())
                return task_info
            
            logger.error('Could not parse quiz structure')
            return None
            
        except Exception as e:
            logger.error(f'Error parsing quiz: {str(e)}')
            return None
    
    def solve_task(self, task_info):
        """Solve the actual task using LLM and data processing"""
        try:
            task = task_info['task']
            file_urls = task_info.get('file_urls', [])
            answer_format = task_info.get('answer_format', 'string')
            
            # Download any required files
            downloaded_files = []
            for url in file_urls:
                file_path = self.data_processor.download_file(url)
                if file_path:
                    downloaded_files.append(file_path)
            
            # Process downloaded files
            processed_data = {}
            for file_path in downloaded_files:
                data = self.data_processor.process_file(file_path)
                if data:
                    processed_data[file_path] = data
            
            # Use LLM to solve the task
            solve_prompt = f"""Solve this data analysis task:

Task: {task}

Available data:
{json.dumps(processed_data, default=str, indent=2)}

Provide the answer in this format: {answer_format}
Respond with ONLY the answer value, nothing else."""
            
            answer = self.llm.get_completion(solve_prompt)
            
            # Convert answer to appropriate type
            answer = self.convert_answer(answer, answer_format)
            
            return answer
            
        except Exception as e:
            logger.error(f'Error solving task: {str(e)}')
            return None
    
    def convert_answer(self, answer, format_type):
        """Convert answer string to the appropriate type"""
        try:
            answer = answer.strip()
            
            if format_type == 'boolean':
                return answer.lower() in ['true', 'yes', '1']
            elif format_type == 'number':
                try:
                    return int(answer)
                except:
                    return float(answer)
            elif format_type == 'json':
                return json.loads(answer)
            else:
                return answer
                
        except Exception as e:
            logger.error(f'Error converting answer: {str(e)}')
            return answer
    
    def submit_answer(self, submit_url, email, secret, quiz_url, answer):
        """Submit the answer to the specified endpoint"""
        try:
            payload = {
                'email': email,
                'secret': secret,
                'url': quiz_url,
                'answer': answer
            }
            
            logger.info(f'Submitting to: {submit_url}')
            logger.info(f'Payload: {json.dumps(payload, indent=2)}')
            
            response = requests.post(
                submit_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            logger.info(f'Response status: {response.status_code}')
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f'Response: {json.dumps(result, indent=2)}')
                return result
            else:
                logger.error(f'Failed to submit: {response.text}')
                return None
                
        except Exception as e:
            logger.error(f'Error submitting answer: {str(e)}')
            return None
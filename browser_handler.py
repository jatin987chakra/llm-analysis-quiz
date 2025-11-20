import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

class BrowserHandler:
    """Handle browser automation using Selenium"""
    
    def __init__(self, config):
        self.config = config
        self.driver = None
        self._init_driver()
    
    def _init_driver(self):
        """Initialize Chrome WebDriver"""
        try:
            chrome_options = Options()
            
            if self.config.HEADLESS_BROWSER:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(self.config.BROWSER_TIMEOUT)
            
            logger.info('Browser initialized successfully')
            
        except Exception as e:
            logger.error(f'Failed to initialize browser: {str(e)}')
            raise
    
    def get_page_content(self, url):
        """Get rendered page content including JavaScript execution"""
        try:
            logger.info(f'Loading page: {url}')
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Wait for body to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            
            # Get the rendered HTML
            content = self.driver.find_element(By.TAG_NAME, 'body').text
            
            # Also get the full HTML if needed
            html = self.driver.page_source
            
            logger.info(f'Page content retrieved: {len(content)} chars')
            
            return content
            
        except Exception as e:
            logger.error(f'Error getting page content: {str(e)}')
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info('Browser closed')
            except Exception as e:
                logger.error(f'Error closing browser: {str(e)}')
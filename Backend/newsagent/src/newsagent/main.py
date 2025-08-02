#!/usr/bin/env python
import sys
import warnings
import schedule
import time
import threading
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from newsagent.crew import Newsagent

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('newsagent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def check_gemini_key():
    """Check if Google Gemini API key is configured"""
    gemini_key = os.getenv('GOOGLE_API_KEY')
    if not gemini_key or gemini_key == "your_google_gemini_api_key_here":
        logger.error("Google Gemini API key not configured!")
        logger.error("Please set GOOGLE_API_KEY in your .env file")
        logger.error("Get your API key from: https://makersuite.google.com/app/apikey")
        logger.error("")
        logger.error("Add this line to your .env file:")
        logger.error("GOOGLE_API_KEY=your_actual_api_key_here")
        return False
    return True

def run_newsletter_generation():
    """
    Run the newsletter generation crew.
    """
    try:
        logger.info("Starting newsletter generation...")
        
        # Check if Gemini key is configured
        if not check_gemini_key():
            raise Exception("Google Gemini API key not configured. Please add GOOGLE_API_KEY to your .env file.")
        
        # Categories to focus on - can be customized
        categories = [
            "technology", "business", "science", 
            "general", "health"
        ]
        
        inputs = {
            'categories': ', '.join(categories),
            'current_date': datetime.now().strftime('%Y-%m-%d'),
            'current_time': datetime.now().strftime('%H:%M:%S')
        }
        
        crew = Newsagent().crew()
        result = crew.kickoff(inputs=inputs)
        
        logger.info("Newsletter generation completed successfully!")
        return result
        
    except Exception as e:
        logger.error(f"An error occurred while running the crew: {e}")
        raise Exception(f"An error occurred while running the crew: {e}")

def run():
    """
    Run the crew once.
    """
    return run_newsletter_generation()

def run_scheduler():
    """
    Run the newsletter generation every minute using schedule.
    """
    logger.info("Starting newsletter scheduler...")
    logger.info("Newsletter will be generated every minute")
    logger.info("Press Ctrl+C to stop the scheduler")
    
    # Schedule the task to run every minute
    schedule.every(1).minutes.do(run_newsletter_generation)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")

def run_scheduler_daemon():
    """
    Run the newsletter generation in daemon mode (background).
    This can be used when integrated with Flask API.
    """
    logger.info("Starting newsletter scheduler in daemon mode...")
    logger.info("Newsletter will be generated every minute")
    
    # Schedule the task to run every minute
    schedule.every(1).minutes.do(run_newsletter_generation)
    
    def scheduler_loop():
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Scheduler daemon error: {e}")
                time.sleep(5)  # Wait before retrying
    
    scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
    scheduler_thread.start()
    logger.info("Newsletter scheduler daemon started in background")
    return scheduler_thread

def train():
    """
    Train the crew for a given number of iterations.
    """
    categories = ["technology", "business", "science"]
    inputs = {
        "categories": ', '.join(categories),
        'current_date': datetime.now().strftime('%Y-%m-%d')
    }
    try:
        Newsagent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Newsagent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    categories = ["technology", "business", "science"]
    inputs = {
        "categories": ', '.join(categories),
        "current_date": datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        Newsagent().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "schedule":
            run_scheduler()
        elif command == "run":
            run()
        elif command == "train":
            train()
        elif command == "replay":
            replay()
        elif command == "test":
            test()
        else:
            print("Available commands: run, schedule, train, replay, test")
    else:
        # Default to running once
        run()
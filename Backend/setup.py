#!/usr/bin/env python3
"""
Newsletter Backend Setup Script
This script helps set up the newsletter backend application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")

def activate_virtual_environment():
    """Get activation command for virtual environment"""
    if os.name == 'nt':  # Windows
        return "venv\\Scripts\\activate"
    else:  # Unix/Linux/macOS
        return "source venv/bin/activate"

def install_dependencies():
    """Install Python dependencies"""
    if os.name == 'nt':  # Windows
        pip_command = "venv\\Scripts\\pip install -r requirements.txt"
    else:  # Unix/Linux/macOS
        pip_command = "venv/bin/pip install -r requirements.txt"
    
    return run_command(pip_command, "Installing dependencies")

def setup_environment_file():
    """Setup .env file from .env.example"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from .env.example")
        print("🔧 Please edit .env file and add your API keys:")
        print("   - NEWS_API_KEY: Get from https://newsapi.org/")
        print("   - GNEWS_API_KEY: Get from https://gnews.io/")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    if os.name == 'nt':  # Windows
        python_command = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_command = "venv/bin/python"
    
    nltk_command = f'{python_command} -c "import nltk; nltk.download(\'punkt\'); nltk.download(\'stopwords\')"'
    return run_command(nltk_command, "Downloading NLTK data")

def test_installation():
    """Test if the installation is working"""
    if os.name == 'nt':  # Windows
        python_command = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_command = "venv/bin/python"
    
    test_command = f'{python_command} -c "import flask; import newspaper; import feedparser; print(\'All dependencies imported successfully\')"'
    return run_command(test_command, "Testing installation")

def main():
    """Main setup function"""
    print("🚀 Newsletter Backend Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    if not setup_environment_file():
        sys.exit(1)
    
    # Download NLTK data
    if not download_nltk_data():
        print("⚠️  NLTK data download failed, but continuing...")
    
    # Test installation
    if not test_installation():
        print("⚠️  Installation test failed, but setup is mostly complete")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit the .env file and add your API keys")
    print("2. Activate virtual environment:")
    print(f"   {activate_virtual_environment()}")
    print("3. Run the application:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\python Scraper.py")
    else:  # Unix/Linux/macOS
        print("   venv/bin/python Scraper.py")
    print("\n📖 API Documentation will be available at http://localhost:5000")

if __name__ == "__main__":
    main()

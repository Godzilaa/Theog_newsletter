"""
Deploy Newsletter App to Hugging Face Spaces
"""
from huggingface_hub import HfApi, create_repo
import os

def deploy_to_huggingface():
    """Deploy the app to Hugging Face Spaces"""
    
    # You'll need to set your Hugging Face token
    # Get it from: https://huggingface.co/settings/tokens
    hf_token = input("Enter your Hugging Face token (get it from https://huggingface.co/settings/tokens): ")
    
    if not hf_token:
        print("❌ Hugging Face token is required!")
        return
    
    # Repository details
    repo_name = input("Enter your desired repository name (e.g., 'newsletter-app'): ") or "newsletter-app"
    username = input("Enter your Hugging Face username: ")
    
    if not username:
        print("❌ Username is required!")
        return
    
    repo_id = f"{username}/{repo_name}"
    
    try:
        # Initialize the API
        api = HfApi(token=hf_token)
        
        # Create repository
        print(f"🚀 Creating repository: {repo_id}")
        try:
            create_repo(
                repo_id=repo_id,
                repo_type="space",
                space_sdk="gradio",
                token=hf_token,
                exist_ok=True
            )
            print("✅ Repository created successfully!")
        except Exception as e:
            print(f"Repository might already exist: {e}")
        
        # Upload files
        print("📤 Uploading files...")
        
        # Upload main app file
        api.upload_file(
            path_or_fileobj="app.py",
            path_in_repo="app.py",
            repo_id=repo_id,
            repo_type="space",
            token=hf_token
        )
        
        # Upload requirements
        api.upload_file(
            path_or_fileobj="requirements_hf.txt",
            path_in_repo="requirements.txt",
            repo_id=repo_id,
            repo_type="space",
            token=hf_token
        )
        
        # Upload README
        api.upload_file(
            path_or_fileobj="README.md",
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="space",
            token=hf_token
        )
        
        print("✅ Files uploaded successfully!")
        print(f"🌐 Your app will be available at: https://huggingface.co/spaces/{repo_id}")
        print("⏳ It may take a few minutes to build and deploy...")
        
        return f"https://huggingface.co/spaces/{repo_id}"
        
    except Exception as e:
        print(f"❌ Error during deployment: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Newsletter App - Hugging Face Deployment")
    print("=" * 50)
    deploy_to_huggingface()

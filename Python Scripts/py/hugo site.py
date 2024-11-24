import os
import subprocess
import shutil
import datetime
import yaml
import logging
import sys
import textwrap

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Comprehensive configuration with PaperMod-specific settings
CONFIG = {
    "site_name": "example-site",
    "site_subfolder": os.path.join("hugo site", "example site"),  # Subfolder under the user's home directory
    "theme": "PaperMod",
    "theme_repo": "https://github.com/adityatelange/hugo-PaperMod.git",
    "base_url": "https://examplesite.com/",
    "author": "Your Name",
    "site_title": "ExampleSite",
    "description": "ExampleSite description",
    "output_dir": "public",
    "google_analytics": "UA-123-45"
}

def run_command(command, cwd=None):
    """
    Run a shell command with proper Windows compatibility.
    """
    try:
        subprocess.run(command, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command: {' '.join(command)}")
        logging.error(f"Error details: {e}")
        sys.exit(1)

def check_hugo_installed():
    """
    Verify Hugo installation and print version.
    """
    if not shutil.which("hugo"):
        logging.error("Hugo is not installed!")
        logging.error("Please install Hugo from: https://gohugo.io/installation/")
        logging.error("Windows users can use: choco install hugo-extended")
        sys.exit(1)
    
    logging.info("Checking Hugo version...")
    run_command(["hugo", "version"])

def create_hugo_site(config):
    """
    Create a new Hugo site with specified configuration.
    """
    site_path = config["site_path"]
    if os.path.exists(site_path):
        logging.error(f"Directory {site_path} already exists. Please remove it or use a different name.")
        sys.exit(1)
    
    logging.info(f"Creating new Hugo site at: {site_path}")
    run_command(["hugo", "new", "site", site_path, "--format", "yaml"])

def setup_theme(config):
    """
    Initialize git and install PaperMod theme.
    """
    site_path = config["site_path"]
    
    logging.info("Initializing git repository...")
    run_command(["git", "init"], cwd=site_path)
    
    logging.info("Installing PaperMod theme...")
    run_command(["git", "submodule", "add", config["theme_repo"], f"themes/{config['theme']}"], cwd=site_path)

def create_config_yaml(config):
    """
    Create comprehensive Hugo configuration in YAML format.
    """
    hugo_config = {
        "baseURL": config["base_url"],
        "title": config["site_title"],
        "paginate": 5,
        "theme": config["theme"],
        "enableRobotsTXT": True,
        "buildDrafts": False,
        "buildFuture": False,
        "buildExpired": False,
        "googleAnalytics": config["google_analytics"],
        
        "minify": {
            "disableXML": True,
            "minifyOutput": True
        },
        
        "params": {
            "env": "production",
            "title": config["site_title"],
            "description": config["description"],
            "keywords": ["Blog", "Portfolio", "PaperMod"],
            "author": config["author"],
            "DateFormat": "January 2, 2006",
            "defaultTheme": "auto",
            "ShowReadingTime": True,
            "ShowShareButtons": True,
            "ShowPostNavLinks": True,
            "ShowBreadCrumbs": True,
            "ShowCodeCopyButtons": True,
            "ShowWordCount": True,
            "ShowRssButtonInSectionTermList": True,
            "UseHugoToc": True,
                
            "homeInfoParams": {
                "Title": "Welcome to ExampleSite",
                "Content": "A modern Hugo site using PaperMod theme"
            },
                
            "socialIcons": [
                {"name": "github", "url": "https://github.com/yourusername"},
                {"name": "twitter", "url": "https://twitter.com/yourusername"}
            ]
        },
        
        "menu": {
            "main": [
                {
                    "identifier": "archives",
                    "name": "Archives",
                    "url": "/archives/",
                    "weight": 10
                },
                {
                    "identifier": "categories",
                    "name": "Categories",
                    "url": "/categories/",
                    "weight": 20
                },
                {
                    "identifier": "tags",
                    "name": "Tags",
                    "url": "/tags/",
                    "weight": 30
                }
            ]
        }
    }
    
    config_path = os.path.join(config["site_path"], "hugo.yaml")
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(hugo_config, f, allow_unicode=True, sort_keys=False)

def create_content(config):
    """
    Create sample content with proper front matter.
    """
    content_dir = os.path.join(config["site_path"], "content")
    
    # Create posts directory and an example post
    posts_dir = os.path.join(content_dir, "posts")
    os.makedirs(posts_dir, exist_ok=True)
    
    # Example post
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    post_content = textwrap.dedent(f"""\
    ---
    title: "My First Post"
    date: {current_date}
    tags: ["first"]
    author: "{config['author']}"
    showToc: true
    TocOpen: false
    draft: false
    hidemeta: false
    comments: false
    description: "This is my first post on Hugo using PaperMod theme"
    canonicalURL: "https://canonical.url/to/page"
    disableShare: false
    disableHLJS: false
    hideSummary: false
    searchHidden: true
    ShowReadingTime: true
    ShowBreadCrumbs: true
    ShowPostNavLinks: true
    ShowWordCount: true
    ShowRssButtonInSectionTermList: true
    UseHugoToc: true
    ---
    
    ## Welcome to My Blog
    
    This is my first post using Hugo with the PaperMod theme. I hope you enjoy reading my content!
    
    ### Features of This Blog
    
    1. Clean and minimal design
    2. Dark/Light mode
    3. Mobile-friendly
    4. SEO optimized
    
    ### Code Example
    
    ```python
    def hello_world():
        print("Hello, Hugo!")
    ```
    
    Feel free to explore more posts!
    """)

    with open(os.path.join(posts_dir, "my-first-post.md"), "w", encoding="utf-8") as f:
        f.write(post_content)
    
    # Create archives page
    archives_content = textwrap.dedent("""\
    ---
    title: "Archives"
    layout: "archives"
    url: "/archives/"
    summary: archives
    ---
    """)
    os.makedirs(os.path.join(content_dir, "archives"), exist_ok=True)
    with open(os.path.join(content_dir, "archives", "_index.md"), "w", encoding="utf-8") as f:
        f.write(archives_content)

def generate_site(config):
    """
    Generate the static site.
    """
    logging.info("Generating static site...")
    run_command(["hugo"], cwd=config["site_path"])

def start_server(config):
    """
    Start the Hugo development server.
    """
    logging.info("\nStarting Hugo development server...")
    logging.info("Visit http://localhost:1313/ to view your site")
    logging.info("Press Ctrl+C to stop the server")
    run_command(["hugo", "server", "-D"], cwd=config["site_path"])

def main():
    """
    Main function to orchestrate Hugo site creation.
    """
    logging.info("Starting Hugo site generation...")
    
    # Determine the user's home directory in a cross-platform way
    home_dir = os.path.expanduser("~")
    
    # Construct the full site path
    CONFIG["site_path"] = os.path.join(home_dir, CONFIG["site_subfolder"])
    
    logging.info(f"Site will be created at: {CONFIG['site_path']}")
    
    # Ensure all prerequisites are met
    check_hugo_installed()
    
    # Create and set up the site
    create_hugo_site(CONFIG)
    setup_theme(CONFIG)
    create_config_yaml(CONFIG)
    create_content(CONFIG)
    generate_site(CONFIG)
    
    logging.info("\nSite created successfully!")
    logging.info(f"Site directory: {os.path.abspath(CONFIG['site_path'])}")
    
    # Start the development server
    start_server(CONFIG)

if __name__ == "__main__":
    main()

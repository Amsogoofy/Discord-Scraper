import os
import json
import sys
from internal.utils import show_header, check_config_file, get_account_settings, Logger
from internal.selfbot import client

logger = Logger()
CONFIG_FILE = "config.json"

def save_config(config_data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)

def interactive_menu():
    show_header()
    check_config_file()
    
    config = get_account_settings()
    
    if not config.get("token"):
        logger.error("No token found in config.json.")
        manual_token = input("[?] Please paste your Discord user token: ").strip()
        if manual_token:
            config["token"] = manual_token
            save_config(config)
            logger.success("Token saved successfully!")
        else:
            logger.error("A valid user token is required to run the scraper.")
            sys.exit(1)
    
    print(f"\n[+] Active Guild ID: {config.get('guild_id', 'Not Set')}")
    change_guild = input("[?] Do you want to change the Target Guild ID? (y/N): ").strip().lower()
    
    if change_guild == 'y':
        new_guild = input("[?] Enter new Guild ID: ").strip()
        if new_guild.isdigit():
            config["guild_id"] = int(new_guild)
            save_config(config)
            logger.success(f"Updated Guild ID to: {new_guild}")

    # Select Scraping Mode Menu
    print("\nSelect Scraping Mode:")
    print("  [1] Active Message Scraper (Scans recent & active chatters)")
    print("  [2] Complete Member Roster Scraper (Captures ALL current server members)")
    print("  [3] Historical Audit Log Scraper (Captures current + past/left members)")
    
    choice = input("\n[?] Enter your choice (1, 2, or 3, default 1): ").strip()
    
    if choice == "2":
        config["scrape_mode"] = "roster"
        logger.success("Mode set to: Complete Member Roster Scraper")
    elif choice == "3":
        config["scrape_mode"] = "historical"
        logger.success("Mode set to: Historical Audit Log Scraper")
    else:
        config["scrape_mode"] = "active"
        logger.success("Mode set to: Active Message Scraper")
        
    save_config(config)
    print("="*50 + "\n")

if __name__ == "__main__":
    interactive_menu()
    
    config = get_account_settings()
    token = config.get("token")
    
    logger.scraper("Launching Discord client session...")
    try:
        client.run(token)
    except Exception as e:
        logger.error(f"Client crashed: {e}")

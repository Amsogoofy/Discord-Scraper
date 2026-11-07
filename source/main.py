from internal.utils import show_header, check_config_file, get_account_settings, Logger
from rich import print
import json

show_header()
check_config_file()
log = Logger()
config = get_account_settings()

# Optional Terminal Prompts for Guild ID and Channel ID
print(f"[bold cyan]Current Config Guild ID:[/bold cyan] {config.get('guild_id', 0)}")
guild_input = input("Enter Guild (Server) ID [Press Enter to keep current]: ").strip()
if guild_input.isdigit():
    config["guild_id"] = int(guild_input)

print(f"[bold cyan]Current Config Channel ID:[/bold cyan] {config.get('channel_id', 0)}")
channel_input = input("Enter Channel ID [Press Enter to keep current]: ").strip()
if channel_input.isdigit():
    config["channel_id"] = int(channel_input)

# Save choices back to config.json
with open("config.json", "w") as f:
    json.dump(config, f, indent=2)

from internal.selfbot import client
client.run(config["token"]) # type: ignore
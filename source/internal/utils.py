from typing import Optional
from rich import print
from functools import cache

import json
import os
import string
import shutil
import re
import html
import csv

from discord import Guild, Member # type: ignore


header = """[bold white]
██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ███████║╚██████╗██║  ██║██║   ██║███████╗██║  ██║
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚══════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝╚══════╝╚═╝  ╚═╝
[/]"""
info = """[bold white]
[bold cyan]Discord Guild Members Scraper
[/]"""

default_data = {
  "token": "",
  "guild_id": 0,
  "pfp_format": "png",
  "purge_old_data": True,
  "download_pfp": False,
  "channel_id": 0
}


@cache
def show_header():
  print(f"{header}{info}")

@cache
def check_config_file():
  if not os.path.isfile("config.json"):
    json.dump(default_data, open("config.json", "w", encoding="utf-8"), indent=2)
    return

  with open("config.json", "r", encoding="utf-8") as file:
    file_data = json.loads(file.read())
  
  required_data = {}

  for key, value in file_data.items():
    if key in default_data.keys():
      required_data[key] = value

  for default_key, default_value in default_data.items():
    if default_key not in required_data.keys():
      required_data[default_key] = default_value

  json.dump(required_data, open("config.json", "w", encoding="utf-8"), indent=2)


class Logger():
  def __init__(self) -> None:
    ...

  def scraper(self, text: str) -> None:
    print(f"[bold white][Scraper] {text} [/]")

  def success(self, text: str) -> None:
    print(f"[bold green][Success] {text} [/]")

  def error(self, text: str) -> None:
    print(f"[bold red][Error] {text} [/]")

  def custom(self, text: str, header: Optional[str] = None, color: str = "white") -> None:
    print(f"[bold {color}][{header}] {text} [/]")

# NO @cache here so it reads fresh updates from disk
def get_account_settings():
  return json.load(open("config.json", "r", encoding="utf-8"))

@cache
def get_safe_guild_name(guild: Guild) -> str:
  return re.sub(r'[\\/*?:"<>|]', "", guild.name)

@cache
def create_guild_directory(guild: Guild):
  safe_name = get_safe_guild_name(guild)
  if get_account_settings()["purge_old_data"]:
    shutil.rmtree(f"data/{guild.id}", ignore_errors=True)
  os.makedirs(f"DataScraped/{safe_name}", exist_ok=True)

@cache
def clean_string(string_to_clean: str) -> str:
  return "".join([char for char in string_to_clean if char in string.printable])


def generate_master_exports(guild: Guild, members: list):
  safe_guild_name = get_safe_guild_name(guild)
  folder = f"DataScraped/{safe_guild_name}"
  os.makedirs(folder, exist_ok=True)

  # 1. Master CSV Export
  csv_file_path = f"{folder}/Scraped_Members.csv"
  fieldnames = ["User ID", "Username", "Discriminator", "Bot", "Avatar URL"]
  
  with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for member in members:
      safe_uname = clean_string(member.display_name)
      writer.writerow({
        "User ID": member.id,
        "Username": safe_uname,
        "Discriminator": f"#{member.discriminator}",
        "Bot": member.bot,
        "Avatar URL": str(member.avatar.url) if member.avatar else "None"
      })

  # 2. Master User IDs & Names SVG Document
  row_height = 30
  svg_height = max(150, 120 + len(members) * row_height)
  
  rows_text = ""
  for idx, member in enumerate(members):
    safe_uname = html.escape(clean_string(member.display_name))
    y_pos = 110 + (idx * row_height)
    bg_fill = "#2b2d31" if idx % 2 == 0 else "#1e1f22"
    rows_text += f'<rect x="30" y="{y_pos-20}" width="740" height="{row_height}" fill="{bg_fill}"/>\n'
    rows_text += f'<text x="50" y="{y_pos}" font-family="monospace" font-size="13" fill="#b5bac1">{idx+1}</text>\n'
    rows_text += f'<text x="100" y="{y_pos}" font-family="monospace" font-size="13" font-weight="bold" fill="#ffffff">{member.id}</text>\n'
    rows_text += f'<text x="320" y="{y_pos}" font-family="sans-serif" font-size="13" fill="#5865f2">{safe_uname}</text>\n'
    rows_text += f'<text x="600" y="{y_pos}" font-family="sans-serif" font-size="13" fill="#949ba4">#{member.discriminator}</text>\n'

  user_ids_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {svg_height}" width="100%" height="100%">
  <rect width="800" height="{svg_height}" fill="#1e1f22"/>
  <text x="30" y="45" font-family="sans-serif" font-size="20" font-weight="bold" fill="#ffffff">Scraped User IDs ({html.escape(guild.name)})</text>
  <text x="30" y="70" font-family="sans-serif" font-size="13" fill="#b5bac1">Total Scraped Members: {len(members)}</text>
  <rect x="30" y="85" width="740" height="25" fill="#383a40"/>
  <text x="50" y="102" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff">#</text>
  <text x="100" y="102" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff">USER ID</text>
  <text x="320" y="102" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff">USERNAME</text>
  <text x="600" y="102" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff">DISCRIMINATOR</text>
  {rows_text}
</svg>"""
  with open(f"{folder}/Scraped_User_IDs.svg", "w+", encoding="utf-8") as f:
    f.write(user_ids_svg)

  # 3. Master Avatars Gallery SVG Document (Direct URL linking)
  cols = 5
  box_size = 120
  grid_rows = (len(members) + cols - 1) // cols
  avatar_svg_height = max(150, 110 + grid_rows * (box_size + 25))

  avatar_nodes = ""
  for idx, member in enumerate(members):
    if member.avatar is None:
      continue
    r = idx // cols
    c = idx % cols
    x = 30 + c * (box_size + 25)
    y = 90 + r * (box_size + 25)
    img_url = html.escape(str(member.avatar.url))
    safe_uname = html.escape(clean_string(member.display_name))
    
    avatar_nodes += f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size+20}" rx="10" fill="#2b2d31"/>\n'
    avatar_nodes += f'<image href="{img_url}" x="{x+10}" y="{y+10}" width="{box_size-20}" height="{box_size-20}"/>\n'
    avatar_nodes += f'<text x="{x + box_size//2}" y="{y + box_size + 12}" font-family="sans-serif" font-size="11" fill="#ffffff" text-anchor="middle">{safe_uname[:14]}</text>\n'

  avatars_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {avatar_svg_height}" width="100%" height="100%">
  <rect width="760" height="{avatar_svg_height}" fill="#1e1f22"/>
  <text x="30" y="45" font-family="sans-serif" font-size="20" font-weight="bold" fill="#ffffff">Scraped Avatars Gallery ({html.escape(guild.name)})</text>
  <text x="30" y="70" font-family="sans-serif" font-size="13" fill="#b5bac1">Total Avatars Displayed: {len(members)}</text>
  {avatar_nodes}
</svg>"""
  with open(f"{folder}/Scraped_Avatars.svg", "w+", encoding="utf-8") as f:
    f.write(avatars_svg)

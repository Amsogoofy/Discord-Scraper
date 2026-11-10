import os
import re
import csv
import time
import asyncio
import random
import discord
from discord import Client, Guild, Member, User
from internal.utils import get_account_settings, Logger

logger = Logger()

def create_client():
    return Client(chunk_guilds_at_startup=True, guild_subscriptions=True)

client = create_client()

async def scrape_active_users(guild: Guild):
    """Scrapes active users via message history archives."""
    logger.scraper(f"Harvesting active user data from '{guild.name}' via message history...")
    users_data = {}
    text_channels = guild.text_channels
    total_channels = len(text_channels)
    
    if total_channels == 0:
        logger.error("No text channels found to scrape!")
        return [], "Scraped_Users_Active.csv"

    start_time = time.time()

    for idx, channel in enumerate(text_channels, start=1):
        percent = (idx / total_channels) * 100
        elapsed = time.time() - start_time
        avg_time = elapsed / idx
        eta_sec = int((total_channels - idx) * avg_time)
        
        print(f"\r[Scraper] [{percent:.1f}%] Channel {idx}/{total_channels} | ETA: {eta_sec}s   ", end="", flush=True)

        try:
            async for message in channel.history(limit=None):
                author = message.author
                if not author.bot and author.id not in users_data:
                    roles = []
                    is_admin = False
                    
                    # Check if user is currently in the guild
                    member_obj = guild.get_member(author.id)
                    in_server = "True" if member_obj else "False"

                    if isinstance(member_obj, Member):
                        roles = [role.name for role in member_obj.roles if role.name != "@everyone"]
                        try:
                            is_admin = member_obj.guild_permissions.administrator
                        except Exception:
                            is_admin = False
                    elif isinstance(author, Member):
                        roles = [role.name for role in author.roles if role.name != "@everyone"]
                        try:
                            is_admin = author.guild_permissions.administrator
                        except Exception:
                            is_admin = False

                    users_data[author.id] = {
                        "id": author.id,
                        "username": author.name,
                        "global_name": getattr(author, "global_name", author.name),
                        "roles": ", ".join(roles) if roles else "None",
                        "administrator": "Yes" if is_admin else "No",
                        "in_server": in_server
                    }
            await asyncio.sleep(random.uniform(1.5, 3.5))
        except Exception:
            continue

    print()
    logger.success(f"Harvested {len(users_data)} active profiles successfully!")
    return list(users_data.values()), "Scraped_Users_Active.csv"


async def scrape_member_roster(guild: Guild):
    """Scrapes all current members using Gateway Chunking (Opcode 8)."""
    logger.scraper(f"Requesting Gateway member chunking for '{guild.name}' (Total members: {guild.member_count})...")
    users_data = {}
    
    try:
        await guild.chunk()
        
        if guild.members:
            for member in guild.members:
                if member.bot:
                    continue
                
                roles = [role.name for role in member.roles if role.name != "@everyone"]
                try:
                    is_admin = member.guild_permissions.administrator
                except Exception:
                    is_admin = False

                users_data[member.id] = {
                    "id": member.id,
                    "username": member.name,
                    "global_name": getattr(member, "global_name", member.name),
                    "roles": ", ".join(roles) if roles else "None",
                    "administrator": "Yes" if is_admin else "No",
                    "in_server": "True"
                }
            
            logger.success(f"Successfully harvested {len(users_data)} members via Gateway Chunking!")
        else:
            logger.error("Gateway chunk returned 0 members. Falling back to history...")
            return await scrape_active_users(guild)
            
    except Exception as e:
        logger.error(f"Gateway chunking failed ({e}).")
        
    return list(users_data.values()), "Scraped_Members_Roster.csv"


async def scrape_historical_members(guild: Guild):
    """
    Scrapes ALL current members (via Gateway Chunking) 
    PLUS past/left members (via Audit Logs & Message History),
    tracking whether they are currently in the server (True/False).
    """
    logger.scraper(f"Harvesting ALL Current & Past members from '{guild.name}'...")
    users_data = {}
    current_member_ids = set()

    # 1. PULL ALL CURRENT MEMBERS VIA GATEWAY CHUNKING FIRST
    logger.scraper("Pulling complete current member roster via Gateway chunking...")
    try:
        await guild.chunk()
        if guild.members:
            for member in guild.members:
                if member.bot:
                    continue
                current_member_ids.add(member.id)
                roles = [role.name for role in member.roles if role.name != "@everyone"]
                try:
                    is_admin = member.guild_permissions.administrator
                except Exception:
                    is_admin = False

                users_data[member.id] = {
                    "id": member.id,
                    "username": member.name,
                    "global_name": getattr(member, "global_name", member.name),
                    "roles": ", ".join(roles) if roles else "None",
                    "administrator": "Yes" if is_admin else "No",
                    "in_server": "True"
                }
            logger.success(f"Loaded {len(users_data)} current members from roster.")
    except Exception as e:
        logger.error(f"Gateway chunking error during historical scrape: {e}")

    # 2. MINING AUDIT LOGS (For past/left members)
    logger.scraper("Mining Audit Logs for historical records...")
    try:
        async for entry in guild.audit_logs(limit=None):
            # Check target
            target = getattr(entry, 'target', None)
            if target and isinstance(target, (User, Member)) and not target.bot:
                if target.id not in users_data:
                    in_server = "True" if target.id in current_member_ids else "False"
                    users_data[target.id] = {
                        "id": target.id,
                        "username": target.name,
                        "global_name": getattr(target, "global_name", target.name),
                        "roles": "Historical / Left Server" if in_server == "False" else "None",
                        "administrator": "Unknown",
                        "in_server": in_server
                    }
            
            # Check actor
            actor = getattr(entry, 'user', None)
            if actor and isinstance(actor, (User, Member)) and not actor.bot:
                if actor.id not in users_data:
                    in_server = "True" if actor.id in current_member_ids else "False"
                    users_data[actor.id] = {
                        "id": actor.id,
                        "username": actor.name,
                        "global_name": getattr(actor, "global_name", actor.name),
                        "roles": "Audit Log Actor",
                        "administrator": "Unknown",
                        "in_server": in_server
                    }
        logger.success(f"Audit log mining complete. Total unique profiles now: {len(users_data)}")
    except Exception:
        logger.error("Could not read audit logs (Missing permissions). Continuing with remaining archives...")

    # 3. MESSAGE HISTORY SCAN (Extra insurance)
    logger.scraper("Scanning message history archives for any remaining profiles...")
    for channel in guild.text_channels:
        try:
            async for message in channel.history(limit=None):
                author = message.author
                if not author.bot and author.id not in users_data:
                    in_server = "True" if author.id in current_member_ids else "False"
                    roles = [r.name for r in author.roles if r.name != "@everyone"] if isinstance(author, Member) else []
                    is_admin = author.guild_permissions.administrator if isinstance(author, Member) else False
                    
                    users_data[author.id] = {
                        "id": author.id,
                        "username": author.name,
                        "global_name": getattr(author, "global_name", author.name),
                        "roles": ", ".join(roles) if roles else "None",
                        "administrator": "Yes" if is_admin else "No",
                        "in_server": in_server
                    }
            await asyncio.sleep(0.5)
        except Exception:
            continue

    logger.success(f"Final comprehensive collection (Current + Past): {len(users_data)} profiles!")
    return list(users_data.values()), "Scraped_All_Historical.csv"


def save_data_to_csv(guild, user_data_list, filename):
    safe_guild_name = re.sub(r'[\\/*?:"<>|]', "", guild.name).strip() or str(guild.id)
    dir_name = os.path.join("DataScraped", safe_guild_name)
    os.makedirs(dir_name, exist_ok=True)
    
    csv_path = os.path.join(dir_name, filename)
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["User ID", "Username", "Display Name", "Roles", "Administrator", "In Server"])
        for data in user_data_list:
            writer.writerow([
                data["id"],
                data["username"],
                data["global_name"],
                data["roles"],
                data["administrator"],
                data["in_server"]
            ])
            
    logger.success(f"Saved export to {csv_path}")


@client.event
async def on_ready():
    logger.scraper(f"Logged in as {client.user}")

    config = get_account_settings()
    guild_id = config.get("guild_id")
    mode = config.get("scrape_mode", "active")

    guild = client.get_guild(int(guild_id))
    if not guild:
        logger.error(f"Could not find guild with ID {guild_id}. Make sure you are in the server!")
        await client.close()
        return

    if mode == "roster":
        user_data_list, filename = await scrape_member_roster(guild)
    elif mode == "historical":
        user_data_list, filename = await scrape_historical_members(guild)
    else:
        user_data_list, filename = await scrape_active_users(guild)

    save_data_to_csv(guild, user_data_list, filename)
    logger.success("Scraping task complete!\n")
    await client.close()

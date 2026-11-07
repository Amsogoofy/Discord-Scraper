
    users_data = {}
    text_channels = guild.text_channels
    total_channels = len(text_channels)
    
    if total_channels == 0:
        logger.error("No text channels found to scrape!")
        return []

    start_time = time.time()

    for idx, channel in enumerate(text_channels, start=1):
        # Calculate progress percentage
        percent = (idx / total_channels) * 100
        
        # Calculate elapsed and estimated time remaining (ETA)
        elapsed = time.time() - start_time
        avg_time_per_channel = elapsed / idx
        remaining_channels = total_channels - idx
        eta_seconds = remaining_channels * avg_time_per_channel
        
        # Format ETA string
        eta_min = int(eta_seconds // 60)
        eta_sec = int(eta_seconds % 60)
        eta_str = f"{eta_min}m {eta_sec}s" if eta_min > 0 else f"{eta_sec}s"
        
        # Build visual progress bar (20 blocks wide)
        bar_length = 20
        filled_length = int(bar_length * idx // total_channels)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        
        # Print dynamic single-line progress status
        print(f"\r[Scraper] [{bar}] {percent:.1f}% ({idx}/{total_channels} channels) | ETA: {eta_str}   ", end="", flush=True)

        try:
            async for message in channel.history(limit=None):
                author = message.author
                if not author.bot and author.id not in users_data:
                    roles = []
                    is_admin = False
                    
                    if isinstance(author, Member):
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
                        "administrator": "Yes" if is_admin else "No"
                    }
        except Exception:
            # Skip channels with insufficient permissions or rate limits silently
            continue

    print() # Move to next line after progress loop finishes
    logger.success(f"Harvested {len(users_data)} unique user profiles successfully!")
    return list(users_data.values())


def save_data_to_csv(guild, user_data_list):
    safe_guild_name = re.sub(r'[\\/*?:"<>|]', "", guild.name).strip()
    if not safe_guild_name:
        safe_guild_name = str(guild.id)
        
    dir_name = os.path.join("DataScraped", safe_guild_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    csv_path = os.path.join(dir_name, "Scraped_Users_Detailed.csv")
    
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["User ID", "Username", "Display Name", "Roles", "Administrator"])
        for data in user_data_list:
            writer.writerow([
                data["id"],
                data["username"],
                data["global_name"],
                data["roles"],
                data["administrator"]
            ])
            
    logger.success(f"Saved detailed user data to {csv_path}")


@client.event
async def on_ready():
    logger.scraper(f"Logged in as {client.user}")

    config = get_account_settings()
    guild_id = config["guild_id"]

    guild = client.get_guild(int(guild_id))
    
    if not guild:
        logger.error(f"Could not find guild with ID {guild_id}. Make sure your account is in that server!")
        return

    user_data_list = await scrape_user_data(config, guild)

    save_data_to_csv(guild, user_data_list)

    logger.success("Finished harvesting user data! Output saved in server-specific folder.\n")
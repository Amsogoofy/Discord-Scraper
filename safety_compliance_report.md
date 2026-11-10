# Discord Guild Members Scraper - Safety & Compliance Report

## 1. Executive Summary

This document outlines the security considerations, risk factors, and compliance guidelines associated with running the Droom Guild Members Scraper. Because this tool relies on user account automation (`discord.py-self`), understanding the operational boundaries and safety implications is essential to protecting your Discord account and maintaining data integrity.

## 2. Platform Policy & Terms of Service (TOS) & Use at Your Own Risk

- **Use at Your Own Risk:** This project uses self-botting mechanisms (`discord.py-self`). Using user tokens or selfbots is strictly against Discord's Terms of Service (TOS). By using this project, you assume full responsibility for any potential consequences, including account flagging, locks, or permanent bans by Discord's automated safety systems.

## 3. Credential Security & Token Management

- **Token Safety & Local Storage:** Our tool is designed with local-only storage and secure handling for your authentication token within your local `config.json` file, meaning it is safe to input your token here for this tool's operation. However, as a general rule of thumb, you should normally exercise caution and avoid inputting your personal user token into unverified third-party scripts.
- **Never Share Your Token:** Do not paste your token into public chatrooms, GitHub repositories, or untrusted issue trackers. Ensure your `config.json` is never committed to public version control repositories (add `config.json` to your `.gitignore`).
- **Use Alt Accounts:** It is strongly recommended to run self-bot scrapers using a secondary "alt" account rather than your primary, personal Discord account to mitigate risk.

## 4. Data Privacy & Responsible Scraping

The tool extracts public messages, user IDs, usernames, display names, roles, administrator statuses, and membership presence (`In Server` flag) across text channels, audit logs, and gateway rosters.

### Ethical Guidelines

- **Data Minimization:** Only harvest data necessary for your specific research or administrative requirements.
- **Secure Storage:** Store scraped CSV files in secure, local directories (`DataScraped/[ServerName]/`). Avoid publishing user datasets publicly where individuals have not consented.
- **Server Rules:** Respect the privacy policies and community guidelines of the guilds you participate in.

## 5. Technical Mitigations & Rate-Limit Handling

To reduce the footprint on Discord's Gateway connection and prevent abrupt account flagging or rate-limiting (`429 Too Many Requests`), developers and operators should observe the following technical safeguards:

- **Anti-Flag Delays:** Do not remove or reduce the randomized sleep intervals between channel scans (`asyncio.sleep(random.uniform(1.5, 3.5))`).
- **Chunking Thresholds:** Be mindful of server size when invoking WebSocket Opcode 8 (`guild.chunk()`). Avoid excessively cycling chunk requests on massive public servers.
- **Console Monitoring:** Monitor console logs for any HTTP rate-limit warnings or unexpected connection disconnects, allowing the automatic exponential backoff to handle retries cleanly.

---

*Disclaimer: This tool is provided as-is for educational and administrative utility. The maintainers accept no liability for accounts flagged or banned by Discord's automated safety systems.*

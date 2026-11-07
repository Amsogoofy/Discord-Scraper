# <p align=center> Discord Guild Members Scraper
## <p align=center> Developed by Droom

- Give the project a star if you liked it! It'll help other people find it :)
- This project uses [discord.py-self](https://github.com/dolfies/discord.py-self). Using selfbots is against Discord's TOS, use this project at your own risk.
- The goal of the project is harvesting users in a specified guild, bypassing offline member limits by crawling message history across text channels. Extracts User IDs, Usernames, Display Names, assigned Roles, and Administrator permissions into a clean CSV file.

### Features
- **Offline Member Harvesting:** Bypasses gateway/member list restrictions by crawling channel message history to catch active, offline, and invisible users.
- **Detailed CSV Export:** Saves User ID, Account Username, Display Name, Roles, and Administrator status to `Scraped_Users_Detailed.csv`.
- **Live Progress & ETA:** Features a real-time terminal progress bar tracking scanned channels and calculating estimated time remaining.
- **Organized Storage:** Each guild has its own dedicated folder (`DataScraped/[ServerName]/`) so data is clean and easy to handle.

---

### PC Requirements & Installation Commands

Before running the tool, make sure you have the following installed on your PC:
1. **Python (v3.8 or newer)** — Ensure you check *"Add Python to PATH"* during installation.
2. **Git** — For cloning the repository.

If you don't have them installed, you can download them using your terminal or package manager:

```sh
# For Windows (using winget package manager):
winget install Python.Python.3.11
winget install Git.Git

# For macOS (using Homebrew):
brew install python git

# For Ubuntu / Debian Linux:
sudo apt update && sudo apt install python3 python3-pip git -y
```

### Repository Setup & Dependencies

Open your terminal (PowerShell, Command Prompt, or Bash) and run these commands to set up the project:

```sh
# 1. Clone the repository and navigate into the folder
git clone https://github.com/YourUsername/Discord-Scraper
cd Discord-Scraper

# 2. Install all required dependencies from requirements.txt
pip install -r requirements.txt
```

---

### Configuration (`config.json`)

The **only thing you need to change** on your end is the `'token'` field inside your `config.json` file. Replace the placeholder with your actual Discord account token.

```json
{
  "token": "YOUR_DISCORD_USER_TOKEN_HERE",
  "guild_id": 0,
  "pfp_format": "png",
  "purge_old_data": true,
  "download_pfp": true,
  "channel_id": 0
}
```

#### How to get your Discord Account Token:
1. Open Discord in your web browser (Chrome, Firefox, Edge, etc.) and log in.
2. Press `Ctrl + Shift + I` (or `F12`) to open the Developer Tools, then navigate to the **Application** tab (or **Storage** tab in Firefox).
3. On the left sidebar, expand **Local Storage** and click on `https://discord.com`.
4. In the search/filter bar, type `token`.
5. Copy the quoted string value (e.g., `OTcx...`) and paste it into your `config.json` under `"token"`.
6. ⚠️ **Warning:** Never share your user token with anyone! Anyone with your token has full access to your Discord account.

---

### How to Run the Scraper

1. Open your terminal (Command Prompt, PowerShell, or Terminal).
2. Use the `cd` command to navigate inside your project directory where `main.py` is located. For example:
   ```sh
   cd Downloads\Discord-Scraper\source
   ```
3. Run the script using Python:
   ```sh
   python main.py
   ```
# <p align="center">Discord Guild Members Scraper</p>
## <p align="center">Developed by Droom</p>

- Give the project a star if you liked it! It'll help other people find it :)
- This project uses [discord.py-self](https://github.com/dolfies/discord.py-self). Using selfbots is against Discord's TOS, use this project at your own risk.
- The goal of the project is harvesting comprehensive user rosters from a specified guild using a multi-modal approach (Active Chatters, Complete Roster Chunking, and Historical Audit Log Mining). Extracts User IDs, Usernames, Display Names, assigned Roles, Administrator permissions, and Server Membership status (`True`/`False`) into clean CSV files.

---

### Features

- **3 Flexible Scraping Modes:**
  1. **Active Message Scraper:** Scans recent and active message history across channels to capture active participants.
  2. **Complete Member Roster Scraper:** Uses Gateway WebSocket Chunking (`Opcode 8`) to pull all current server members instantly without needing admin permissions.
  3. **Historical Audit Log Scraper:** Mines audit logs and chat archives to capture **both current and past/left members**, tagging each record with an `In Server` status.
- **Detailed CSV Export:** Saves User ID, Username, Display Name, Roles, Administrator status, and an **`In Server` (`True`/`False`)** column to track active vs. historical members.
- **Live Progress & ETA:** Features a real-time terminal progress bar tracking scanned channels and calculating estimated time remaining.
- **Organized Storage:** Each guild has its own dedicated folder (`DataScraped/[ServerName]/`) so output data is clean and easy to manage.

---

### System Requirements & Installation

Before running the tool, make sure you have the following installed on your PC:
1. **Python (v3.8 or newer)** — Ensure you check *"Add Python to PATH"* during installation.
2. **Git** — For cloning the repository.

#### Package Manager Commands

```sh
# For Windows (using winget package manager):
winget install Python.Python.3.11
winget install Git.Git

# For macOS (using Homebrew):
brew install python git

# For Ubuntu / Debian Linux:
sudo apt update && sudo apt install python3 python3-pip git -y
```

---

### Repository Setup & Dependencies

Open your terminal (PowerShell, Command Prompt, or Bash) and run these commands to set up the project:

```sh
# 1. Clone the repository and navigate into the project folder
git clone https://github.com/YourUsername/Discord-Scraper
cd Discord-Scraper

# 2. Install required dependencies
pip install --upgrade -r requirements.txt
```

---

### Configuration (`config.json`)

The configuration file handles your user token and target guild settings.

```json
{
  "token": "YOUR_DISCORD_USER_TOKEN_HERE",
  "guild_id": 0,
  "pfp_format": "png",
  "purge_old_data": true,
  "download_pfp": false,
  "channel_id": 0
}
```

#### How to Retrieve Your Discord User Token:
1. Open Discord in your web browser (Chrome, Firefox, Edge, etc.) and log in.
2. Press `Ctrl + Shift + I` (or `F12`) to open Developer Tools, then navigate to the **Application** tab (or **Storage** tab in Firefox).
3. On the left sidebar, expand **Local Storage** and click on `https://discord.com`.
4. In the search/filter bar, type `token`.
5. Copy the quoted string value (e.g., `OTcx...`) and paste it into your `config.json` under `"token"`.
6. ⚠️ **Warning:** Never share your user token with anyone! Anyone with your token has full access to your account.

---

### How to Run the Scraper

1. Open your terminal (Command Prompt, PowerShell, or Terminal).
2. Navigate to the `source` directory where `main.py` is located:
   ```sh
   cd path\to\Discord-Scraper\source
   ```
3. Execute the program using Python:
   ```sh
   python main.py
   ```
4. Use the interactive menu to confirm your target Guild ID and select your preferred scraping mode (`1`, `2`, or `3`).

---

### CSV Output Structure

All exported files are saved under `DataScraped/[Guild Name]/` with the following column headers:

| Field Name | Description |
| :--- | :--- |
| **User ID** | The unique 18-digit Discord Snowflake ID for the account |
| **Username** | Account handle/username |
| **Display Name** | Server or global nickname |
| **Roles** | Comma-separated list of assigned server roles |
| **Administrator** | `Yes` or `No` indicator of admin permissions |
| **In Server** | `True` if currently in the server roster; `False` if past/left member |

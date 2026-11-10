# Changelog

All notable changes to the **Discord Guild Members Scraper** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] - 2026-11-10

### Added
- **`In Server` Column**: Introduced a boolean tracking field (`True`/`False`) across all CSV exports (`Scraped_Users_Active.csv`, `Scraped_Members_Roster.csv`, `Scraped_All_Historical.csv`) to distinguish active members from former/left members.
- **Safety & Compliance Documentation**: Added `SAFETY_COMPLIANCE.md` detailing security policies, user token protection guidelines, rate-limit mitigations, and ethical scraping boundaries.

### Changed
- **Historical Mode Enhancement (`[3]`)**: Refactored `scrape_historical_members()` to first execute Gateway Chunking (enforcing full active roster coverage) before merging historical audit log entries and chat history archives.
- **Client Session Configuration**: Updated `create_client()` in `internal/selfbot.py` to set `chunk_guilds_at_startup=True` and `guild_subscriptions=True` for reliable opcode 8 member streaming.

---

## [2.0.0] - 2026-11-08

### Added
- **Interactive Multi-Mode Terminal Menu**: Redesigned `source/main.py` with an interactive terminal interface allowing users to toggle between three distinct scraping modes at startup:
  1. Active Message Scraper (`active`)
  2. Complete Member Roster Scraper (`roster`)
  3. Historical Audit Log Scraper (`historical`)
- **Gateway Chunking Integration (Opcode 8)**: Implemented `guild.chunk()` to pull complete server rosters for servers under 1,000 members, bypassing REST API member list restrictions (`403 Missing Access`).
- **Audit Log Mining Engine**: Added `guild.audit_logs()` scanning to harvest historical interactions, deleted profile references, and former member accounts.

### Refactored
- **Multi-Mode Routing in `internal/selfbot.py`**: Separated scraping engines into `scrape_active_users()`, `scrape_member_roster()`, and `scrape_historical_members()`.
- **Dynamic Configuration Handling**: Updated `config.json` schema to dynamically save `scrape_mode` and handle active guild switching seamlessly.

---

## [1.1.0] - 2026-10-15

### Added
- **Rich Terminal Logging**: Integrated `rich` text formatting for real-time channel scanning progress bars, estimated time remaining (ETA), and status indicators.
- **Structured Output Directories**: Automated local directory creation under `DataScraped/[Guild Name]/` for organized guild-by-guild CSV exports.

### Changed
- Improved error handling for restricted channels (`discord.Forbidden`) during message history scanning.

---

## [1.0.0] - 2026-09-01

### Added
- **Initial Release**: Basic self-bot scraper built with `discord.py-self`.
- Features basic text channel message history scanning to collect active chatter profiles.
- Exports User ID, Username, Display Name, Roles, and Administrator status to CSV.
- Configuration template (`config.json`) and project dependencies setup (`requirements.txt`).

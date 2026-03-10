# 🏰 COC Attack Bot

An automated attack bot for **Clash of Clans** built with Python and OpenCV, featuring a Vue 3 monitoring dashboard for real-time log analysis.

> ⚠️ **Disclaimer:** This project is intended for **educational purposes only**. The use of bots may violate Supercell's Terms of Service. Use at your own risk.

---

## 📦 Project Structure

```
COC-Bot/
├── Python BOT/              # Core automation engine
│   ├── coc_bot.py           # Main bot logic
│   ├── logger.py            # Logging setup
│   ├── coc_config.json      # Bot configuration
│   ├── requirements.txt     # Python dependencies
│   └── templates/           # UI button screenshots for image matching
│       ├── attack_button.png
│       ├── multiplayer_button.png
│       ├── find_match_button.png
│       ├── return_home.png
│       ├── cancel/
│       └── airdefense/
│
└── VUE Monitoring System/   # Web dashboard for log analysis
    ├── src/
    │   ├── views/           # HomeView & LogView
    │   ├── components/      # UI components (LogLine, DropZone, etc.)
    │   ├── composables/     # useLogParser, useLogFilter, useDragDrop
    │   ├── stores/          # Pinia state management
    │   └── router/          # Vue Router config
    └── package.json
```

---

## ✨ Features

### 🤖 Python Bot
- **Image Recognition** – Detects in-game UI buttons using OpenCV template matching
- **Automated Navigation** – Finds multiplayer matches, initiates attacks, and returns home automatically
- **Smart Attack Logic** – Deploys heroes and units at configurable screen positions
- **Air Defense Targeting** – Targets air defenses with lightning spells via configurable coordinates
- **Human-like Input** – Randomized delays and mouse movement to reduce detection risk
- **Auto-Cancel** – Automatically cancels searches that exceed a configurable timeout
- **Continuous Loop** – Runs indefinitely with a configurable cycle limit
- **JSON Config** – All parameters (confidence threshold, battle time, keybinds, delays) are externalized to `coc_config.json`
- **Detailed Logging** – Session statistics and structured log output

### 📊 Vue Monitoring Dashboard
- **Drag & Drop** – Load bot log files directly into the browser
- **Log Parsing** – Parses structured `[TIMESTAMP] [LEVEL] Message` log format
- **Level Filtering** – Filter by `INFO`, `WARNING`, `ERROR`, and `DEBUG`
- **Overview Cards** – At-a-glance statistics for the current log session
- **Sidebar Navigation** – Browse and switch between multiple loaded log files

---

## 🚀 Getting Started

### Python Bot

**Requirements:** Python 3.8+

```bash
cd "Python BOT"
pip install -r requirements.txt
python coc_bot.py
```

On first run, the bot will warn about any missing template images. Take screenshots of the relevant in-game buttons and place them in the `templates/` folder as described in the console output.

### Vue Monitoring Dashboard

**Requirements:** Node.js 16+

```bash
cd "VUE Monitoring System"
npm install
npm run dev
```

Open `http://localhost:5173` in your browser and drag a bot log file into the dashboard.

---

## ⚙️ Configuration

Edit `Python BOT/coc_config.json` to customize bot behavior:

| Parameter | Default | Description |
|---|---|---|
| `confidence_threshold` | `0.7` | Minimum match confidence for template detection |
| `max_cycles` | `50` | Maximum number of attack cycles before stopping |
| `delay_between_cycles` | `10` | Seconds to wait between cycles |
| `battle_time` | `30` | Seconds to wait during a battle |
| `search_timeout` | `30` | Seconds before canceling a matchmaking search |
| `auto_cancel_timeout` | `45` | Seconds before triggering auto-cancel |
| `enable_auto_cancel` | `true` | Enable/disable the auto-cancel feature |
| `human_like_mouse` | `true` | Enable randomized mouse movement |
| `random_delay` | `[0.1, 0.5]` | Min/max random delay range in seconds |

Attack-specific settings (hero positions, keybinds, air defense coordinates) can be configured interactively via the bot's **main menu → option 3**.

---

## 🖥️ Bot Menu

```
=== MAIN MENU ===
1. Single Navigation + Attack Test
2. Continuous Navigation + Attack Loop
3. Configure Attack Settings
4. View Statistics
5. Exit
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Bot Engine | Python 3.8+ |
| Image Recognition | OpenCV (`cv2`) |
| GUI Automation | PyAutoGUI |
| Keyboard Hooks | `keyboard` library |
| Monitoring UI | Vue 3 + Vite |
| State Management | Pinia |
| Routing | Vue Router |

---

## 📁 Template Setup

The bot uses screenshot templates to locate buttons on screen. Place the following images in the `templates/` directory:

```
templates/
├── attack_button.png          # The "Attack" button on the home screen
├── multiplayer_button.png     # The "Multiplayer" option
├── find_match_button.png      # The "Find a Match" button
├── return_home.png            # The "Return Home" button after battle
├── cancel/
│   ├── cancel_attack.png      # Cancel button during search
│   └── cancel_ok.png          # Confirmation dialog OK button
└── airdefense/
    ├── airdefense_level6.png
    ├── airdefense_level7.png
    └── ...                    # One image per Air Defense level to detect
```

---

## 📄 License

This project is for educational purposes only. All rights to Clash of Clans belong to Supercell.

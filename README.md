# Roblox Unit Visualizer 🚀

A lightweight, cross-platform system tray application designed for Roblox players and developers to easily visualize large unit scales (from **K** to **Vg**).

[![License](https://img.shields.io/github/license/dubo78/Roblox-Unit-Visualizer)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey)](https://github.com/dubo78/Roblox-Unit-Visualizer/releases/latest)
[![Release](https://img.shields.io/github/v/release/dubo78/Roblox-Unit-Visualizer)](https://github.com/dubo78/Roblox-Unit-Visualizer/releases/latest)

---

## ✨ Features

- **Quick Dashboard**: View all 21 units (K to Vg) in a compact 7x3 grid layout.
- **Detailed Table**: Expand to see full names and zero counts for every unit.
- **Always on Top**: Keeps the visualizer visible while you play.
- **System Tray Integration**: Runs quietly in your taskbar (Windows) or menu bar (macOS).
- **Clean Aesthetic**: Modern Mint-colored UI with rounded corners and system fonts.

---

## 📥 Download

Get the latest version for your operating system:

👉 **[Download Latest Release](https://github.com/dubo78/Roblox-Unit-Visualizer/releases/latest)**

- **Windows**: Download `RobloxUnitVisualizer-Windows.exe`
- **macOS**: Download `RobloxUnitVisualizer-macOS.zip`, extract it, and move the `.app` to your Applications folder.

---

## 🛠 Troubleshooting: "App is damaged" Error

If you see a message saying **"Roblox Unit Visualizer is damaged and can't be opened"** on macOS, it is because the app is unsigned. You can easily fix this by following these steps:

1. Open **Terminal**.
2. Type the following command (make sure to include a **space** at the end):
   ```bash
   xattr -d com.apple.quarantine 
   ```
3. **Drag and drop** the `RobloxUnitVisualizer.app` file from your Finder directly into the Terminal window. This will automatically paste the correct file path.
4. Press **Enter**.
5. Now you can open the app normally!

### 💡 Note on the command:
- **What it does**: This command removes the "quarantine" flag that macOS automatically attaches to files downloaded from the internet for security reasons.
- **Moving the app**: Once you've run this command, you can move the app to any folder (like the `/Applications` folder) without having to run it again. The fix is permanent for that specific file.

---

## 🛠 Installation (Source Code)

If you prefer to run from source (Python 3.12+ required):

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dubo78/Roblox-Unit-Visualizer.git
   cd Roblox-Unit-Visualizer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   python main.py
   ```

---

## 🖥 Screenshots

| Dashboard View | Detailed View |
| :---: | :---: |
| ![Dashboard](screenshots/dashboard.png) | ![Detail](screenshots/detail.png) |

---

## 📝 Unit Reference

| Symbol | Full Name | Zeros |
| :--- | :--- | :--- |
| **K** | Thousand | 3 |
| **M** | Million | 6 |
| **B** | Billion | 9 |
| ... | ... | ... |
| **Vg** | Vigintillion | 63 |

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

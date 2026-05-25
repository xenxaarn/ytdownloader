# ⚡ Universal YouTube Downloader

A lightweight, cross-platform desktop application designed for high-speed YouTube media extraction. Built with Python, this tool features a modern GUI and supports multiple formats, including video (MP4, MKV) and audio (MP3, M4A).

## 🚀 Key Features
- **Modern Interface**: Clean, dark-themed UI built with `CustomTkinter`.
- **Format Flexibility**: Download in MP4, MKV, MP3, or M4A quality.
- **Smart Clipboard**: Automatically detects and pastes links from your clipboard.
- **Visual Feedback**: Real-time progress bar for long downloads.
- **Desktop Notifications**: Get alerted the moment your file is ready.
- **Standalone**: Built as a native binary—no Python installation required for end-users.

## 🛠️ How it works
This application functions using a three-tier architecture:
1. **GUI Thread**: Manages the interface and user interaction.
2. **Worker Thread**: Executes `yt-dlp` in the background to prevent interface freezing.
3. **FFmpeg Engine**: Utilizes `imageio-ffmpeg` to handle stream merging and transcoding.



## 📋 Requirements
- No manual Python setup is required if using the pre-compiled binary.
- To compile from source: `Python 3.10+` and `PyInstaller`.

## 📦 Installation
1. Navigate to the **[Releases](https://github.com/YOUR_USERNAME/ytdownloader/releases)** page.
2. Download the binary matching your OS (Windows, macOS, or Linux).
3. (Linux/macOS) Run `chmod +x ytdownloader` to grant execution permission.
4. Launch the application.

## ⚠️ Known Issues & Roadmap
- *JavaScript Runtime Warning*: `yt-dlp` may occasionally prompt for a JS runtime. Installing Node.js resolves this.
- *Future Plan*: Add playlist bulk downloading and custom thumbnail extraction.

## ⚖️ License
This project is open-source under the **MIT License**.
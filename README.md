# 🎵 YouTube Audio Downloader Bot

A simple Telegram bot that lets you download audio from YouTube by just typing the name of a song.  
It searches YouTube, finds the best match, downloads the audio, and sends it to you — all within Telegram.

## 🚀 Features

- Search YouTube by song name
- Download high-quality audio
- Fast response
- Clean and minimal interface

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/Tribedn/MerySearchBot
cd MerySearchBot
```
```bash
python3 main.py
```

##If you going to deploying Bot on Google Cloud/VPS with Ubuntu 20.04 LTS(With Python 3.9):

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.9 python3.9-venv python3.9-dev
```
Check that Python 3.9 is installed:
```bash
python3.9 --version
```
🧪 Create a virtual environment

Navigate to your bot's directory and run:
```bash
python3.9 -m venv venv
source venv/bin/activate
```
After that you need install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

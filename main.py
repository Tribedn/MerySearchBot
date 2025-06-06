import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
from yt_dlp import YoutubeDL
from pytube import Search
from config import BOT_TOKEN  # Твій токен бота
from typing import Tuple

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

search_cache = {}
audio_cache = {}

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    user_name = message.from_user.first_name or "друже"
    await message.answer(
        f"Привіт, {user_name}! 👋\n\n"
        "Надішли мені назву пісні, і я знайду її на YouTube та надішлю в MP3 🎵"
    )

@dp.message(F.text & ~F.text.startswith("/"))
async def search_youtube(message: Message):
    query = message.text.strip()
    search = Search(query)
    results = search.results[:5]

    if not results:
        await message.answer("❌ Нічого не знайдено.")
        return

    search_cache[str(message.from_user.id)] = results

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=video.title[:50], callback_data=f"select_{i}")]
            for i, video in enumerate(results)
        ]
    )

    await message.answer("🔍 Вибери пісню зі списку:", reply_markup=keyboard)

def download_audio_yt_dlp(url: str) -> Tuple[str, str]:
    os.makedirs('downloads', exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'audio')

        # Назва файлу без розширення
        downloaded_basename = ydl.prepare_filename(info)
        mp3_filename = os.path.splitext(downloaded_basename)[0] + '.mp3'

        if not os.path.exists(mp3_filename):
            raise FileNotFoundError(f"MP3 файл не знайдено: {mp3_filename}")

        return mp3_filename, title


@dp.callback_query(F.data.startswith("select_"))
async def audio_selection(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    index = int(callback.data.split("_")[1])
    videos = search_cache.get(user_id)

    if not videos or index >= len(videos):
        await callback.message.edit_text("❌ Невірний вибір.")
        return

    video = videos[index]
    video_id = video.video_id

    await callback.message.edit_text(f"🎧 Завантажую: {video.title}")

    if video_id in audio_cache and os.path.exists(audio_cache[video_id]):
        mp3_path = audio_cache[video_id]
        title = video.title
    else:
        mp3_path, title = await asyncio.to_thread(download_audio_yt_dlp, video.watch_url)
        audio_cache[video_id] = mp3_path

    if not os.path.exists(mp3_path):
        await callback.message.answer("❌ Помилка при завантаженні.")
        return

    await callback.message.answer_audio(
        audio=FSInputFile(mp3_path),
        title=title,
        caption="🔗 Завантажуй аудіо тут 👉 @MerySearchBot"
    )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

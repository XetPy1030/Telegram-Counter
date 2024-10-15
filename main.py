import os
from collections import defaultdict
from datetime import timedelta, datetime, timezone

from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
client = TelegramClient(
    'bot_session', api_id, api_hash,
    system_version='4.16.30-vxCUSTOM',
    device_model='POCO M4 Pro',
    app_version='1.0'
)

client.start()

# Слова, которые мы ищем в сообщениях
words_count = ["👎", "❤️", "💌 / 📹"]
diff_time = timedelta(days=7)


@client.on(events.NewMessage(pattern='/count'))
async def count_handler(event):
    chat = await event.get_chat()

    print(f"Start counting in {chat}")
    counter = defaultdict(int)
    async for message in client.iter_messages(chat):
        if message.date < datetime.now(timezone.utc) - diff_time:
            break

        for word in words_count:
            if word == message.text:
                counter[word] += 1

    print(f"Counting in {chat} finished")
    await event.respond(f"Counting in {chat} finished\n{counter}")


client.run_until_disconnected()

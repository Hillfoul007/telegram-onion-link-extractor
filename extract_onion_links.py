import re
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.types import Message

# Replace with your credentials from my.telegram.org
api_id = 22640901  # e.g. 123456
api_hash = '5155aa21d8e2ac9a14eb023f7110882a'  # e.g. '0123456789abcdef0123456789abcdef'

onion_pattern = re.compile(r"(http[s]?://)?([a-zA-Z0-9]{16,56})\.onion\b")

async def extract_onion_links(channel_username, limit=100):
    async with TelegramClient('anon', api_id, api_hash) as client:
        messages = await client.get_messages(channel_username, limit=limit)
        onion_links = set()

        for message in messages:
            if isinstance(message, Message) and message.message:
                matches = onion_pattern.findall(message.message)
                for match in matches:
                    url = match[0] + match[1] + '.onion'
                    onion_links.add(url)

        print(f"\nFound {len(onion_links)} .onion link(s):")
        for link in onion_links:
            print(link)

if __name__ == '__main__':
    channel = input("Enter Telegram channel (username or invite link): ")
    limit = input("How many recent messages to scan? [Default 100]: ")
    limit = int(limit) if limit.isdigit() else 100
    asyncio.run(extract_onion_links(channel.strip(), limit))

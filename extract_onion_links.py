import re
import json
import asyncio
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# Replace with your own API credentials
api_id = '22640901'
api_hash = '5155aa21d8e2ac9a14eb023f7110882a'
channel_username = 'toronionlinks'  # or any public channel

output_file = 'onion_links.json'
last_id_file = 'last_message_id.txt'

onion_regex = re.compile(r"https?://[a-zA-Z0-9]{16,56}\.onion")

async def main():
    client = TelegramClient('anon', api_id, api_hash)
    await client.start()

    # Load last message ID if exists
    last_id = 0
    try:
        with open(last_id_file, 'r') as f:
            last_id = int(f.read().strip())
    except FileNotFoundError:
        pass

    # Fetch history
    channel = await client.get_entity(channel_username)
    messages = await client(GetHistoryRequest(
        peer=channel,
        limit=100,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=last_id,
        add_offset=0,
        hash=0
    ))

    max_message_id = last_id
    with open(output_file, 'a') as out_file:
        for message in messages.messages:
            if message.id > max_message_id:
                max_message_id = message.id
            if message.message:
                links = onion_regex.findall(message.message)
                for link in links:
                    result = {
                        "source": "telegram",
                        "url": link,
                        "discovered_at": datetime.utcnow().isoformat() + 'Z',
                        "context": f"Found in Telegram channel @{channel_username}",
                        "status": "pending"
                    }
                    out_file.write(json.dumps(result) + '\n')
                    print(f"Extracted: {link}")

    # Save the latest message ID
    with open(last_id_file, 'w') as f:
        f.write(str(max_message_id))

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())

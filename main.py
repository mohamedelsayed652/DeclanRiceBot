from __future__ import annotations

import os
from typing import Final

from dotenv import load_dotenv
from discord import Client, Intents, Message

from Responses import get_response

load_dotenv()
TOKEN: Final | None = os.getenv("DISCORD_TOKEN")

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("User message is empty")
        return

    is_private: bool = user_message.startswith("?")
    if is_private:
        user_message = user_message[1:]

    try:
        response: str = await get_response(user_message)
    except Exception as error:  # pragma: no cover - log unexpected issues
        print(f"Error while generating response: {error}")
        await message.channel.send(
            "Sorry, I had trouble figuring that out. Please try again later."
        )
        return

    if not response:
        print("No response generated")
        return

    destination = message.author if is_private else message.channel
    await destination.send(response)


@client.event
async def on_ready() -> None:
    assert client.user is not None
    print(f"{client.user} is making tackles in the midfield!")


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f"{username} said {user_message} in {channel}")
    await send_message(message, user_message)


def main() -> None:
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN is not set in the environment")

    client.run(TOKEN)


if __name__ == "__main__":
    main()

from __future__ import annotations

from random import choice
from typing import Final

from arsenal_stats import build_arsenal_stats_report


SMALL_TALK_RESPONSES: Final = (
    "I love Declan Rice!",
    "Declan Rice is the best!",
    "I am a huge fan of Declan Rice!",
    "Declan Rice is my favorite player!",
    "I can talk about Declan Rice all day!",
    "Declan Rice is amazing!",
    "Do you want to know more about Declan Rice?",
    "Declan Rice is a fantastic player!",
    "I admire Declan Rice so much!",
)


async def get_response(user_input: str) -> str:
    message = user_input.strip()
    lowered: str = message.lower()

    if not message:
        return "Hello?"
    if lowered in {"hi", "hello", "hey"}:
        return "Hello!"
    if lowered in {"do you like declan rice?", "do you like declan rice"}:
        return "I love Declan Rice! He's the best!"

    if lowered in {
        "!arsenal",
        "!arsenal stats",
        "arsenal stats",
        "!arsenal next",
        "!arsenal latest",
    }:
        return await build_arsenal_stats_report()

    return choice(SMALL_TALK_RESPONSES)

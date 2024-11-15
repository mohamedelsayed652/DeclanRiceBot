from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from Responses import get_response

load_dotenv()
TOKEN: Final = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True # NOQA
cleint: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('User message is empty')
        return
    
    
    
    if is_private:= user_message[0] == '?':
        user_message = user_message[1:] 
        
        
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
        
    except Exception as e:
        print(f'Error: {e}')
        
        
@cleint.event
async def on_ready() -> None:
    print(f'{cleint.user} is making tackles in the midfield!')
    
@cleint.event
async def on_message(message: Message) -> None:
    if message.author == cleint.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel:str = str(message.channel)
    
    print(f'{username} said {user_message} in {channel}')
    await send_message(message, user_message)
    
def main() -> None:
    cleint.run(TOKEN)
    
if __name__ == '__main__':
    main()
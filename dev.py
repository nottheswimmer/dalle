import os
import asyncio
import platform

from dalle.imperative.api.labs import get_bearer_token, get_bearer_token_async

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

OPENAI_USERNAME = os.environ.get('OPENAI_USERNAME')
OPENAI_PASSWORD = os.environ.get('OPENAI_PASSWORD')


def main():
    print("Attempting to get token for DALL-E...")
    token = get_bearer_token(OPENAI_USERNAME, OPENAI_PASSWORD)
    print("Token:", token)


async def main_async():
    print("Attempting to get token for DALL-E...")
    token = await get_bearer_token_async(OPENAI_USERNAME, OPENAI_PASSWORD)
    print("Token:", token)


if __name__ == '__main__':
    # main()
    asyncio.run(main_async())

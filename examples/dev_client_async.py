import os
import asyncio
import platform

from PIL import Image

from pydalle import Dalle

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

OPENAI_USERNAME = os.environ.get('OPENAI_USERNAME')
OPENAI_PASSWORD = os.environ.get('OPENAI_PASSWORD')


async def main():
    client = Dalle(OPENAI_USERNAME, OPENAI_PASSWORD)
    print(f"Client created. {(await client.get_credit_summary_async()).aggregate_credits} credits remaining...")
    tasks = client.get_tasks(limit=5)
    print(f"{len(tasks)} tasks found...")

    print("Attempting to do a text2im task...")
    completed_text2im_task = await client.text2im_async("A cute cat")
    async for image in completed_text2im_task.download_async():
        image.to_pil().show()

    print("Attempting to create variations task on the first cat...")
    first_generation = completed_text2im_task.generations[0]
    completed_variation_task = first_generation.variations()
    first_variation = completed_variation_task.generations[0]
    first_image = (await first_variation.download_async()).to_pil()
    first_image.show()

    print("Attempting to create inpainting task and showing the mask...")
    mask = first_image.convert("RGBA")
    # Make the right-side of the image transparent by pasting over the right side of the image with a transparent image
    mask.paste(Image.new('RGBA', (mask.width, mask.height), (0, 0, 0, 0)), (mask.width // 2, 0))
    mask.show("inpainting mask")
    completed_inpainting_task = await first_generation.inpainting_async("A cute cat, with a dark side", mask)
    async for image in completed_inpainting_task.download_async():
        image.to_pil().show()


if __name__ == '__main__':
    asyncio.run(main())

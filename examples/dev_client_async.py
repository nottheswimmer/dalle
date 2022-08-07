import os
import asyncio
import platform

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
    # Make the right-side of the image transparent
    masked_image = first_image.convert("RGBA")
    for i in range(masked_image.width):
        if i > masked_image.width / 2:
            for j in range(masked_image.height):
                masked_image.putpixel((i, j), (0, 0, 0, 0))
    masked_image.show("inpainting mask")
    completed_inpainting_task = await first_generation.inpainting_async("A cute cat, with a dark side", masked_image)
    async for image in completed_inpainting_task.download_async():
        image.to_pil().show()


if __name__ == '__main__':
    asyncio.run(main())

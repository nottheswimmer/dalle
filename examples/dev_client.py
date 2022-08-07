import os

from pydalle import Dalle

OPENAI_USERNAME = os.environ.get('OPENAI_USERNAME')
OPENAI_PASSWORD = os.environ.get('OPENAI_PASSWORD')


def main():
    client = Dalle(OPENAI_USERNAME, OPENAI_PASSWORD)
    print(f"Client created. {client.get_credit_summary().aggregate_credits} credits remaining...")
    tasks = client.get_tasks(limit=5)
    print(f"{len(tasks)} tasks found...")

    print("Attempting to do a text2im task...")
    completed_text2im_task = client.text2im("A cute cat")
    for image in completed_text2im_task.download():
        image.to_pil().show()

    print("Attempting to create variations task on the first cat...")
    first_generation = completed_text2im_task.generations[0]
    completed_variation_task = first_generation.variations()
    first_variation = completed_variation_task.generations[0]
    first_image = first_variation.download().to_pil()
    first_image.show()

    print("Attempting to create inpainting task and showing the mask...")
    # Make the right-side of the image transparent
    masked_image = first_image.convert("RGBA")
    for i in range(masked_image.width):
        if i > masked_image.width / 2:
            for j in range(masked_image.height):
                masked_image.putpixel((i, j), (0, 0, 0, 0))
    masked_image.show("inpainting mask")
    completed_inpainting_task = first_generation.inpainting("A cute cat, with a dark side", masked_image)
    for image in completed_inpainting_task.download():
        image.to_pil().show()


if __name__ == '__main__':
    main()

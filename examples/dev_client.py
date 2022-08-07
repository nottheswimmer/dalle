import os

from pydalle import Dalle

OPENAI_USERNAME = os.environ.get('OPENAI_USERNAME')
OPENAI_PASSWORD = os.environ.get('OPENAI_PASSWORD')


def main():
    client = Dalle(OPENAI_USERNAME, OPENAI_PASSWORD)
    print(f"Client created. {client.get_credit_summary().aggregate_credits} credits remaining...")
    tasks = client.get_tasks(limit=5)
    print(f"{len(tasks)} tasks found...")

    print("Attempting to download a generation of the first task and show off some built-in helpers...")
    if tasks and tasks[0].generations:
        example = tasks[0].generations[0].download()
        example.to_pil().show()  # Convert the image to a PIL image and show it
        example.to_pil_masked(x1=0.5, y1=0, x2=1, y2=1).show()  # Show a version with left side transparent (for edits)
        example.to_pil_padded(0.5).show()  # Show w/ 50% padding around the image, centered at (50%, 50%)
        example.to_pil_padded(0.4, cx=0.25, cy=0.25).show()  # Show w/ 40% padding, centered at (25%, 25%)

    print("Attempting to do a text2im task...")
    completed_text2im_task = client.text2im("A cute cat")
    for image in completed_text2im_task.download():
        image.to_pil().show()

    print("Attempting to create variations task on the first cat...")
    first_generation = completed_text2im_task.generations[0]
    completed_variation_task = first_generation.variations()
    first_variation = completed_variation_task.generations[0]
    first_image = first_variation.download()
    first_image.to_pil().show()

    print("Attempting to create inpainting task and showing the mask...")
    # Make the right-side of the image transparent
    mask = first_image.to_pil_masked(x1=0.5, y1=0, x2=1, y2=1)
    mask.show("inpainting mask")
    completed_inpainting_task = first_generation.inpainting("A cute cat, with a dark side", mask)
    for image in completed_inpainting_task.download():
        image.to_pil().show()


if __name__ == '__main__':
    main()

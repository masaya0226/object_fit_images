from PIL import Image, ImageDraw
from pathlib import Path
import click
import mimetypes

FRAME_COLOR = (255, 255, 255)

def object_fit_image(image: Path) -> Image:
    image_name = str(image)

    src_image = Image.open(image_name)
    sw, sh = src_image.size

    canvas_image = Image.new('RGB', (sh, sh))
    canvas = ImageDraw.Draw(canvas_image)
    canvas.rectangle([(0, 0), (sh, sh)], fill=FRAME_COLOR)
    canvas_image.paste(src_image, (int((sh-sw)/2), 0))
    return canvas_image

@click.command()
@click.argument('path')
def main(path: str):
    images_dir = "input" / Path(path)
    output_dir = "output" / Path(path)
    output_dir.mkdir(exist_ok=True)
    images = list(images_dir.iterdir())
    
    for image in images:
        if mimetypes.guess_type(image)[0] != "image/jpeg":
            continue
        fixed_image = object_fit_image(image)
        fixed_image.save(output_dir / image.name)

if __name__ == "__main__":
    main()



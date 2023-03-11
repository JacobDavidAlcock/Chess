from PIL import Image
import os

for imageName in os.listdir('Icons/'):
    image = Image.open('Icons/' + imageName)
    # Convert the image to RGBA mode
    image = image.convert('RGBA')

    # Get the pixel data from the image
    pixels = image.load()

    # Loop through each pixel in the image
    for x in range(image.width):
        for y in range(image.height):
            # Get the color of the pixel
            color = pixels[x, y]

            # Check if the color is black
            if color == (0, 0, 0, 255):
                # Set the color to white
                pixels[x, y] = (255, 255, 255, 255)

    # Save the image
    image.save('Icons/' + imageName + "_white.png")

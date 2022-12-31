from PIL import Image
import os
from os import listdir
from fpdf import FPDF

def MakePDF():
    
    pdf = FPDF()
    pdf = FPDF(orientation="landscape", format="A5")
    image_list = []
    folder_dir = "./Images/"
    for image in os.listdir(folder_dir):

        if (image.endswith(".png")):
            ##imageInput = Image.open(folder_dir + image)
            #image_list.append(imageInput.convert('RGB'))
            image_list.append(folder_dir + image)
         

    for image in image_list:
        pdf.add_page()
        pdf.image(image, 30, 3 ,150,150)

    if os.path.exists("Output.pdf"):
        os.remove("Output.pdf")

    with open("Output.pdf", "w") as my_file:
        pdf.output("Output.pdf", "F")


if __name__ == '__main__':
    MakePDF()
    
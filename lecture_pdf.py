try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\lamar\miniconda2\envs\tesseract\Library\bin\tesseract.exe'

from pdf2image import convert_from_path


def from_pdf_to_text(path):
    pages = convert_from_path(path)
    #Saving pages in jpeg format
    pages[0].save('fichiers_analyse_pdf/out.jpg', 'JPEG')
    text_from_image = pytesseract.image_to_string(Image.open('fichiers_analyse_pdf/out.jpg'))
    return text_from_image

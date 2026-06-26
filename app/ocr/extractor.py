from pdf2image import convert_from_path
import pytesseract
from app.models.schemas import TextBlock
from app.config import settings

def _extract_with_tesseract(pdf_path: str) -> list[TextBlock]:
    images = convert_from_path(pdf_path, dpi=300)
    info = []

    for index, image in enumerate(images):
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT) # output_type=pytesseract.Output.DICT to get the dict format

        for i in range(len(data['text'])):
            if data['text'][i].strip() == "":
                continue
            else:
                textblock = TextBlock(
                    text = data['text'][i],
                    x = data['left'][i],
                    y = data['top'][i],
                    width = data['width'][i],
                    height = data['height'][i],
                    page_number = index + 1,
                    confidence = (data['conf'][i])/100
                )

            info.append(textblock)

    return info

def _extract_with_cloud_vision(pdf_path: str) -> list[TextBlock]: 
    raise NotImplementedError("Cloud Vision backend not yet implemneted")

def extract_text_blocks(pdf_path):
    ocr = settings.ocr_backend

    if ocr == 'tesseract':
        return _extract_with_tesseract(pdf_path)
    return _extract_with_cloud_vision(pdf_path)
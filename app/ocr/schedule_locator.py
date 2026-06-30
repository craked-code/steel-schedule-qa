from pdf2image import convert_from_path
from transformers import AutoImageProcessor, AutoModelForObjectDetection
import torch
from app.models.schemas import Table
from app.config import settings


def detect_table_pos(images):
    #images = convert_from_path(pdf_path=pdf_path, dpi=300)

    processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
    model = AutoModelForObjectDetection.from_pretrained("microsoft/table-transformer-detection")
    detected_tables = []

    for index, i in enumerate(images):
        image = i.convert("RGB")
        image.save(f"s{index}-test-page.png")

        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        target_size = torch.tensor([image.size[::-1]])
        results = processor.post_process_object_detection(
            outputs, target_sizes=target_size, threshold=settings.table_detection_conf_threshold
        )[0]

        for box, score, category in zip(results["boxes"], results["scores"], results["labels"]):
            #x[0], box[1], box[2], box[3] are 0 dimension tensors not floats, so use .item() to change into float/int accordingly
            x_min, y_min, x_max, y_max = box.tolist()
            page_number = index
            confidence = score.item()
            label = model.config.id2label[category.item()]

            table = Table(
                x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, page_number=page_number, confidence=confidence, label=label
            )
            detected_tables.append(table)

    return detected_tables
            
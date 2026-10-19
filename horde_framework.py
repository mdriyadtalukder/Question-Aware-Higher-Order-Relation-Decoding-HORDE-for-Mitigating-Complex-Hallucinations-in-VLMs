

from google.colab import drive
drive.mount('/content/drive')

# cp -r '/content/drive/MyDrive/Research Paper/vlm' '/content/vlm'

from google.colab import drive
drive.mount('/content/drive')

import os
import zipfile

zip_path = '/content/drive/MyDrive/Research Paper/vlm hallucination/web_data.zip'
extract_path = '/content/vlm'

os.makedirs(extract_path, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print("Extraction completed!")
print("Files extracted to:", extract_path)

"""# **Step 1 — Load your dataset in Google Colab**"""

# Step 1.1: Check whether Google Colab provides a GPU

import torch

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("No GPU available. Enable GPU in Runtime settings.")

# Install basic libraries for dataset preparation
!pip install -q pillow

# Step 1.2: Load the dataset JSON file from Google Drive

import os
import json

json_path = '/content/vlm/web_data/web_v1.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("JSON file:", os.path.basename(json_path))
print("Dataset loaded successfully!")

# Step 1.3: Load JSON records

import json

with open(json_path, "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Many datasets use a list of records.
# Some instead store records inside a dictionary.
if isinstance(dataset, dict):
    print("Top-level JSON keys:", dataset.keys())
else:
    print("Total records:", len(dataset))
    print("First record:")
    print(json.dumps(dataset[0], indent=2, ensure_ascii=False))

# Step 1.4: Set the folder path containing dataset images

image_folder = '/content/vlm/web_data/images'

import os

if not os.path.isdir(image_folder):
    raise FileNotFoundError(f"Image folder not found: {image_folder}")

image_filenames = os.listdir(image_folder)

print("Image folder:", image_folder)
print("Total files:", len(image_filenames))
print("First 10 files:", image_filenames[:10])

# Step 1.5: Inspect the first image-question pair

from pathlib import Path
from PIL import Image
from IPython.display import display
import json

print(json.dumps(dataset[0], indent=2, ensure_ascii=False))
# Get dataset records
records = dataset if isinstance(dataset, list) else (
    dataset.get("data")
    or dataset.get("questions")
    or dataset.get("annotations")
)

if not records:
    raise ValueError("No dataset records found.")

# Select first record
record = records[0]

# Extract fields using your JSON structure
question_id = record["question_id"]
image_filename = record["image"]
question = record["text"]
reference_answer = record["label"]

print("Question ID:", question_id)
print("Image filename:", image_filename)
print("Question:", question)
print("Reference answer:", reference_answer)
print("Type:", record["type"])

# Locate the image using its exact filename
image_dir = Path(image_folder)
matches = list(image_dir.rglob(image_filename))

if matches:
    image_path = matches[0]

    with Image.open(image_path) as img:
        print("\nMatched image:", image_path)
        display(img.convert("RGB"))
else:
    print("\nImage not found:", image_filename)
    print("Check the image folder path:", image_dir)


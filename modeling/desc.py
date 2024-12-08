from transformers import pipeline, CLIPProcessor, CLIPModel
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
from PIL import Image
import torch
from transformers import AutoProcessor, Blip2ForConditionalGeneration



def description(text=None, image=None):
    
    #need to change use_auth_token
    processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b", use_auth_token="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")
    
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b",
    torch_dtype=torch.float16,
    use_auth_token="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"
    )
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)


    def desc(text=None, image_path=None):
        if text and image_path:
            if len(text) > 100 or (image_path is None or image_path == ""):
                try:
                    summary = summarizer(text, max_length=100, min_length=10, do_sample=False, truncation=True)[0]['summary_text']
                except IndexError:
                    print(f"Skipping summarization for text: {text[:50]}...")  # Print a portion of the problematic text
                    summary = text
                return summary
            else:
                image = Image.open(image_path).convert("RGB")
                inputs = processor(image, text=text, return_tensors="pt").to(device, torch.float16)
                generated_ids = model.generate(**inputs, max_new_tokens=100)
                generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
                return generated_text

        elif text:
            try:
                summary = summarizer(text, max_length=100, min_length=10, do_sample=False, truncation=True)[0]['summary_text']
            except IndexError:
                print(f"Skipping summarization for text: {text[:50]}...")  # Print a portion of the problematic text
                summary = text
            return summary

        elif image_path:
                image = Image.open(image_path).convert("RGB")
                inputs = processor(image, text=text, return_tensors="pt").to(device, torch.float16)
                generated_ids = model.generate(**inputs, max_new_tokens=100)
                generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
                return generated_text


        else:
            return "No valid input provided. Please provide text or an image."
    
    return desc(text,image)
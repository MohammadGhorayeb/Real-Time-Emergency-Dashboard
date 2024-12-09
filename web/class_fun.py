import torch
from transformers import BertForSequenceClassification, BertTokenizer


def classification(text):
    # Path to the extracted model
    model_path = '/home/moegho/Desktop/490_Project/fine_tuned_model'
        

    # Load the model and tokenizer
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
        

    # Label mapping
    label_mapping = {
        "Medical assistance": 0,
        "Shelter request": 1,
        "Supplies needed": 2,
        "Evacuation support": 3,
        "Rescue operations": 4,
        "Mental health support": 5,
        "Infrastructure repair": 6,
        "Animal rescue assistance": 7,
        "No assistance needed": 8,
        "Authority intervention": 9
    }

    # Inverse mapping to get class names from indices
    inverse_label_mapping = {v: k for k, v in label_mapping.items()}
        

    def classify_text(text):
        # Tokenize the input text
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

        # Get model outputs
        outputs = model(**inputs)

        # Get predictions
        predictions = torch.argmax(outputs.logits, dim=-1)

        # Get the class label from the index
        class_label = inverse_label_mapping[predictions.item()]

        return class_label

    return classify_text(text)
        

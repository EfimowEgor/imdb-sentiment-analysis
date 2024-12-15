from transformers import BertTokenizer, BertModel
from config import Settings

settings = Settings()

model_name = settings.model_name
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

model.save_pretrained(settings.model_path)
tokenizer.save_pretrained(settings.model_path)

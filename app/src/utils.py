import torch
from transformers import (BertTokenizer, 
                          BertModel)

def load_bert_components(path: str, device: str):
    tokenizer = BertTokenizer.from_pretrained(path)
    model = BertModel.from_pretrained(path)
    
    model.to(device)
    
    return tokenizer, model

def get_embeddings(texts: list, tokenizer, model, batch_size: int = 32, device: str = 'cuda'):
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        
        inputs = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        cls_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        yield cls_embeddings

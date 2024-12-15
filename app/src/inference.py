import joblib
import torch
from utils import (get_embeddings,
                   load_bert_components)
from config import Settings

def get_review() -> str:
    review = input()

    return review

if __name__ == "__main__":
    settings = Settings()
    
    review = get_review()

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    tokenizer, model = load_bert_components(settings.model_path, device)

    embeddings = next(get_embeddings([review], tokenizer, model, batch_size=1, device=device))

    with open('../models/sgd_classifier_model.pkl', 'rb') as f:
        clf = joblib.load(f)



    pred = clf.predict(embeddings[0].reshape(1, -1))

    print(pred)




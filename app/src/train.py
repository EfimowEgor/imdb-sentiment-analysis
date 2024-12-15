import logging
import joblib
import pandas as pd
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import f1_score
from config import Settings
from utils import (get_embeddings,
                   load_bert_components)


def load_data(path: str):
    df = pd.read_csv(path)
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    settings = Settings()

    logging.info("Loading components")

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    tokenizer, model = load_bert_components(settings.model_path, device)
    data = load_data(settings.data_path)

    texts = data["text"].tolist()
    labels = data["rating"].tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    clf = SGDClassifier(loss="log_loss", random_state=42)

    logging.info("Started fitting model")

    batch_size = 256
    count = 0
    threshold = 2000

    for embeddings in get_embeddings(X_train, tokenizer, model, batch_size=batch_size, device=device):
        batch_labels = y_train[:len(embeddings)]
        y_train = y_train[len(embeddings):]
        clf.partial_fit(embeddings, batch_labels, classes=np.unique(labels))

        count += len(embeddings)

        if count >= threshold:
            logging.info(f"Processed {count} training samples.")
            threshold += 2000

    y_pred = []
    for test_embeddings in get_embeddings(X_test, tokenizer, model, batch_size=batch_size, device=device):
        y_pred.extend(clf.predict(test_embeddings))

    f1 = f1_score(y_test, y_pred, average="weighted")
    # f1: 0.8255032451769995
    logging.info(f"f1: {f1}")

    joblib.dump(clf, 'sgd_classifier_model.pkl')

# IMDB Movie Reviews Sentiment Analysis Using Pre-Trained BERT Embeddings


## Project Overview
This project focuses on performing sentiment analysis of IMDB movie reviews using pre-trained BERT embeddings as input features. The primary goal is to classify reviews as either positive, negative or neutral while leveraging BERT's ability to capture semantic meaning. A SGDClassifier is trained on these embeddings to perform the classification task.

---

## Installation and Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/EgorEfimow/imdb-sentiment-analysis.git
   cd imdb-sentiment-analysis
   ```
2. **Set up a virtual environment**
    ```
    python -m venv .venv
    source .venv/bin/activate  # Linux/MacOS
    .venv\Scripts\activate     # Windows
    ```
3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```
4. **Create .env file:**
    ```
    PRS_BASE_PATH="https://www.imdb.com"
    PRS_CHART_PATH="https://www.imdb.com/chart/top/"
    PRS_REVIEWS_COUNT= Number of reviews to parse
    PRS_DATA_PATH= Where save dataset 
    MDL_MODEL_PATH= Path to bert model
    MDL_DATA_PATH= Where save processed dataset
    MDL_MODEL_NAME= Model name ("bert-base-uncased")
    ```
5. **Get dataset:** Parse IMDB website
    ```
    make generate_dataset
    ```
6. **Get model:** Download and save BERT weights and tokenizer
    ```
    make get_model
    ```
7. **Train model:**
    ```
    make train
    ```
8. **Run inference:**
    ```
    make inference
    ```

## Data

### Source Data
The data was obtained from the [IMDb Top 250 Movies chart](https://www.imdb.com/chart/top/), which lists the highest-rated movies based on user ratings.

### Data Acquisition
The movie reviews used in this project were scraped from a popular movie review platform. The process involves:

1. **Fetching Top Movies**  
The `get_top_movies` function scrapes the top-rated movies from a TOP 250 IMDB chart. It uses the `requests` library to fetch the page content and `BeautifulSoup` to parse and extract movie titles and their respective links.

2. **Scraping Reviews**  
Reviews for the fetched movies are collected using the `get_reviews` function, which employs the `playwright` library for dynamic web scraping. This ensures the extraction of full reviews, including those hidden behind spoiler tags.

    * Sanitizing URLs: A helper function adjusts the movie page URL to point directly to its review section.
    * Handling Dynamic Content: Using `playwright`, the script simulates user interactions, such as clicking "Load More" or revealing spoilers, to ensure all reviews are accessible.
    * Data Parsing: Reviews are parsed with `BeautifulSoup`, extracting elements like ratings, titles, and full review texts.
3. **Review Storage**  
Extracted reviews are stored in a custom `Review` collection class. Duplicate reviews are filtered out using a set of already-scraped titles.

4. **Asynchronous Processing**  
The script is designed to handle multiple movies concurrently using Python’s `asyncio`. Reviews are scraped in parallel for efficiency.

5. **Saving Data**  
All reviews are aggregated into a Pandas DataFrame and saved as a CSV file for further analysis. The data includes three fields:

    * rating: The numerical score assigned to the movie.
    * title: The title of the review.
    * review: The full text of the review.

### Data Preprocessing

1. Tokenization: Use a BERT tokenizer to convert text into token IDs compatible with the pre-trained BERT model.
2. Embedding Extraction: Extract embeddings using the BERT model for input to the SGDClassifier.

# Code structure

    root/
    │
    ├── app/
    │   ├── data/
    │   │   ├── raw/                 # Contains data after parsing
    │   │   └── processed/           # Preprocessed data files
    │   ├── models/
    │   │   └── sgd_classifier_model.pkl 
    │   ├── notebooks/
    │   ├── parser/
    │   │   ├── review/              # Review class implementation
    │   │   ├── generate_dataset.py  # Parse movies, parse reviews, build dataset
    │   │   ├── parse_movies.py      # Get TOP N movies titles and links
    │   │   ├── parse_reviews.py     # Get rating, title, review body
    │   │   └── config.py            # which environment variables to load
    │   ├── src/
    │   │   ├── get_model.py         # Load and save model   
    │   │   ├── train.py
    │   │   ├── inference.py         # Reads review from stdin
    │   │   ├── utils.py             # load_bert_components and get_embeddings
    │   │   └── config.py            # which environment variables to load
    ├── requirements.txt
    ├── Makefile
    └── README.md


## Results and Evaluation

The model achieved an F1 score of `0.8255 (weighted)` on the test set, demonstrating strong overall performance.

Upon evaluating the model on reviews from other movies, it was observed that it performs well in classifying `positive reviews` (ratings 8–10) and `neutral reviews` (ratings 4–7). However, the model struggles to accurately identify `negative reviews` (ratings 1–4), which may require further adjustments or additional training data for improvement.


https://www.imdb.com/review/rw0357564/?ref_=tturv_perm_35 rating 2/10, model says it is neutral (output [1])
class Review:
    def __init__(self):
        self.reviews = {
            "rating": [],
            "title": [],
            "review": []
        }

    def add_review(self, 
                   rating: int, 
                   title: str,
                   review_text: str):
        self.reviews["rating"].append(rating)
        self.reviews["title"].append(title)
        self.reviews["review"].append(review_text)

    def __len__(self):
        return len(self.reviews["rating"])
    
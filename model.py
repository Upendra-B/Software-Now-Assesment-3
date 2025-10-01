from transformers import pipeline

# ---------------------------
# Base Model
# ---------------------------
class BaseModel:
    def run(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

# ---------------------------
# Sentiment Analysis Model
# ---------------------------
class SentimentModel(BaseModel):
    def __init__(self):
        # small free model from Hugging Face
        self.pipe = pipeline("sentiment-analysis")

    def run(self, text: str):
        """Analyze sentiment of text"""
        result = self.pipe(text)
        return {"input": text, "result": result}

# ---------------------------
# Demo
# ---------------------------
if __name__ == "__main__":
    s_model = SentimentModel()
    print(s_model.run("I am very happy today!"))
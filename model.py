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
        self.pipe = pipeline("sentiment-analysis")

    def run(self, text: str):
        result = self.pipe(text)
        return {"input": text, "result": result}

# ---------------------------
# Text Generation Model
# ---------------------------
class TextGenModel(BaseModel):
    def __init__(self):
        # lightweight text generation model
        self.pipe = pipeline("text-generation", model="distilgpt2")

    def run(self, text: str):
        """Generate text continuation"""
        result = self.pipe(text, max_length=30, num_return_sequences=1)
        return {"input": text, "result": result}

# ---------------------------
# Demo
# ---------------------------
if __name__ == "__main__":
    # Sentiment analysis
    s_model = SentimentModel()
    print(s_model.run("I am very happy today!"))

    # Text generation
    g_model = TextGenModel()
    print(g_model.run("Once upon a time"))
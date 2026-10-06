from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

text = "Кошки любят спать"

vector = model.encode(text)

print(vector)
print(len(vector))
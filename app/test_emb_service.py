from app.core.embedding import create_embedding


text = "Кошки любят спать"

vector = create_embedding(text)

print(vector)
print("Размер:", len(vector))
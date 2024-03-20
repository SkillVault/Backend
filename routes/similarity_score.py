from transformers import BertTokenizer, BertModel
import torch
from pydantic import BaseModel
from scipy.spatial.distance import cosine
from fastapi import APIRouter

app = APIRouter()

class TextPair(BaseModel):
    text1: str
    text2: str

def bert_text_similarity(text1, text2, model_name='bert-base-uncased'):
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    inputs1 = tokenizer(text1, return_tensors='pt', padding=True, truncation=True, max_length=512)
    inputs2 = tokenizer(text2, return_tensors='pt', padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        outputs1 = model(**inputs1)
        outputs2 = model(**inputs2)

    embeddings1 = outputs1.last_hidden_state.mean(dim=1)
    embeddings2 = outputs2.last_hidden_state.mean(dim=1)

    similarity = 1 - cosine(embeddings1[0].numpy(), embeddings2[0].numpy())
    return similarity

@app.post("/")
async def compute_similarity(pair: TextPair):
    similarity = bert_text_similarity(pair.text1, pair.text2)
    return {"similarity": similarity}
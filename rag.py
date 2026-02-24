from sentence_transformers import SentenceTransformer
import re
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from apscheduler.schedulers.background import BackgroundScheduler
from sheets import get_sheet_data
from config import SYNC_CRON

model_name = 'all-MiniLM-L6-v2'
embed_model=SentenceTransformer(model_name)
vectordb = None

def load_vectordb():
    global vectordb
    print("Loading vector DB...")
    rows= get_sheet_data()
    texts=[]
    metadatas=[]
    for row in rows:
        combined_text=f"{row[1]} - {row[2]} - {row[3]} - {row[6]}"
        texts.append(combined_text)
        metadatas.append({
        "name": row[1],
        "type": row[0],
        "short_desc": row[2],
        "detailed_desc": row[3],
        "price": row[4],
        "link": row[5],
        "tags": row[6]
    })
    embeddings=embed_model.encode(texts)
    print("Example embedding for first row:\n", len(embeddings[0]))
    
    embedding_model = HuggingFaceEmbeddings(
    model_name=model_name,
    encode_kwargs={'normalize_embeddings': False})
    
    vectordb = Chroma(
    collection_name="offerings",
    embedding_function=embedding_model
)
    vectordb.add_texts(texts,metadatas=metadatas)
    print("✅ Vector DB Loaded Successfully")
    print(f"🔢 Total Products Stored: {vectordb._collection.count()}")

    
def refresh_vectordb():
    print("\n🔄 Refreshing vector store...")
    load_vectordb()
    print("✅ Vector store refreshed successfully!\n")


scheduler = BackgroundScheduler()

if SYNC_CRON == "hourly":
    scheduler.add_job(refresh_vectordb, 'interval', hours=1)
else:
    scheduler.add_job(refresh_vectordb, 'interval', minutes=30)

scheduler.start()

def search_vectordb(user_query,k=1):
    global vectordb
    if vectordb is None:
        print("\n Loading vector DB")
        load_vectordb()
    results=vectordb.similarity_search(user_query, k=k)
    return results


def extract_offered_price(user_query):
    numbers = re.findall(r"(\d+)%", user_query)
    if not numbers:
        return None
    return float(numbers[-1])   

def extract_offered_amount(user_query):
    match = re.search(r"(\d{3,7})", user_query.replace(',', ''))  
    if match:
        return float(match.group(1))
    return None


def calculate_bargain(product, user_input, user_data):
    try:
        actual_price = float(product.metadata["price"])
    except:
        return None

    max_attempts = 3
    max_bargain_percent = 10
    min_allowed_price = round(actual_price * (1 - max_bargain_percent / 100), 2)

    offered_percent = extract_offered_price(user_input)
    offered_amount = extract_offered_amount(user_input)

    if offered_percent is None and offered_amount is None:
        return None

    current_attempts = user_data.get("bargain_count", 0)

    if current_attempts >= max_attempts:
        user_data["last_final_price"] = min_allowed_price
        return {
            "status": "limit_reached",
            "final_price": min_allowed_price,
            "attempts": current_attempts
        }

    if offered_percent is not None:
        if offered_percent <= max_bargain_percent:
            final_price = round(actual_price * (1 - offered_percent / 100), 2)
            user_data["last_final_price"] = final_price
            return {
                "status": "accepted",
                "offered_percent": offered_percent,
                "final_price": final_price,
                "min_price": min_allowed_price
            }
        else:
            user_data["bargain_count"] = current_attempts + 1
            return {
                "status": "counter",
                "offered_percent": offered_percent,
                "counter_price": min_allowed_price,
                "min_price": min_allowed_price
            }

    if offered_amount is not None:
        if offered_amount >= min_allowed_price:
            user_data["last_final_price"] = offered_amount
            return {
                "status": "accepted",
                "offered_amount": offered_amount,
                "final_price": offered_amount,
                "min_price": min_allowed_price
            }
        else:
            user_data["bargain_count"] = current_attempts + 1
            return {
                "status": "counter",
                "offered_amount": offered_amount,
                "counter_price": min_allowed_price,
                "min_price": min_allowed_price
            }

    return None
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client.grocery_db
items_collection = db.items

class Item(BaseModel):
    name: str
    price: float
    quantity: int = 0

# Seed initial data if collection is empty
@app.on_event("startup")
async def seed_data():
    if items_collection.count_documents({}) == 0:
        initial_items = [
            {"name": "Carrot", "price": 1.5, "quantity": 10},
            {"name": "Broccoli", "price": 2.0, "quantity": 5},
            {"name": "Tomato", "price": 1.2, "quantity": 15},
        ]
        items_collection.insert_many(initial_items)

@app.get("/items")
async def get_items():
    items = []
    for item in items_collection.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return items

@app.post("/items")
async def add_item(item: Item):
    result = items_collection.insert_one(item.dict())
    return {"id": str(result.inserted_id)}

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    result = items_collection.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item updated"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = items_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}

@app.put("/items/{item_id}/quantity")
async def update_quantity(item_id: str, action: str):  # action: "add" or "remove"
    if action not in ["add", "remove"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    inc = 1 if action == "add" else -1
    result = items_collection.update_one({"_id": ObjectId(item_id)}, {"$inc": {"quantity": inc}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Quantity updated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
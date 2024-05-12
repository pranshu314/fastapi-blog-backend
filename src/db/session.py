import os
from typing import Any

from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI")
client: Any = MongoClient(mongo_uri)
db: Any = client.blog

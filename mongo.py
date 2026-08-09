# -----------------------------------------------
# 🔸 QUEENBOT Project
# 🔹 Developed by: Royalbot213
# 📅 Copyright © 2025 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love
# -----------------------------------------------

from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

config = Config()

print("Connecting to your Mongo Database...")
try:
    _mongo_async_ = AsyncIOMotorClient(config.MONGO_URL)
    mongodb = _mongo_async_.QUEENBOT
    print("Connected to your Mongo Database.")
except Exception as e:
    print(f"Failed to connect to your Mongo Database: {e}")
    exit()

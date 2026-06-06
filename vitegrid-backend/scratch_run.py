import sys
sys.modules['_wmi'] = None
print("1. Starting imports", flush=True)
import os
import dotenv
dotenv.load_dotenv()
print("2. dotenv loaded", flush=True)
import fastapi
print("3. fastapi imported", flush=True)
import sqlalchemy
print("4. sqlalchemy imported", flush=True)
import pydantic
print("5. pydantic imported", flush=True)
import PIL
print("6. PIL imported", flush=True)
print("7. Importing agent...", flush=True)
import agent
print("8. agent imported", flush=True)
print("9. Importing parser...", flush=True)
import parser
print("10. parser imported", flush=True)

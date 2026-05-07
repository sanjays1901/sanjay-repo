from db import engine

conn = engine.connect()

print("DB Connected Successfully!")

conn.close()
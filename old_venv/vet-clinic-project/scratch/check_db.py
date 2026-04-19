import sqlite3
import os

db_path = r'c:\Users\admin\Desktop\Project\old_venv\vet-clinic-project\backend\db.sqlite3'

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check for triggers and views
    cursor.execute("SELECT type, name FROM sqlite_master WHERE type IN ('trigger', 'view');")
    results = cursor.fetchall()
    
    if not results:
        print("ตอนนี้ยังไม่มี Trigger หรือ View (Procedure-like) ใน Database ของคุณครับ")
    else:
        print("พบรายการดังนี้:")
        for row in results:
            print(f"- {row[0]}: {row[1]}")
    
    conn.close()

import pyodbc

conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=.\SQLEXPRESS;'
    r'DATABASE=VetClinicDB;'
    r'Trusted_Connection=yes;'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM auth_user")
    rows = cursor.fetchall()
    
    if not rows:
        print("ตาราง auth_user ใน SQL Server ยังว่างเปล่าครับ (ไม่มีผู้ใช้ย้ายมา)")
    else:
        print("รายชื่อผู้ใช้ใน SQL Server:")
        for row in rows:
            print(f"- {row.username} ({row.email})")
            
    conn.close()
except Exception as e:
    print(f"Error: {e}")

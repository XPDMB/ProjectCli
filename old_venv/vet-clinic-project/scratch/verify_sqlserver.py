import pyodbc
import os

# Database connection details from settings
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=.\SQLEXPRESS;'
    r'DATABASE=VetClinicDB;'
    r'Trusted_Connection=yes;'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Check counts for some main tables
    tables = [
        'auth_user',
        'clinic_api_pet',
        'clinic_api_appointment'
    ]
    
    print("ตรวจสอบข้อมูลใน SQL Server (VetClinicDB):")
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"- ตาราง {table}: มีข้อมูล {count} แถว")
        except Exception as e:
            print(f"- ตาราง {table}: ไม่สามารถดึงข้อมูลได้ ({e})")
            
    conn.close()
except Exception as e:
    print(f"เชื่อมต่อ SQL Server ไม่ได้: {e}")

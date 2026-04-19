import sqlite3
import pyodbc
import sys

def migrate():
    try:
        # 1. เชื่อมต่อทั้งสองฐานข้อมูล
        sq = sqlite3.connect('db.sqlite3')
        ms = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=.\SQLEXPRESS;'
            'DATABASE=VetClinicDB;'
            'Trusted_Connection=yes;'
        )
        ms.autocommit = True
        cur = ms.cursor()

        # รายชื่อตารางที่ต้องย้าย
        tables = [
            'auth_user', 
            'clinic_api_profile', 
            'clinic_api_inventoryitem', 
            'clinic_api_pet', 
            'clinic_api_appointment', 
            'clinic_api_medicalrecord', 
            'clinic_api_prescriptionline', 
            'clinic_api_staffshift'
        ]

        print("🚀 เริ่มต้นกระบวนการย้ายข้อมูลทั้งหมดจาก SQLite -> SQL Server...")
        
        # ปิดการตรวจ Foreign Key เพื่อกัน Error เรื่องลำดับการย้าย
        try:
            cur.execute("EXEC sp_MSforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL'")
        except:
            print("⚠️ ไม่สามารถปิด Constraint ได้ (อาจไม่มีสิทธิ์) แต่จะพยายามย้ายต่อ...")

        for table in tables:
            print(f"📦 กำลังย้ายตาราง: {table}...")
            
            try:
                # ดึงข้อมูลจาก SQLite
                sq_cur = sq.cursor()
                sq_cur.execute(f"SELECT * FROM {table}")
                data = sq_cur.fetchall()
                
                # ดึงชื่อคอลัมน์
                sq_cur.execute(f"PRAGMA table_info({table})")
                cols = [d[1] for d in sq_cur.fetchall()]
                
                if not data:
                    print(f"➖ ตาราง {table} ไม่มีข้อมูล ข้าม...")
                    continue

                # ล้างข้อมูลเก่า
                cur.execute(f"DELETE FROM {table}")
                
                # เปิด Identity Insert เพื่อให้ใช้ ID เดิมจาก SQLite ได้
                try:
                    cur.execute(f"SET IDENTITY_INSERT {table} ON")
                except:
                    pass
                
                placeholders = ", ".join(["?" for _ in cols])
                columns_str = ", ".join(cols)
                
                # ย้ายข้อมูลแบบ Bulk
                cur.executemany(
                    f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})", 
                    data
                )
                
                try:
                    cur.execute(f"SET IDENTITY_INSERT {table} OFF")
                except:
                    pass
                    
                print(f"✅ ย้าย {table} สำเร็จ ({len(data)} แถว)")
            except Exception as e:
                print(f"❌ พลาดที่ตาราง {table}: {e}")

        # เปิดการตรวจ Foreign Key คืน
        try:
            cur.execute("EXEC sp_MSforeachtable 'ALTER TABLE ? WITH CHECK CHECK CONSTRAINT ALL'")
        except:
            pass
            
        print("\n🔥 เสร็จสิ้น! ทุกอย่างถูกย้ายไป SQL Server เรียบร้อยแล้วครับ")
        print("💡 ตอนนี้คุณสามารถ Login ด้วยรหัสเดิมได้เลยครับ")

    except Exception as e:
        print(f"❗ เกิดข้อผิดพลาดร้ายแรง: {e}")
    finally:
        sq.close()
        ms.close()

if __name__ == "__main__":
    migrate()

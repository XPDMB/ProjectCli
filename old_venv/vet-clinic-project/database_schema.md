# โครงสร้างฐานข้อมูลระบบคลินิกสัตวแพทย์ใจดี (Vet Clinic DB Schema)

ระบบจะแปลงโค้ดจาก `models.py` ของ Django ให้กลายเป็น "ตาราง (Tables)" ในฐานข้อมูล `db.sqlite3` โดยอัตโนมัติ 
นี่คือตารางหลักแต่ละตัวที่ถูกสร้างขึ้นในระบบพร้อมคำอธิบายการทำงานครับ:

---

## 1. ตารางตัวตนและผู้ใช้งาน (User & Profile)
Django มีตาราง `auth_user` เป็นค่าเริ่มต้นสำหรับจัดการระบบ Login ส่วนเราสร้าง `Profile` มาขยายเพิ่มครับ

### 👩‍⚕️ Table: `clinic_api_profile` (ข้อมูลผู้ใช้งานเพิ่มเติม)
| ชื่อคอลัมน์ (Column) | ชนิดข้อมูล (Data Type) | หน้าที่ / คำอธิบาย |
| :--- | :--- | :--- |
| `id` | Integer | รหัสเฉพาะของโปรไฟล์ (Primary Key) |
| `user_id` | Integer | รหัสอ้างอิงไปที่ระบบความปลอดภัยหลัก (Foreign Key ไปโต๊ะ User) |
| `display_name` | String | ชื่อ-นามสกุล ที่ใช้แสดงในเว็บหลัก |
| `phone` | String | เบอร์โทรศัพท์สำหรับติดต่อ |
| `role` | String | สถานะ: `customer` (ลูกค้า), `vet` (สัตวแพทย์), `assistant` (ผู้ช่วย) |

---

## 2. ตารางเกี่ยวกับลูกค้าและสัตว์เลี้ยง (Customers & Pets)

### 🐾 Table: `clinic_api_pet` (ข้อมูลสัตว์เลี้ยง)
| ชื่อคอลัมน์ (Column) | ชนิดข้อมูล (Data Type) | หน้าที่ / คำอธิบาย |
| :--- | :--- | :--- |
| `id` | Integer | รหัสเฉพาะของสัตว์เลี้ยง (Primary Key) |
| `owner_id` | Integer | รหัสอ้างอิงใครเป็นเจ้าของ (Foreign Key ไปตาราง User) |
| `name` | String | ชื่อสัตว์เลี้ยง (เช่น ถุงทอง) |
| `species` | String | ประเภทของสัตว์ (สุนัข, แมว, นก, ฯลฯ) |
| `breed` | String | สายพันธุ์ |
| `birth_date` | Date | วันเกิดของน้อง (ใช้คำนวณอายุ) |
| `sex` | String | เพศ |
| `is_neutered`| Boolean | ทำหมันแล้วหรือไม่ (True/False) |
| `allergies` | Text | ข้อมูลประวัติการแพ้ยา |

---

## 3. ตารางคลินิกและการรักษา (Clinic & Treatments)

### 📅 Table: `clinic_api_appointment` (ตารางคิวนัดหมาย)
| ชื่อคอลัมน์ (Column) | ชนิดข้อมูล (Data Type) | หน้าที่ / คำอธิบาย |
| :--- | :--- | :--- |
| `id` | Integer | รหัสการนัดหมาย (Primary Key) |
| `pet_id` | Integer | รหัสอ้างอิงว่าน้องตัวไหนมา (Foreign Key ไปตาราง Pet) |
| `scheduled_at` | DateTime | วันที่และเวลาที่นัดหมายมาตรวจ |
| `status` | String | สถานะคิว: `pending`, `confirmed`, `waiting`, `completed`, `cancelled` |
| `reason` | String | อาการเบื้องต้น / สาเหตุที่มารักษา |

### 🩺 Table: `clinic_api_medicalrecord` (ตารางประวัติการรักษา/ใบเสร็จ)
| ชื่อคอลัมน์ (Column) | ชนิดข้อมูล (Data Type) | หน้าที่ / คำอธิบาย |
| :--- | :--- | :--- |
| `id` | Integer | รหัสบันทึกการรักษา (Primary Key) |
| `appointment_id`| Integer | รหัสคิวที่ตรวจเสร็จแล้ว (Foreign Key 1-to-1 ไปตาราง Appointment) |
| `symptoms` | Text | อาการโดยละเอียดที่หมอตรวจพบ |
| `diagnosis` | Text | ผลการวินิจฉัยโรค (คุณหมอเป็นคนกรอก) |
| `weight` | Decimal | น้ำหนักตอนมาชั่งก่อนตรวจ |
| `temperature` | Decimal | อุณหภูมิร่างกาย (ไข้) |
| `exam_fee` | Decimal | ค่าใช้จ่ายเฉพาะค่าตรวจ (ไม่รวมค่ายา) |
| `is_paid` | Boolean | จ่ายเงินหรือยัง? (ตัดจบเคส) |
| `total_amount` | Decimal | สรุปยอดเงินรวมทั้งหมดในบิลนี้ (ค่ารักษา + ค่ายา) |

---

## 4. ตารางคลังยาและรายการสั่งจ่าย (Inventory & Prescription)

### 💊 Table: `clinic_api_inventoryitem` (คลังยา/สินค้า)
| ชื่อคอลัมน์ (Column) | ชนิดข้อมูล (Data Type) | หน้าที่ / คำอธิบาย |
| :--- | :--- | :--- |
| `id` | Integer | รหัสรายการ (Primary Key) |
| `item_code` | String | รหัสสินค้าหน้าร้าน (บาร์โค้ด) |
| `name` | String | ชื่อยา หรือชื่อสินค้า |
| `category` | String | หมวดหมู่ (`medicine`, `vaccine`, `food`, ฯลฯ) |
| `stock_quantity`| Integer | **จำนวนคงคลัง (Stock เหลือเท่าไหร่)** |
| `price` | Decimal | ราคาขายปลีกต่อหน่วย (Customer Price) |
| `cost_price` | Decimal | ราคาต้นทุน (ใช้ดูตอนสรุปบัญชีการเงินรายงานรายเดือน) |

### 📝 Table: `clinic_api_prescriptionline` (รายการสั่งจ่ายยารายชิ้น)
| ชื่อคอลัมน์ (Column) | ชนิดข้อมูล (Data Type) | หน้าที่ / คำอธิบาย |
| :--- | :--- | :--- |
| `id` | Integer | รหัสรายการย่อยในบิล (Primary Key) |
| `medical_record_id`| Integer | ผูกบิลใบนี้เข้ากับ "ใบสั่งแพทย์/ใบเสร็จ" ใบไหน (Foreign Key) |
| `inventory_item_id`| Integer | ผูกไปที่รหัสยาว่าหยิบยาขวดไหนไปจ่าย (Foreign Key) |
| `quantity` | Integer | **จำนวนชิ้นที่จ่าย (เช่น จ่าย 2 ขวด)** |
| `dosage` | String | วิธีใช้ให้เจ้าของรู้ (เช่น ทาน 1 เม็ดเช้า-เย็น) |
| `unit_price` | Decimal | ราคาขายถูกบันทึกแช่แข็งไว้ ณ วันที่จ่าย |

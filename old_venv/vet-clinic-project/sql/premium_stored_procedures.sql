-- Premium Edition Stored Procedures
-- สำรับงานระบบคลินิกสัตวแพทย์ (KindVet)
-- ออกแบบสำหรับรันบน Microsoft SQL Server

USE VetClinicDB;
GO

-- =============================================
-- 1. สตอร์พรอซีเจอร์สำหรับตัดสต็อกสินค้าและยาอัตโนมัติ
-- =============================================
CREATE OR ALTER PROCEDURE sp_UpdateInventory
    @inventory_id INT,
    @quantity_deducted INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- อัปเดตเพื่อลดจำนวนสต็อกลงตามจำนวนที่ระบุ
    UPDATE clinic_api_inventoryitem
    SET stock_quantity = CASE 
        WHEN stock_quantity - @quantity_deducted < 0 THEN 0 
        ELSE stock_quantity - @quantity_deducted 
    END
    WHERE id = @inventory_id;
    
    -- สามารถเพิ่ม Logic บันทึกประวัติการตัดสต็อก (Transaction Log) ลงตารางอื่นได้ด้วย
END
GO

-- =============================================
-- 2. สตอร์พรอซีเจอร์สำหรับคำนวณและสรุปยอดการเงินแบบรวดเร็ว
-- =============================================
CREATE OR ALTER PROCEDURE sp_GetFinancialReport
    @start_date DATETIME,
    @end_date DATETIME
AS
BEGIN
    SET NOCOUNT ON;
    
    -- คำนวณสรุปยอดรายได้จากตาราง MedicalRecord 
    -- (ทำงานได้รวดเร็วกว่าการดึงข้อมูลทั้งหมดไปวนลูปใน Python)
    SELECT 
        COUNT(id) AS total_patients,
        ISNULL(SUM(total_amount), 0) AS gross_revenue
    FROM clinic_api_medicalrecord
    WHERE is_paid = 1 AND created_at BETWEEN @start_date AND @end_date;
END
GO

-- =============================================
-- 3. ตรีเกอร์ (Trigger) เพื่อช่วยปรับสถานะคิวอัตโนมัติ (Bonus)
-- =============================================
CREATE OR ALTER TRIGGER trg_CompleteAppointment
ON clinic_api_medicalrecord
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    -- เมื่อบันทึกการตรวจรักษา (MedicalRecord) ถูกสร้างหรือจ่ายเงินแล้ว 
    -- ให้อัปเดตสถานะในตาราง Appointment เป็น 'completed' หรือ 'payment'
    UPDATE a
    SET a.status = CASE 
        WHEN i.is_paid = 1 THEN 'completed' 
        ELSE 'payment' 
    END
    FROM clinic_api_appointment a
    INNER JOIN inserted i ON a.id = i.appointment_id;
END
GO

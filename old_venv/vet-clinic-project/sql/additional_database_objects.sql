-- =============================================
-- 4. วิว (View) สำหรับดูคิวนัดหมายของวันนี้แบบรวดเร็ว
-- =============================================
USE VetClinicDB;
GO

CREATE OR ALTER VIEW vw_TodayAppointments AS
SELECT a.id, p.name AS PetName, a.scheduled_at, a.status, a.reason
FROM clinic_api_appointment a
JOIN clinic_api_pet p ON a.pet_id = p.id
WHERE CAST(a.scheduled_at AS DATE) = CAST(GETDATE() AS DATE);
GO

-- =============================================
-- 5. ฟังก์ชัน (Function) คำนวณอายุสัตว์เลี้ยง
-- =============================================
CREATE OR ALTER FUNCTION fn_CalculatePetAge (@BirthDate DATE)
RETURNS INT
AS
BEGIN
    DECLARE @Age INT;
    SET @Age = DATEDIFF(YEAR, @BirthDate, GETDATE());
    RETURN @Age;
END;
GO

-- =============================================
-- 6. การสร้างผู้ใช้งานฐานข้อมูล (Create User)
-- =============================================
-- หมายเหตุ: การสร้าง Login ต้องทำใน Master DB ดังนั้นควรนำโค้ดส่วนนี้ไปรันแยกต่างหาก
/*
USE master;
GO
CREATE LOGIN ClinicAdmin WITH PASSWORD = 'StrongPassword123!';
GO
*/

-- อนุญาต User ให้เข้าใช้งานและเขียนข้อมูลใน VetClinicDB ได้เต็มรูปแบบ
USE VetClinicDB;
GO
CREATE USER ClinicAdmin FOR LOGIN ClinicAdmin;
ALTER ROLE db_owner ADD MEMBER ClinicAdmin;
GO

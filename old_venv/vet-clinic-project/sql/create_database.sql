-- สร้างฐานข้อมูลบน Microsoft SQL Server (รันใน SSMS หรือ sqlcmd ก่อน migrate)
-- จากนั้นตั้งค่า environment: USE_SQL_SERVER=1, DB_NAME=VetClinicDB, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
-- และ pip install mssql-django pyodbc

IF DB_ID(N'VetClinicDB') IS NULL
BEGIN
    CREATE DATABASE VetClinicDB;
END
GO

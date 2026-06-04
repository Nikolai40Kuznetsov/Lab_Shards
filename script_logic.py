import pymssql
import credits as cr

conn = pymssql.connect(cr.server, cr.user, cr.password, cr.db)
cursor = conn.cursor()

cursor.execute ("""
    USE UUTW_66_LAB_1
    CREATE TABLE Person(  
    id INT IDENTITY(1,1) PRIMARY KEY,
    Surname NVARCHAR (20),
    Name NVARCHAR (20),
    Middle_Name NVARCHAR (20),
    Age INT,
    Sex NVARCHAR (1),
    ) 
                
    DECLARE @age INT, @sex NVARCHAR (1)
                
    Select @age = -19 from Person
    Select @sex = 'Х' from Person
                
    if @age <= 0 or @age >= 150
        BEGIN
        PRINT 'Неверное значение в поле Age'
        END;
    ELSE
        BEGIN
        CASE @sex
            WHEN 'М' THEN INSERT INTO Person VALUES ('Карась', 'Илья', 'Гена', @age, @sex)
            WHEN 'Ж' THEN INSERT INTO Person VALUES ('Карась', 'Илья', 'Гена', @age, @sex)
            ELSE PRINT 'Неверное значение в поле Sex'
        END
        END        
    SELECT * FROM Person   
"""
)
print(cursor.fetchall())
conn.commit()
conn.close()


import pymssql
import credits as cr

conn = pymssql.connect(cr.server, cr.user, cr.password, cr.db)
cursor = conn.cursor()

cursor.execute (
"""
CREATE DATABASE User_Actions;

USE User_Actions;

CREATE TABLE User_Logs(
    id uniqueidentifier DEFAULT NEWID() PRIMARY KEY,
    username varchar(255) NOT NULL,
    user_action varchar(50) NOT NULL,
    action_date date NOT NULL,
    action_time time NOT NULL,
    action_result varchar(50) NOT NULL
);

SET NOCOUNT ON;

WITH Tally AS (
    SELECT TOP 1000000
        rn = ROW_NUMBER() OVER (ORDER BY (SELECT NULL))
    FROM (VALUES (1),(1),(1),(1),(1),(1),(1),(1),(1),(1)) v1(n)
    CROSS JOIN (VALUES (1),(1),(1),(1),(1),(1),(1),(1),(1),(1)) v2(n)
    CROSS JOIN (VALUES (1),(1),(1),(1),(1),(1),(1),(1),(1),(1)) v3(n)
    CROSS JOIN (VALUES (1),(1),(1),(1),(1),(1),(1),(1),(1),(1)) v4(n)
    CROSS JOIN (VALUES (1),(1),(1),(1),(1),(1),(1),(1),(1),(1)) v5(n)
    CROSS JOIN (VALUES (1),(1),(1),(1),(1),(1),(1),(1),(1),(1)) v6(n)
),
Randomized AS (
    SELECT
        rn,
        rand_val = ABS(CHECKSUM(NEWID()))
    FROM Tally
)
INSERT INTO User_Logs WITH (TABLOCK) (username, user_action, action_date, action_time, action_result)
SELECT
    'user_' + RIGHT('00000' + CAST(rand_val % 99999 AS varchar(5)), 5),
    
    CASE rand_val % 8
        WHEN 0 THEN 'LOGIN'      WHEN 1 THEN 'LOGOUT'
        WHEN 2 THEN 'UPDATE'     WHEN 3 THEN 'DELETE'
        WHEN 4 THEN 'VIEW'       WHEN 5 THEN 'CREATE'
        WHEN 6 THEN 'EXPORT'     WHEN 7 THEN 'IMPORT'
        ELSE 'UNKNOWN'
    END,
    
    DATEADD(day, rand_val % 365, '2025-01-01'),
    
    DATEADD(second, rand_val % 86400, CAST('00:00:00' AS time)),
    
    CASE rand_val % 5
        WHEN 0 THEN 'SUCCESS'        WHEN 1 THEN 'FAILED'
        WHEN 2 THEN 'PENDING'        WHEN 3 THEN 'TIMEOUT'
        WHEN 4 THEN 'ACCESS_DENIED'
        ELSE 'ERROR'
    END
FROM Randomized;

SELECT * FROM User_Logs ORDER BY action_date;

--DROP TABLE User_Logs;
"""
)
create table Logs(
	id int identity(100000000,1),
	username text not null,
	user_action text not null,
	action_date date not null,
	action_time time not null,
	action_result text not null
)

SET NOCOUNT ON;

-- Генерация 1 000 000 записей
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
        -- Генерируем одно случайное число на строку и фиксируем его
        rand_val = ABS(CHECKSUM(NEWID()))
    FROM Tally
)
INSERT INTO Logs WITH (TABLOCK) (username, user_action, action_date, action_time, action_result)
SELECT
    -- username: user_00001 ... user_99999
    'user_' + RIGHT('00000' + CAST(rand_val % 99999 AS VARCHAR(5)), 5),
    
    -- user_action: используем остаток от деления того же rand_val
    CASE rand_val % 8
        WHEN 0 THEN 'LOGIN'      WHEN 1 THEN 'LOGOUT'
        WHEN 2 THEN 'UPDATE'     WHEN 3 THEN 'DELETE'
        WHEN 4 THEN 'VIEW'       WHEN 5 THEN 'CREATE'
        WHEN 6 THEN 'EXPORT'     WHEN 7 THEN 'IMPORT'
        ELSE 'UNKNOWN'           -- Страховка от NULL, хотя при %8 и ABS она не нужна
    END,
    
    -- action_date: случайная дата за ~3 года (начиная с 2023-01-01)
    DATEADD(DAY, rand_val % 1096, '2023-01-01'),
    
    -- action_time: случайное время суток (0-86399 секунд)
    DATEADD(SECOND, rand_val % 86400, CAST('00:00:00' AS TIME)),
    
    -- action_result: случайный статус
    CASE rand_val % 5
        WHEN 0 THEN 'SUCCESS'        WHEN 1 THEN 'FAILED'
        WHEN 2 THEN 'PENDING'        WHEN 3 THEN 'TIMEOUT'
        WHEN 4 THEN 'ACCESS_DENIED'
        ELSE 'ERROR'                 -- Страховка от NULL
    END
FROM Randomized;

select * from Logs
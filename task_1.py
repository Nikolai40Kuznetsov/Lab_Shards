import pymssql
import credits as cr

conn = pymssql.connect(cr.server, cr.user, cr.password, cr.db)
cursor = conn.cursor()

cursor.execute ("""
-- Задание 1
CREATE DATABASE User_Actions

create table User_Logs(
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
INSERT INTO User_Logs WITH (TABLOCK) (username, user_action, action_date, action_time, action_result)
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
    
    -- action_date: случайная дата за 1 год (начиная с 2025-01-01)
    DATEADD(DAY, rand_val % 364, '2025-01-01'),
    
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

select * from User_Logs


#zadanie 2

USE User_Actions;

-- Шаг 2: Анализ временных рамок исходных данных
-- Находим самую раннюю дату логов в таблице User_Logs
SELECT MIN(action_date) FROM User_Logs;
-- Находим самую позднюю дату логов в таблице User_Logs
SELECT MAX(action_date) FROM User_Logs;


-- Шаг 3: Подготовка физической структуры БД Sector
-- Добавляем в базу данных новую логическую группу файлов с именем 'Sector_frag'
ALTER DATABASE User_Actions ADD FILEGROUP User_Actions_frag;
GO

-- Физически привязываем к созданной группе новый файл данных (.ndf) на диске D
ALTER DATABASE User_Actions ADD FILE(
	NAME = 'User_Actions_frag_2023',
	FILENAME = 'D:\SQL\User_Actions_frag_2023.ndf') TO FILEGROUP User_Actions_frag;
GO


-- Шаг 4: Создание функции секционирования
-- Определяем правила деления данных по типу "date".
-- RANGE RIGHT означает, что граничное значение входит в правую (следующую) секцию.
CREATE PARTITION FUNCTION pf_User_Actions_year(date)
AS RANGE RIGHT FOR VALUES (
    '2026-02-01', '2026-03-01', '2026-04-01', '2026-05-01', 
    '2026-06-01', '2026-07-01', '2026-08-01', '2026-09-01', 
    '2026-10-01', '2026-11-01', '2026-12-01'
);
GO


-- Шаг 5: Создание схемы секционирования
-- Связываем функцию секционирования с физическими группами файлов.
-- Так как указано 12 раза 'User_Actions_frag', все 12 секции будут физически лежать в одном месте.
CREATE PARTITION SCHEME ps_User_Actions_frag
AS PARTITION pf_User_Actions_year TO (
    User_Actions_frag, 
    User_Actions_frag,
	User_Actions_frag, 
    User_Actions_frag,
	User_Actions_frag, 
    User_Actions_frag,
	User_Actions_frag, 
    User_Actions_frag,
	User_Actions_frag, 
    User_Actions_frag, 
	User_Actions_frag,
    User_Actions_frag
);
GO


-- Шаг 6: Создание секционированной таблицы
CREATE TABLE User_Logs_frag(
	id INT IDENTITY(100000000,1),
	username TEXT NOT NULL,       
	user_action TEXT NOT NULL,
	action_date DATE NOT NULL,
	action_time TIME NOT NULL,
	action_result TEXT NOT NULL,

	-- ВАЖНО: Ключ секционирования (action_date) ОБЯЗАТЕЛЬНО должен входить в состав составного ПК
	CONSTRAINT pk_logs PRIMARY KEY CLUSTERED (id, action_date)
) ON ps_User_Actions_frag(action_date); -- Указываем схему и колонку, по которой делить таблицу
GO


-- Шаг 7: Проверка пустой таблицы
-- Ожидаемый результат: 0 (таблица только что создана)
SELECT COUNT(*) FROM User_Logs_frag;


-- Шаг 8: Миграция данных
-- Копируем все записи из старой таблицы 'Logs' в новую секционированную 'Logs_frag'.
-- SQL Server автоматически разложит строки по секциям на основе даты action_date.
INSERT INTO User_Logs_frag (username, user_action, action_date, action_time, action_result) 
	SELECT username, user_action, action_date, action_time, action_result FROM User_Logs;


-- Шаг 9: Проверка после вставки
-- Показывает общее количество успешно перенесенных строк
SELECT COUNT(*) FROM User_Logs_frag;


-- Шаг 10: Контрольное чтение
SELECT * FROM User_Logs;      -- Просмотр исходных данных
SELECT * FROM User_Logs_frag; -- Просмотр новых секционированных данных
                """
)
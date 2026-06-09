import pymssql
import credits as cr

conn = pymssql.connect(cr.server, cr.user, cr.password, cr.db)
cursor = conn.cursor()

cursor.execute (
"""
USE User_Actions;

CREATE PARTITION FUNCTION pf_UserLogsPart_Monthly (DATE)
AS RANGE RIGHT FOR VALUES (
    '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01',
    '2025-06-01', '2025-07-01', '2025-08-01', '2025-09-01',
    '2025-10-01', '2025-11-01', '2025-12-01'
);

CREATE PARTITION SCHEME ps_UserLogsPart_Monthly
AS PARTITION pf_UserLogsPart_Monthly
ALL TO ([PRIMARY]);

CREATE TABLE User_Logs_Partitioned (
    id uniqueidentifier DEFAULT NEWID(),
    username varchar(255) NOT NULL,
    user_action varchar(50) NOT NULL,
    action_date date NOT NULL,
    action_time time NOT NULL,
    action_result varchar(50) NOT NULL,
    CONSTRAINT PK_User_Logs_Partitioned PRIMARY KEY NONCLUSTERED (id, action_date)
) 
ON ps_UserLogsPart_Monthly(action_date);

CREATE CLUSTERED INDEX IX_User_Logs_Partitioned_ActionDate 
ON User_Logs_Partitioned (action_date, id)
ON ps_UserLogsPart_Monthly(action_date);

SET NOCOUNT ON;

INSERT INTO User_Logs_Partitioned WITH (TABLOCK) 
    (id, username, user_action, action_date, action_time, action_result)
SELECT 
    id, username, user_action, action_date, action_time, action_result
FROM User_Logs;

SELECT 
    $PARTITION.pf_UserLogsPart_Monthly(action_date) AS PartitionNumber,
    YEAR(action_date) AS [Year],
    MONTH(action_date) AS [Month],
    COUNT(*) AS [RowCount],
    MIN(action_date) AS MinDate,
    MAX(action_date) AS MaxDate
FROM User_Logs_Partitioned
GROUP BY 
    $PARTITION.pf_UserLogsPart_Monthly(action_date),
    YEAR(action_date),
    MONTH(action_date)
ORDER BY PartitionNumber;
"""
)
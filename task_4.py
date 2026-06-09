import pymssql
import credits as cr

conn = pymssql.connect(cr.server, cr.user, cr.password, cr.db)
cursor = conn.cursor()

cursor.execute (
"""
use master
backup database [User_Actions] 
to disk = 'D:\User_Actions_backup.bak' 
with format, 
medianame = 'SQL_Server_Backup', 
name = 'Полный бэкап базы данных';

use master;
go

create or alter procedure sp_RestoreDatabaseFromBackup
    @BackupFilePath nvarchar(512),
    @NewDBName nvarchar(128),
    @TargetFilesDir nvarchar(512)
as
begin
    set nocount on;

    if right(@TargetFilesDir, 1) <> '\' 
        set @TargetFilesDir = @TargetFilesDir + '\';

    declare @LogicalDataName nvarchar(128);
    declare @LogicalLogName nvarchar(128);
    declare @LogicalDataPath nvarchar(512);
    declare @LogicalLogPath nvarchar(512);

    create table #FileList (
        LogicalName nvarchar(128), PhysicalName nvarchar(260), Type char(1),
        FileGroupName nvarchar(128), Size numeric(20,0), MaxSize numeric(20,0),
        FileId bigint, CreateLSN numeric(25,0), DropLSN numeric(25,0),
        UniqueId uniqueidentifier, ReadOnlyLSN numeric(25,0), ReadWriteLSN numeric(25,0),
        BackupSizeInBytes bigint, SourceBlockSize int, FileGroupId int,
        LogGroupGuid uniqueidentifier, DifferentialBaseLsn numeric(25,0),
        DifferentialBaseGuid uniqueidentifier, IsReadOnly bit, IsPresent bit,
        TDEThumbprint varbinary(32), SnapshotUrl nvarchar(360)
    );

    declare @SqlList nvarchar(max) = 'RESTORE FILELISTONLY FROM DISK = ''' + @BackupFilePath + '''';
    insert into #FileList
    exec sp_executesql @SqlList;

    select top 1 @LogicalDataName = LogicalName from #FileList where Type = 'D' order by FileId;
    select top 1 @LogicalLogName = LogicalName from #FileList where Type = 'L' order by FileId;

    drop table #FileList;

    if @LogicalDataName is null or @LogicalLogName is null
    begin
        raiserror('Не удалось прочитать логические имена файлов из указанного бэкапа.', 16, 1);
        return;
    end

    set @LogicalDataPath = @TargetFilesDir + @NewDBName + '.mdf';
    set @LogicalLogPath = @TargetFilesDir + @NewDBName + '_log.ldf';

    if exists (select name from sys.databases where name = @NewDBName)
    begin
        declare @SqlKill nvarchar(max) = 'ALTER DATABASE [' + @NewDBName + '] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;';
        exec sp_executesql @SqlKill;
    end

    declare @SqlRestore nvarchar(max);
    set @SqlRestore = 'RESTORE DATABASE [' + @NewDBName + '] ' +
                      'FROM DISK = ''' + @BackupFilePath + ''' ' +
                      'WITH MOVE ''' + @LogicalDataName + ''' TO ''' + @LogicalDataPath + ''', ' +
                      'MOVE ''' + @LogicalLogName + ''' TO ''' + @LogicalLogPath + ''', ' +
                      'REPLACE, STATS = 10;';
    
    exec sp_executesql @SqlRestore;

    declare @SqlMultiUser nvarchar(max) = 'ALTER DATABASE [' + @NewDBName + '] SET MULTI_USER;';
    exec sp_executesql @SqlMultiUser;

    print 'База данных ' + @NewDBName + ' успешно восстановлена.';
end;
go

exec [master].[dbo].[sp_RestoreDatabaseFromBackup]
    @BackupFilePath = 'D:\User_Actions_backup.bak',
    @NewDBName = 'User_Actions_backupDB',
    @TargetFilesDir = 'D:\SQL_Data\';
"""
)
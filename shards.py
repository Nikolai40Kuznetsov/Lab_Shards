from sqlalchemy.orm import Session
from sqlalchemy import Column, Date, Integer, String, Time, create_engine, text
from sqlalchemy.orm import DeclarativeBase

database_url_1 = r"mssql+pyodbc://lol:123456789aA@15-2-441-1-PREP/Sector?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"
database_url_2 = r"mssql+pyodbc://lol:123456789aA@15-2-441-1-PREP/Sector2?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"
database_url_3 = r"mssql+pyodbc://lol:123456789aA@15-2-441-1-PREP/Sector3?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"
database_url_4 = r"mssql+pyodbc://lol:123456789aA@15-2-441-1-PREP/Sector4?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"
database_url_5 = r"mssql+pyodbc://lol:123456789aA@15-2-441-1-PREP/Sector5?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"
database_url_6 = r"mssql+pyodbc://lol:123456789aA@15-2-441-1-PREP/Sector6?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"
database_url_7 = r"mssql+pyodbc://lol:123456789aA@15-2-441-1-PREP/Sector7?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"
database_url_8 = r"mssql+pyodbc://lol:123456789aA@15-2-441-1-PREP/Sector8?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"
database_url_9 = r"mssql+pyodbc://lol:123456789aA@15-2-441-1-PREP/Sector9?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"
database_url_10 = r"mssql+pyodbc://lol:123456789aA@15-2-441-1-PREP/Sector10?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"

engine1 = create_engine(database_url_1)
engine2 = create_engine(database_url_2)
engine3 = create_engine(database_url_3)
engine4 = create_engine(database_url_4)
engine5 = create_engine(database_url_5)
engine6 = create_engine(database_url_6)
engine7 = create_engine(database_url_7)
engine8 = create_engine(database_url_8)
engine9 = create_engine(database_url_9)
engine10 = create_engine(database_url_10)

class Base(DeclarativeBase):
    pass

class Logs(Base):
    __tablename__ = "Logs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    user_action = Column(String, nullable=False)
    action_date = Column(Date, nullable=False)
    action_time = Column(Time, nullable=False)
    action_result = Column(String, nullable=False)

Base.metadata.create_all(bind=engine1)
Base.metadata.create_all(bind=engine2)


def inputt(engine:str, input_data:Logs):
    with Session(autoflush=False, bind=engine) as db:
        db.add(input_data)
        db.commit()

def sendto_shard(input_data:Logs, memory):
    if memory:
        inputt(engine=engine1, input_data = input_data)
        memory = False
        print("bd1")
    else:
        inputt(engine=engine2, input_data = input_data)
        memory = True
        print("bd2")
    return memory


def main():
    input_data = Logs(username = "asd", user_action = "DELETE", action_date = "2023-01-01", action_time = "00:00:00", action_result = "OK")
    memory = True
    memory = sendto_shard(input_data, memory=memory)
    memory = sendto_shard(input_data, memory=memory)

if __name__ == "__main__":
    main()
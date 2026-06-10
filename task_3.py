from sqlalchemy.orm import Session
from sqlalchemy import Column, Date, Integer, String, Time, create_engine, text
from sqlalchemy.orm import DeclarativeBase
from credits import user, password, server, db


database_url = f"mssql+pyodbc://{user}:{password}@{server}/{db}?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=No&TrustServerCertificate=yes&PersistSecurityInfo=no&Pooling=no&MultipleActiveResultSets=no"

engine1 = create_engine(database_url)
engine2 = create_engine(database_url)
engine3 = create_engine(database_url)
engine4 = create_engine(database_url)
engine5 = create_engine(database_url)
engine6 = create_engine(database_url)
engine7 = create_engine(database_url)
engine8 = create_engine(database_url)
engine9 = create_engine(database_url)
engine10 = create_engine(database_url)
engine11 = create_engine(database_url)
engine12 = create_engine(database_url)

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
Base.metadata.create_all(bind=engine3)
Base.metadata.create_all(bind=engine4)
Base.metadata.create_all(bind=engine5)
Base.metadata.create_all(bind=engine6)
Base.metadata.create_all(bind=engine7)
Base.metadata.create_all(bind=engine8)
Base.metadata.create_all(bind=engine9)
Base.metadata.create_all(bind=engine10)
Base.metadata.create_all(bind=engine11)
Base.metadata.create_all(bind=engine12)

def inputt(engine:str, input_data:Logs):
    with Session(autoflush=False, bind=engine) as db:
        db.add(input_data)
        db.commit()

def sendto_shard(input_data:Logs, memory):
    match memory:
        case 0:
            inputt(engine=engine1, input_data = input_data)
            print("bd1")
        case 1:
            inputt(engine=engine2, input_data = input_data)
            print("bd2")
        case 2:
            inputt(engine=engine3, input_data = input_data)
            print("bd3")
        case 3:
            inputt(engine=engine4, input_data = input_data)
            print("bd4")
        case 4:
            inputt(engine=engine5, input_data = input_data)
            print("bd5")
        case 5:
            inputt(engine=engine6, input_data = input_data)
            print("bd6")
        case 6:
            inputt(engine=engine7, input_data = input_data)
            print("bd7")
        case 7:
            inputt(engine=engine8, input_data = input_data)
            print("bd8")
        case 8:
            inputt(engine=engine9, input_data = input_data)
            print("bd9")
        case 9:
            inputt(engine=engine10, input_data = input_data)
            print("bd10")
        case 10:
            inputt(engine=engine11, input_data = input_data)
            print("bd11")
        case 11:
            inputt(engine=engine12, input_data = input_data)
            print("bd12")
    return (memory + 1) % 12


def main():
    input_data = Logs(username = "asd", user_action = "DELETE", action_date = "2025-01-01", action_time = "00:00:00", action_result = "OK")
    memory = 0
    for i in range(1, 13):
        memory = sendto_shard(input_data, memory=memory)

if __name__ == "__main__":
    main()
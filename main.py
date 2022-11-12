import configparser
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import json

import class_model

def load_param():
    """Чтение параметров из файла settings.ini """
    config = configparser.ConfigParser()
    config.read("settings.ini")

    database_mane = config.get("database", "database_mane")
    user_name = config["database"]["user_name"]
    user_password = config["database"]["user_password"]
    server = config["database"]["server"]
    port = int(config["database"]["port"])

    DSN = f'postgresql+psycopg2://{user_name}:{user_password}@{server}:{port}/{database_mane}'

    return DSN

def create_database_structure():
    """Функция создания структуры БД"""
    dsn = load_param()
    engine = sqlalchemy.create_engine(dsn)
    engine.connect()
    
    class_model.drop_tables(engine=engine)
    class_model.create_tables(engine=engine)

def insert_data_from_file():
    """Функция заполнения БД данными из файла tests_data.json"""
    data = {}

    with open("fixtures/tests_data.json", "r") as read_file:
        data = json.load(read_file)

    for r in data:
         
        if r['model'] == 'publisher':
            db_rows = class_model.Publisher(**r['fields'])
            session.add(db_rows)
            session.commit()
        
        if r['model'] == 'book':
            db_rows = class_model.Book(**r['fields'])
            session.add(db_rows)
            session.commit()
        
        if r['model'] == 'shop':
            db_rows = class_model.Shop(**r['fields'])
            session.add(db_rows)
            session.commit()

        if r['model'] == 'stock':
            db_rows = class_model.Stock(**r['fields'])
            session.add(db_rows)
            session.commit()

        if r['model'] == 'sale':
            db_rows = class_model.Sale(**r['fields'])
            session.add(db_rows)
            session.commit()      

def select_shop_on_publisher(id_p, name_p):
    """Функция поиска магазинов продающих автора с идентификатором id_p и по имени name_p"""
    if id_p !='' and name_p != '':

        q = session.query(class_model.Publisher).filter(class_model.Publisher.id == id_p)

        if name_p == q.one().name:
            q1 = session.query(class_model.Shop).join(class_model.Stock).join(class_model.Book).join(class_model.Publisher).filter(class_model.Publisher.id == id_p)
            for s in q1.all():
                print(s.id, s.name)
        else:
            print(f'Идентификатор {id_p} не соответсвует издателю {name_p}')
    else:
        print('ВНИМАНИЕ!!!Введены нулевые параметры для поиска!!!')


if __name__ == "__main__":
    create_database_structure()
    # сессия
    dsn = load_param()
    engine = sqlalchemy.create_engine(dsn)
    engine.connect()
    
    Session = sessionmaker(bind=engine)
    session = Session()
    print('*****Функция поиска магазинов продающих автора с идентификатором id_p и по имени name_p*****')
    insert_data_from_file()

    id_p = input('Введите дентификатор издателя>>')
    name_p = input('Введите имя издателя>>')

    select_shop_on_publisher(id_p, name_p)

    
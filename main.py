import configparser
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import json

Base = declarative_base()

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

class Publisher(Base):
    """Класс таблицы Publisher"""    
    __tablename__ = "publisher" 

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True) 

class Book(Base):
    """Класс таблицы book"""
    __tablename__ = "book" 

    id = sq.Column(sq.Integer, primary_key=True)
    titel = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="Books")       

class Shop(Base):
    """Класс таблицы shop"""
    __tablename__ = "shop" 

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.Text, nullable=False)
   

class Sale(Base):
    """Класс таблицы salq"""
    __tablename__ = "sale" 

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
   

class Stock(Base):
    """Класс таблицы stock"""
    __tablename__ = "stock" 

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")
    sale = relationship(Sale, backref="stock")  

def create_tables(engine):
    """Функция создания таблиц в БД"""
    Base.metadata.create_all(engine) #Создание объектов     

def drop_tables(engine):
    """Функция удаления таблиц в БД"""
    Base.metadata.drop_all(engine) #Удаление объектов


def create_database_structure():
    """Функция создания структуры БД"""
    dsn = load_param()
    engine = sqlalchemy.create_engine(dsn)
    engine.connect()

    drop_tables(engine)
    create_tables(engine)

def add_publisher_rows(name_d):
    """Функция добавления строки в таблицу publishe"""
    db_rows = Publisher(name=name_d)
    session.add(db_rows)
    session.commit()

def add_book_rows(titel_d, id):
    """Функция добавления строки в таблицу book"""
    db_rows = Book(titel=titel_d, id_publisher=id)
    session.add(db_rows)
    session.commit()

def add_shop_rows(name_d):
    """Функция добавления строки в таблицу shop"""
    db_rows = Shop(name=name_d)
    session.add(db_rows)
    session.commit()

def add_stock_rows(id_b, id_s, count_d):
    """Функция добавления строки в таблицу stock"""
    db_rows = Stock(count=count_d, id_book=id_b, id_shop=id_s)
    session.add(db_rows)
    session.commit()

def add_sale_rows(price, date_sale, count, id_stock):
    """Функция добавления строки в таблицу sale"""
    db_rows = Sale(price=price, date_sale=date_sale, count=count, id_stock =id_stock)
    session.add(db_rows)
    session.commit()

def insert_data_from_file():
    """Функция заполнения БД данными из файла tests_data.json"""
    data = {}

    with open("fixtures/tests_data.json", "r") as read_file:
        data = json.load(read_file)

    res1 = ''

    for r in data:
        res = r['model']
        count = 1
        for x in r['fields']: 
         
            if res == 'publisher':
                add_publisher_rows(r['fields'][x])
        
            if res == 'book':
                if x == 'title':
                    par1 = r['fields'][x]
                elif x == 'id_publisher':
                    par2 = int(r['fields'][x])
                if count == len(r['fields']):
                    add_book_rows(par1, par2)
        
            if res == 'shop':
                add_shop_rows(r['fields'][x])

            if res == 'stock':
                if x == 'id_shop':
                    par1 = int(r['fields'][x])
                elif x == 'id_book':
                    par2 = int(r['fields'][x])
                elif x == 'count':
                    par3 = int(r['fields'][x])    
                if count == len(r['fields']):
                    add_stock_rows(par2, par1, par3)

            if res == 'sale':
                if x == 'price':
                    par1 = float(r['fields'][x])
                elif x == 'date_sale':
                    par2 = r['fields'][x]
                elif x == 'count':
                    par3 = int(r['fields'][x])    
                elif x == 'id_stock':
                    par4 = int(r['fields'][x]) 
                if count == len(r['fields']):                                 
                    add_sale_rows(par1, par2, par3, par4)
        
            count += 1

def select_shop_on_publisher(id_p, name_p):
    """Функция поиска магазинов продающих автора с идентификатором id_p и по имени name_p"""
    q = session.query(Publisher).filter(Publisher.id == id_p)

    if name_p == q.one().name:
        q1 = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == id_p)
        for s in q1.all():
            print(s.id, s.name)
    else:
        print(f'Идентификатор {id_p} не соответсвует издателю {name_p}')


if __name__ == "__main__":
    create_database_structure()
    # сессия
    dsn = load_param()
    engine = sqlalchemy.create_engine(dsn)
    engine.connect()

    Session = sessionmaker(bind=engine)
    session = Session()

    insert_data_from_file()

    id_p = input('Введите дентификатор издателя>>')
    name_p = input('Введите имя издателя>>')

    select_shop_on_publisher(id_p, name_p)
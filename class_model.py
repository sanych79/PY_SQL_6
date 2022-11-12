import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    """Класс таблицы Publisher"""    
    __tablename__ = "publisher" 

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True) 

class Book(Base):
    """Класс таблицы book"""
    __tablename__ = "book" 

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="book")       

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
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=True)
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")
    sale = relationship(Sale, backref="stock")  

def create_tables(engine):
    """Функция создания таблиц в БД"""
    Base.metadata.create_all(engine) #Создание объектов     

def drop_tables(engine):
    """Функция удаления таблиц в БД"""
    Base.metadata.drop_all(engine) #Удаление объектов
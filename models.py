from abc import ABC, abstractmethod
from atexit import register
from colorsys import yiq_to_rgb
from ctypes import resize
import datetime
from re import L
from tkinter.messagebox import RETRY
import traceback
from settings import db_path
import sqlite3


class BaseModel(ABC):

    def __init__(self, id=None) -> None:
        self.id = id
        self.__isValid = True

    @property
    
    def isValid(self):
        return self.__isValid

    @isValid.setter
    def isValid(self, isValid):
        self.__isValid = isValid

    @abstractmethod
    def print():
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @classmethod
    @abstractmethod
    def objects():
        pass

    @classmethod
    @abstractmethod
    def get_by_id(id):
        pass


class Market(BaseModel):
    table = 'Markets'

    def __init__(self, name, id=None) -> None:
        super().__init__(id)
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = ''
            self.__isValid = False

    def print():
        pass

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {Market.table} ('Name')
                                VALUES ('{self.name}')
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row
                            conn.execute(f'''
                                UPDATE {Market.table} set Name = '{self.name}' where Id = {self.id}
                            ''')

                            conn.commit()
                    except:
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                return True
            except:
                print('Bog\'lanishda xatolik')
        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Market.table} where Id = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {Market.table}
                """
                for row in cursor.execute(query):
                    yield Market(row[1], row[0])
        except:
            print('Bog\'lanishda xatolik')

    def get_by_id(id):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            query = f"""
                Select *From  {Market.table}
                Where Id={id}
                """
            res = cursor.execute(query).fetchone()
            if res is not None:
                return Market(res[1], res[0])
            else:
                return None

    def __str__(self):
        return f'{self.name}'


class Flat(BaseModel):
    table = 'Flats'

    def __init__(self, name, marketId, id=None) -> None:
        super().__init__(id)
        self.name = name
        self.marketId = marketId

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = ''
            self.__isValid = False

    @property
    def marketId(self):
        return self.__marketId

    @marketId.setter
    def marketId(self, marketId):
        if isinstance(marketId, int) and Market.get_by_id(marketId) is not None:
            self.__marketId = marketId
        else:
            self.__marketId = None
            self.__isValid = False

    @property
    def market(self):
        return Market.get_by_id(self.marketId)

    def print():
        pass

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {Flat.table} ('Name', MarketId)
                                VALUES ('{self.name}', {self.marketId})
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row

                            conn.execute(f'''
                                UPDATE {Flat.table} set Name = '{self.name}', MarketId={self.marketId} where Id = {self.id}
                            ''')

                            conn.commit()
                    except:
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                return True
            except:
                print('Bog\'lanishda xatolik')
        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Flat.table} where Id = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            print(db_path)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {Flat.table}
                """
                for row in cursor.execute(query):
                    yield Flat(row[1], row[2], row[0])
        except:
            print('Bog\'lanishda xatolik')

    def get_by_id(id):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            query = f"""
                Select *From  {Flat.table}
                Where Id={id}
                """
            res = cursor.execute(query).fetchone()
            if res is not None:
                return Flat(res[1], res[2], res[0])
            else:
                return None

    def __str__(self):
        return f'{self.market}\t | {self.name}'


class Row(BaseModel):
    table = 'Rows'

    def __init__(self, product_name, company_name, expiration_date, price, discount_price, flatId, id=None) -> None:
        super().__init__(id)
        self.product_name = product_name
        self.company_name = company_name
        self.expiration_date = expiration_date
        self.price = price
        self.discount_price = discount_price
        self.flatId = flatId

    @property
    def product_name(self):
        return self.__product_name

    @product_name.setter
    def product_name(self, product_name):
        if isinstance(product_name, str):
            self.__product_name = product_name
        else:
            self.__product_name = ''
            self.__isValid = False

    @property
    def company_name(self):
        return self.__company_name

    @company_name.setter
    def company_name(self, company_name):
        if isinstance(company_name, str):
            self.__company_name = company_name
        else:
            self.__company_name = ''
            self.__isValid = False

    @property
    def expiration_date(self):
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, expiration_date):
        if isinstance(expiration_date, int):
            self.__expiration_date = expiration_date
        else:
            self.__expiration_date = 0
            self.__isValid = False

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        if isinstance(price, int):
            self.__price = price
        else:
            self.__price = 0
            self.__isValid = False

    @property
    def discount_price(self):
        return self.__discount_price

    @discount_price.setter
    def discount_price(self, discount_price):
        if isinstance(discount_price, int):
            self.__discount_price = discount_price
        else:
            self.__discount_price = 0
            self.__isValid = False

    @property
    def flatId(self):
        return self.__flatId

    @flatId.setter
    def flatId(self, flatId):
        if isinstance(flatId, int):
            self.__flatId = flatId
        else:
            self.__flatId = 0
            self.__isValid = False

    @property
    def flat(self):
        return Flat.get_by_id(self.flatId)

    def del_by_id(id):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Row.table} where Id = {id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {Row.table} (Product_name, Company_name, Expiration_date, Price, Discount_price, FlatId)
                                VALUES ('{self.product_name}', '{self.company_name}', {self.expiration_date}, {self.price}, {self.discount_price}, {self.flatId})
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row

                            conn.execute(f'''
                                UPDATE {Row.table} set
                                Product_name = '{self.product_name}',
                                Company_name = '{self.company_name}',
                                Expiration_date = {self.expiration_date},
                                Price = {self.price},
                                Discount_price = {self.discount_price},
                                FlatId = {self.flatId}
                                where Id = {self.id}
                            ''')

                            conn.commit()
                    except:
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                        raise
                return True
            except:
                print('Bog\'lanishda xatolik')
                raise

        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Row.table} where Id = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            print(db_path)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {Row.table}
                """
                for row in cursor.execute(query):
                    yield Row(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        except:
            traceback.print_exc()
            print('Bog\'lanishda xatolik')

    def print():
        pass

    def get_by_id(id):
        pass

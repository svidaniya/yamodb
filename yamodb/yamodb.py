import sqlite3
import yaml
import os
import traceback
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256
import os
import json
import types
import random
import string
import locale
from collections import defaultdict
import time 
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  
dir = os.getcwd()
import calendar

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "placeholder_database")

def load_database(file):
    file_path = os.path.join(DATABASE_DIR, file)
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def ajusta_chave(chave):
    return sha256(chave.encode()).digest()

class YamTimes:
    def __init__(self, dt=None):
        if dt is None:
            self.__datetime = datetime.now()
        else:
            self.__datetime = dt

    def _set_locale(self, language_code: str):
        try:
            locale.setlocale(locale.LC_TIME, language_code)
        except locale.Error:
            print(f"Idioma {language_code} não é suportado.")

    def month_name(self, language_code: str = 'en_US') -> str:
        self._set_locale(language_code)
        return self.__datetime.strftime("%B")

    def weekday_name(self, language_code: str = 'en_US') -> str:
        self._set_locale(language_code)
        return self.__datetime.strftime("%A")

    def day_of_month(self) -> int:
        return self.__datetime.day

    def week_number(self) -> int:
        return self.__datetime.isocalendar()[1]

    def is_weekend(self) -> bool:
        return self.__datetime.weekday() >= 5

    def days_in_month(self) -> int:
        return calendar.monthrange(self.__datetime.year, self.__datetime.month)[1]

    def is_leap_year(self) -> bool:
        return (self.__datetime.year % 4 == 0 and (self.__datetime.year % 100 != 0 or self.__datetime.year % 400 == 0))

    def month(self) -> int:
        return self.__datetime.month

    def year(self) -> int:
        return self.__datetime.year

    def weekday_number(self) -> int:
        return self.__datetime.weekday()

    def hour(self) -> int:
        return self.__datetime.hour

    def minute(self) -> int:
        return self.__datetime.minute

    def second(self) -> int:
        return self.__datetime.second

    def timestamp(self) -> float:
        return self.__datetime.timestamp()

    def next_month(self) -> "YamTimes":
        next_month = self.__datetime.replace(day=28) + timedelta(days=4)
        return YamTimes(next_month.replace(day=1))

    def next_year(self) -> "YamTimes":
        return YamTimes(self.__datetime.replace(year=self.__datetime.year + 1))

    def last_week(self) -> "YamTimes":
        return YamTimes(self.__datetime - timedelta(weeks=1))

    def last_month(self) -> "YamTimes":
        return YamTimes(self.__datetime - timedelta(days=30))

    def is_dst(self) -> bool:
        return bool(self.__datetime.dst())

    def weeks_in_year(self) -> int:
        return 52 if not self.is_leap_year() else 53

    def start_of_month(self) -> "YamTimes":
        return YamTimes(self.__datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0))

    def end_of_month(self) -> "YamTimes":
        last_day = calendar.monthrange(self.__datetime.year, self.__datetime.month)[1]
        return YamTimes(self.__datetime.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999))

    def start_of_year(self) -> "YamTimes":
        return YamTimes(self.__datetime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0))

    def end_of_year(self) -> "YamTimes":
        return YamTimes(self.__datetime.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999))

    def quarter(self) -> str:
        month = self.__datetime.month
        if month <= 3:
            return "Q1"
        elif month <= 6:
            return "Q2"
        elif month <= 9:
            return "Q3"
        return "Q4"

    def previous_day(self) -> "YamTimes":
        return YamTimes(self.__datetime - timedelta(days=1))

    def next_day(self) -> "YamTimes":
        return YamTimes(self.__datetime + timedelta(days=1))

    def start_of_week(self) -> "YamTimes":
        start = self.__datetime - timedelta(days=self.__datetime.weekday())
        return YamTimes(start.replace(hour=0, minute=0, second=0, microsecond=0))

    def end_of_week(self) -> "YamTimes":
        end = self.__datetime + timedelta(days=(6 - self.__datetime.weekday()))
        return YamTimes(end.replace(hour=23, minute=59, second=59, microsecond=999999))

    def add_days(self, days: int) -> "YamTimes":
        return YamTimes(self.__datetime + timedelta(days=days))

    def subtract_days(self, days: int) -> "YamTimes":
        return YamTimes(self.__datetime - timedelta(days=days))

    def add_months(self, months: int) -> "YamTimes":
        new_month = self.__datetime.month + months
        year_adjustment = (new_month - 1) // 12
        new_month = new_month % 12 + 1
        return YamTimes(self.__datetime.replace(year=self.__datetime.year + year_adjustment, month=new_month))

    def subtract_months(self, months: int) -> "YamTimes":
        return self.add_months(-months)

    def add_years(self, years: int) -> "YamTimes":
        return YamTimes(self.__datetime.replace(year=self.__datetime.year + years))

    def subtract_years(self, years: int) -> "YamTimes":
        return self.add_years(-years)

    def seconds_until(self, other: "YamTimes") -> int:
        return int((other.datetime - self.__datetime).total_seconds())

    def days_until(self, other: "YamTimes") -> int:
        return (other.datetime - self.__datetime).days

    def hours_until(self, other: "YamTimes") -> int:
        return (other.datetime - self.__datetime).seconds // 3600

    def day_of_year(self) -> int:
        return self.__datetime.timetuple().tm_yday

    def short_month_name(self, language_code: str = 'en_US') -> str:
        self._set_locale(language_code)
        return self.__datetime.strftime("%b")

    def short_weekday_name(self, language_code: str = 'en_US') -> str:
        self._set_locale(language_code)
        return self.__datetime.strftime("%a")

    def week_day_number(self) -> int:
        return self.__datetime.weekday() + 1

    def time_12hr_format(self) -> str:
        return self.__datetime.strftime("%I:%M:%S %p")

    def readable_format(self, language_code: str = 'en_US') -> str:
        self._set_locale(language_code)
        return self.__datetime.strftime("%A, %d %B %Y %I:%M:%S %p")

    def is_holiday(self) -> bool:
        return False  

    def years_difference(self, other: "YamTimes") -> int:
        return abs(self.__datetime.year - other.datetime.year)

    def current_quarter(self) -> int:
        return (self.__datetime.month - 1) // 3 + 1

    def day_of_year_number(self) -> int:
        return self.__datetime.timetuple().tm_yday

    def time_24hr_format(self) -> str:
        return self.__datetime.strftime("%H:%M:%S")

    def iso_with_microseconds(self) -> str:
        return self.__datetime.isoformat()

    @property
    def datetime(self) -> datetime:
        return self.__datetime

    @classmethod
    def now(cls) -> "YamTimes":
        return cls(datetime.now())

    def tomorrow(self) -> "YamTimes":
        return YamTimes(self.__datetime + timedelta(days=1))

    def yesterday(self) -> "YamTimes":
        return YamTimes(self.__datetime - timedelta(days=1))
    @classmethod
    def today(self) -> "YamTimes":
        return YamTimes(datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))

    @classmethod
    def from_string(cls, date_string: str, format: str = "%Y-%m-%d %H:%M:%S") -> "YamTimes":
        return cls(datetime.strptime(date_string, format))

    @classmethod
    def from_iso_format(cls, iso_string: str) -> "YamTimes":
        return cls(datetime.fromisoformat(iso_string))

    @classmethod
    def from_timestamp(cls, ts: float) -> "YamTimes":
        return cls(datetime.fromtimestamp(ts))

    def after(self, years=0, months=0, days=0, hours=0, minutes=0, seconds=0) -> "YamTimes":
        return YamTimes(
            self.__datetime + relativedelta(
                years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds
            )
        )

    def before(self, years=0, months=0, days=0, hours=0, minutes=0, seconds=0) -> "YamTimes":
        return YamTimes(
            self.__datetime - relativedelta(
                years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds
            )
        )

    def set_time(self, hour: int = 0, minute: int = 0, second: int = 0) -> "YamTimes":
        return YamTimes(self.__datetime.replace(hour=hour, minute=minute, second=second, microsecond=0))

    def set_date(self, year: int, month: int, day: int) -> "YamTimes":
        return YamTimes(self.__datetime.replace(year=year, month=month, day=day))

    def start_of_week(self) -> "YamTimes":
        start = self.__datetime - timedelta(days=self.__datetime.weekday())
        return YamTimes(start.replace(hour=0, minute=0, second=0, microsecond=0))

    def end_of_week(self) -> "YamTimes":
        end = self.__datetime + timedelta(days=(6 - self.__datetime.weekday()))
        return YamTimes(end.replace(hour=23, minute=59, second=59, microsecond=999999))

    def start_of_month(self) -> "YamTimes":
        return YamTimes(self.__datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0))

    def end_of_month(self) -> "YamTimes":
        last_day = calendar.monthrange(self.__datetime.year, self.__datetime.month)[1]
        return YamTimes(self.__datetime.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999))

    def start_of_year(self) -> "YamTimes":
        return YamTimes(self.__datetime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0))

    def end_of_year(self) -> "YamTimes":
        return YamTimes(self.__datetime.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999))

    def is_same_day(self, other: "YamTimes") -> bool:
        return self.__datetime.date() == other.datetime.date()

    def is_past(self) -> bool:
        return self.__datetime < datetime.now()

    def is_future(self) -> bool:
        return self.__datetime > datetime.now()

    def days_in_month(self) -> int:
        return calendar.monthrange(self.__datetime.year, self.__datetime.month)[1]

    def to_iso_format(self) -> str:
        return self.__datetime.isoformat()

    def string(self, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        return self.__datetime.strftime(format)

    def timestamp(self) -> float:
        return self.__datetime.timestamp()

    def difference(self, other: "YamTimes") -> timedelta:
        if not isinstance(other, YamTimes):
            raise TypeError("O argumento deve ser uma instância de YamTimes")
        return self.__datetime - other.datetime

    def time_until(self, other: "YamTimes") -> timedelta:
        if not isinstance(other, YamTimes):
            raise TypeError("O argumento deve ser uma instância de YamTimes")
        return other.datetime - self.__datetime

    def is_before(self, other: "YamTimes") -> bool:
        if not isinstance(other, YamTimes):
            raise TypeError("O argumento deve ser uma instância de YamTimes")
        return self.__datetime < other.datetime

    def is_after(self, other: "YamTimes") -> bool:
        if not isinstance(other, YamTimes):
            raise TypeError("O argumento deve ser uma instância de YamTimes")
        return self.__datetime > other.datetime

    def __call__(self):
        return self.string()

    def __str__(self):
        return self.string()

    def __repr__(self):
        return f"YamTimes({self.__datetime!r})"

    def __format__(self, format_spec):
        return self.__datetime.strftime(format_spec or "%Y-%m-%d %H:%M:%S")

    def __eq__(self, other):
        return isinstance(other, YamTimes) and self.__datetime == other.datetime

    def __lt__(self, other):
        return isinstance(other, YamTimes) and self.__datetime < other.datetime

    def __le__(self, other):
        return isinstance(other, YamTimes) and self.__datetime <= other.datetime

    def __gt__(self, other):
        return isinstance(other, YamTimes) and self.__datetime > other.datetime

    def __ge__(self, other):
        return isinstance(other, YamTimes) and self.__datetime >= other.datetime

class Result:
    def __init__(self,data):
        self.__data = data
    def order_by(self, order,desc=False,reverse=False) -> "Result":
        return Result(
            sorted(
                self.__data,
                key=lambda x: (x[order] is None, x[order]),reverse=desc or reverse  
            )
        )

    def result(self):
        return self.__data
    def tail(self, n: int) -> "Result":
        return Result(self.__data[-n:])
    def head(self, n: int) -> "Result":
        return Result(self.__data[:n])
    def data(self):
        return self.__data
    def unique(self) -> "Result":
        return Result(list({str(item): item for item in self.__data}.values()))
    def first(self) -> "Result":
        return Result(self.__data[0])
    def number(self,number) -> "Result":
        return Result(self.__data[ number - 1 ])
    def limit(self,limit) -> "Result":
        return Result(self.__data[:limit])
    def print(self) :
        print(self.__data)
    def column(self, column) -> "Result":
        return Result([x[column] for x in self.__data])
    def where(self, where: dict) -> "Result":
        def apply_condition(item, condition):
            field, value = condition
            item_value = item.get(field)
            if value.startswith('='):
                return item_value == value[1:]
            elif value.startswith('>'):
                return item_value > float(value[1:])
            elif value.startswith('<'):
                return item_value < float(value[1:])
            elif value.startswith('>='):
                return item_value >= float(value[2:])
            elif value.startswith('<='):
                return item_value <= float(value[2:])
            elif value.startswith('!='):
                return item_value != value[2:]
            else:
                return item_value == value

        result = self.__data
        for field, condition in where.items():
            result = [item for item in result if apply_condition(item, (field, condition))]
        return Result(result)
    def like(self, like: dict) -> "Result":
        def match(value, pattern):
            if pattern.endswith('%'):  
                return value.startswith(pattern[:-1])  
            if pattern.startswith('%'):  
                return value.endswith(pattern[1:])  
            return value == pattern  

        return Result([
            x for x in self.__data if all(match(x[key], value) for key, value in like.items())
        ])
    def not_like(self, not_like: dict) -> "Result":
        def does_not_match(value, pattern):
            if pattern.endswith('%'):  
                return not value.startswith(pattern[:-1])  
            if pattern.startswith('%'):  
                return not value.endswith(pattern[1:])  
            return value != pattern  

        return Result([
            x for x in self.__data if all(does_not_match(x[key], value) for key, value in not_like.items())
        ])
    def group_by(self, column: str) -> "Result":
        groups = defaultdict(list)
        for item in self.__data:
            key = item[column]
            groups[key].append(item)
        return Result(dict(groups))
    def distinct(self) -> "Result":
        return Result(list({str(item): item for item in self.__data}.values()))
    def count(self) -> "Result":
        return Result(len(self.__data))
    def sum(self) -> "Result":
        return Result(sum(float(x) for x in self.__data))
    def avg(self) -> "Result":
        return Result(sum(float(x) for x in self.__data) / len(self.__data))
    def decrypt(self, column=None) -> "Result":
        if column:  

            return Result([
                {**item, column: YamoDB.decrypt(item[column])} if column in item else item
                for item in self.__data
            ])
        else:

            return Result([YamoDB.decrypt(x) for x in self.__data])
    def update(self, new_data: dict) -> bool:
            cursor = YamoDB.db.cursor()  

            for item in self.__data:

                set_clause = ", ".join([f"{key} = ?" for key in new_data.keys()])
                values = tuple(new_data.values())

                where_clause = " AND ".join([f"{key} = ?" for key in item.keys()])
                where_values = tuple(item.values())

                query = f"UPDATE user SET {set_clause} WHERE {where_clause}"

                cursor.execute(query, values + where_values)

            YamoDB.db.commit()

            return True  
    def delete(self) -> bool:
        cursor = YamoDB.db.cursor()  

        for item in self.__data:

            where_clause = " AND ".join([f"{key} = ?" for key in item.keys()])
            values = tuple(item.values())

            cursor.execute(f"DELETE FROM user WHERE {where_clause}", values)

        YamoDB.db.commit()

        return True
    def is_empty(self) -> bool:
        return len(self.__data) == 0
    def random_sample(self, n : int = 1) -> "Result":
        sample = random.sample(self.__data, n)
        return Result(sample)
    def exclude(self,condition : dict) -> "Result":
        return Result([x for x in self.__data if all(x[key] != value for key, value in condition.items())])
    def apply(self, func) -> "Result":
        return Result([func(item) for item in self.__data])

    def to_yamtimes(self) -> YamTimes:
        return YamTimes().from_string(self.__data)

    def __call__(self):

        return self.__data

    def __str__(self):

        return str(self.__data)

    def __repr__(self):

        return f"{self.__data}"

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __getitem__(self, index):
        return self.__data[index]
class YamoDB:
    secret = None
    db = None
    db_name = None
    delete_old_db = False
    debug_mode = False  

    COLORS = {
        'reset': '\033[0m',
        'blue': '\033[34m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'red': '\033[31m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
    }

    @staticmethod
    def number_placeholder(min_value = 0, max_value = 1000):
        return random.randint(min_value, max_value)
    @staticmethod
    def random_placeholder(length = 30):

        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    @staticmethod
    def name_placeholder(middle_name = True):
            first_names = load_database("first-names.json")
            first_name = random.choice(first_names)
            if(middle_name):
                    middle_names = load_database("middle-names.json")
                    middle_name = random.choice(middle_names)
                    return f"{first_name} {middle_name}"
            else:
                return first_name
    @staticmethod
    def encrypt(content,in_string=True):
        if(YamoDB.secret):

            secret_key = ajusta_chave(YamoDB.secret)

            iv = os.urandom(16)

            cipher = Cipher(algorithms.AES(secret_key), modes.CTR(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            encrypted = encryptor.update(content.encode()) + encryptor.finalize()

            if(not in_string):
                return {
                    'a': iv.hex(),
                    'l': encrypted.hex()
                }
            else:
                return json.dumps({
                    'a': iv.hex(),
                    'l': encrypted.hex()
                })
        else:
            YamoDB.log_error("Secret key not set.", color='red')
            return "Secret key not set."

    @staticmethod
    def decrypt(content):
        if(YamoDB.secret):
            try:

                if isinstance(content, str):
                    try:

                        content = json.loads(content.replace("'", '"'))
                    except json.JSONDecodeError as e:
                        print(f"Erro ao decodificar JSON: {e}")
                        return False  

                secret_key = ajusta_chave(YamoDB.secret)

                if 'a' not in content or 'l' not in content:
                    raise ValueError("Conteúdo inválido: chaves 'a' ou 'l' não encontradas.")

                iv = bytes.fromhex(content['a'])
                encrypted_content = bytes.fromhex(content['l'])

                cipher = Cipher(algorithms.AES(secret_key), modes.CTR(iv), backend=default_backend())
                decryptor = cipher.decryptor()

                decrypted = decryptor.update(encrypted_content) + decryptor.finalize()

                return decrypted.decode()

            except Exception as e:
                print(f"Erro ao descriptar o conteúdo: {e}")
                return False
        else:
            YamoDB.log_error("Secret key not set.", color='red')
            return "Secret key not set."

    @staticmethod
    def log_debug(message, color='cyan'):
        """Print debug messages if debug mode is enabled with color."""
        if YamoDB.debug_mode:
            print(f"{YamoDB.COLORS[color]}[DEBUG] {message}{YamoDB.COLORS['reset']}")

    @staticmethod
    def log_info(message, color='green'):
        """Print info messages with color."""
        print(f"{YamoDB.COLORS[color]}[INFO] {message}{YamoDB.COLORS['reset']}")

    @staticmethod
    def log_warning(message, color='yellow'):
        """Print warning messages with color."""
        print(f"{YamoDB.COLORS[color]}[WARNING] {message}{YamoDB.COLORS['reset']}")

    @staticmethod
    def log_error(message, color='red'):
        """Print error messages with color."""
        print(f"{YamoDB.COLORS[color]}[ERROR] {message}{YamoDB.COLORS['reset']}")

    @staticmethod
    def delete_database():
        if YamoDB.db_name:
            if os.path.exists(YamoDB.db_name):
                os.remove(YamoDB.db_name)
                YamoDB.log_warning(f"Database '{YamoDB.db_name}' deleted.", color='yellow')

    @staticmethod
    def connect(db_name='db.sqlite3'):
        YamoDB.db_name = db_name
        if(YamoDB.delete_old_db):
            YamoDB.delete_database()
        try:
            YamoDB.db = sqlite3.connect(db_name,check_same_thread=False)
            YamoDB.db.execute("PRAGMA foreign_keys = ON;")
            YamoDB.log_info(f"Successfully connected to the database '{db_name}'.", color='green')
            return True
        except sqlite3.Error as e:
            YamoDB.log_error(f"Error connecting to the database: {e}", color='red')
            return False

    @staticmethod
    def close():
        try:
            if YamoDB.db:
                YamoDB.db.close()
                YamoDB.db = None
                YamoDB.db_name = None
                YamoDB.log_info("Database connection closed.", color='green')
                return True
            else:
                YamoDB.log_warning("No open connection.", color='yellow')
                return False
        except sqlite3.Error as e:
            YamoDB.log_error(f"Error closing the database connection: {e}", color='red')
            return False

    @staticmethod
    def generate_from(yaml_string):
        try:
            data = yaml.load(yaml_string, Loader=yaml.FullLoader)
            YamoDB.log_info("YAML loaded successfully.", color='green')
            YamoDB.generate(data)
        except Exception as e:
            YamoDB.log_error(f"Error processing the YAML: {e}", color='red')

    @staticmethod
    def generate_from_file(yaml_file):
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                YamoDB.log_info(f"YAML file '{yaml_file}' loaded successfully.", color='green')
                YamoDB.generate(data)
        except Exception as e:
            YamoDB.log_error(f"Error reading the YAML file: {e}", color='red')
            return

    @staticmethod
    def generate(data):
        try:
            YamoDB.db.execute("PRAGMA foreign_keys = ON;")
            cursor = YamoDB.db.cursor()

            type_mapping = {
                'string': 'TEXT',
                'number': 'INTEGER',
                'int': 'INTEGER',
                'integer': 'INTEGER',
                'float': 'REAL',
                'blob': 'BLOB',
                'numeric': 'NUMERIC',
                'datetime': 'DATETIME',
                'date': 'DATE',
                'time': 'TIME',
                'boolean': 'BOOLEAN',
                'encrypted': 'TEXT',  
            }

            for table_name, columns in data.items():
                column_definitions = []
                foreign_keys = []

                YamoDB.log_info(f"Generating table: {table_name}", color='green')
                for column_name, attributes in columns.items():

                    constraints = []
                    if 'reference' in attributes and attributes['reference']:
                        reference = attributes['reference'].split('.')
                        reference_table = reference[0]
                        reference_column = reference[1]
                        

                        foreign_key = f"FOREIGN KEY ({column_name}) REFERENCES {reference_table}({reference_column})"
                        

                        if "on_delete" in attributes and attributes["on_delete"]:
                            on_delete = attributes["on_delete"]
                            if on_delete == "cascade":
                                foreign_key += " ON DELETE CASCADE"
                            elif on_delete == "set_null":
                                foreign_key += " ON DELETE SET NULL"
                            elif on_delete == "no_action":
                                foreign_key += " ON DELETE NO ACTION"
                            elif on_delete == "restrict":
                                foreign_key += " ON DELETE RESTRICT"
                        

                        if "on_update" in attributes and attributes["on_update"]:
                            on_update = attributes["on_update"]
                            if on_update == "cascade":
                                foreign_key += " ON UPDATE CASCADE"
                            elif on_update == "set_null":
                                foreign_key += " ON UPDATE SET NULL"
                            elif on_update == "no_action":
                                foreign_key += " ON UPDATE NO ACTION"
                            elif on_update == "restrict":
                                foreign_key += " ON UPDATE RESTRICT"
                        

                        foreign_keys.append(foreign_key)

                    else:
                        YamoDB.log_debug(f"  Processing column: {column_name}", color='cyan')
                        col_type = type_mapping.get(attributes['type'], 'TEXT')
                        if "unique" in attributes and attributes["unique"]:
                            constraints.append("UNIQUE")
                        if "primary_key" in attributes and attributes["primary_key"]:
                            constraints.append("PRIMARY KEY")
                        if 'max_length' in attributes:
                            constraints.append(f"CHECK(LENGTH({column_name}) <= {attributes['max_length']})")
                        if 'not_null' in attributes and attributes['not_null']:
                            constraints.append("NOT NULL")
                        if 'default' in attributes:
                            constraints.append(f"DEFAULT {attributes['default']}")
                        if 'auto_increment' in attributes and attributes['auto_increment']:
                            constraints.append("AUTOINCREMENT")
                        if 'autoincrement' in attributes and attributes['auto_increment']:
                            constraints.append("AUTOINCREMENT")

                    column_definitions.append(f"{column_name} {col_type} {' '.join(constraints)}")

                column_definitions.extend(foreign_keys)

                create_table_command = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(column_definitions)}
                )
                """
                YamoDB.log_debug(f"Generated SQL for table '{table_name}':", color='magenta')
                YamoDB.log_debug(create_table_command, color='magenta')  
                cursor.execute(create_table_command)

            YamoDB.db.commit()
            YamoDB.log_info(f"Finished generating tables! Total tables: {len(data)}", color='green')

        except sqlite3.Error as e:
            YamoDB.log_error(f"Error creating the database or executing commands: {e}", color='red')
        except Exception as e:
            YamoDB.log_error(f"Unexpected error: {e}", color='red')
            traceback.print_exc()  

    @staticmethod
    def insert(row, data) -> bool:
        try:
            if not YamoDB.db:
                YamoDB.log_error("Connection not established.", color='red')
                return False

            cursor = YamoDB.db.cursor()
            columns = ", ".join(data.keys())
            values = ", ".join("?" * len(data))
            query = f"INSERT INTO {row} ({columns}) VALUES ({values})"

            cursor.execute(query, tuple(data.values()))
            YamoDB.db.commit()
            if(YamoDB.debug_mode):
                YamoDB.log_info(f"Inserted data into {row} table.", color='green')
            return True
        except sqlite3.Error as e:
            YamoDB.log_error(f"Error inserting data: {e}", color='red')
            return False
        except Exception as e:
            print(traceback.format_exc())
            YamoDB.log_error(f"Unexpected error: {e}", color='red')
            return False

    @staticmethod
    def select(row, where=None, order_by=None, asc=False, desc=False, limit=None, offset=None, like=None, first=False) -> Result:
        try:
            if not YamoDB.db:
                YamoDB.log_error("Connection not established.", color='red')
                return []

            cursor = YamoDB.db.cursor()

            query = f"SELECT * FROM {row}"
            params = []
            conditions = []

            if where:
                for key, value in where.items():
                    if value is None:
                        YamoDB.log_warning(f"Skipping condition with None value for key '{key}'.", color='yellow')
                        continue

                    if isinstance(value, str) and value.startswith(('=', '>', '<', '>=', '<=', '!=')):
                        operator = value[:2] if value[:2] in ('>=', '<=', '!=') else value[0]  
                        conditions.append(f"{key} {operator} ?")
                        params.append(value[2:] if operator != value[0] else value[1:])
                    else:
                        conditions.append(f"{key} = ?")
                        params.append(value)

                    if like and key in like:
                        conditions.append(f"{key} LIKE ?")
                        params.append(f"%{like[key]}%")

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

            if order_by:
                query += f" ORDER BY {order_by} "
                if asc:
                    query += "ASC"
                elif desc:
                    query += "DESC"

            if limit:
                query += f" LIMIT {limit}"

            if offset:
                query += f" OFFSET {offset}"

            YamoDB.log_debug(f"Executing query: {query}", color='magenta')
            cursor.execute(query, tuple(params))

            columns = [description[0] for description in cursor.description]
            results = cursor.fetchall()

            results_dict = [dict(zip(columns, row)) for row in results]

            if first:
                return results_dict[0] if results_dict else None
            return Result(results_dict)
        except sqlite3.Error as e:
            YamoDB.log_error(f"Error querying data: {e}", color='red')
            return []
        except Exception as e:
            YamoDB.log_error(f"Unexpected error: {e}", color='red')
            return []
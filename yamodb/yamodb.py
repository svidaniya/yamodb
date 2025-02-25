import sqlite3
import yaml
import os
import traceback
import json
from collections import defaultdict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256
import os
import json
import random
import string
from yamtimes import YamTimes
dir = os.getcwd()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "placeholder_database")

def load_database(file):
    file_path = os.path.join(DATABASE_DIR, file)
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def adjust_key(key):
    return sha256(key.encode()).digest()


class Result:
    def __init__(self,table,data):
        self.__data = data
        self.__table = table

    def order_by(self, order, desc=False, reverse=False) -> "Result":
        try:
            return Result(
                self.__table,
                sorted(
                    self.__data,
                    key=lambda x: (x[order] is None, x[order]), reverse=desc or reverse
                )
            )
        except Exception as e:
            YamoDB.log_error(f"Error in order_by: {e}", color='red')
            return Result(self.__table,[])

    def result(self):
        return self.__data

    def tail(self, n: int) -> "Result":
        try:
            return Result(self.__table,self.__data[-n:])
        except Exception as e:
            YamoDB.log_error(f"Error in tail: {e}", color='red')
            return Result(self.__table,[])

    def head(self, n: int) -> "Result":
        try:
            return Result(self.__table,self.__data[:n])
        except Exception as e:
            YamoDB.log_error(f"Error in head: {e}", color='red')
            return Result(self.__table,[])

    def data(self):
        return self.__data

    def unique(self) -> "Result":
        try:
            return Result(self.__table,list({str(item): item for item in self.__data}.values()))
        except Exception as e:
            YamoDB.log_error(f"Error in unique: {e}", color='red')
            return Result(self.__table,[])

    def first(self) -> "Result":
        try:
            return Result(self.__table,self.__data[0]) if self.__data else Result([])
        except Exception as e:
            YamoDB.log_error(f"Error in first: {e}", color='red')
            return Result(self.__table,[])

    def number(self, number) -> "Result":
        try:
            return Result(self.__table,self.__data[number - 1:number])
        except Exception as e:
            YamoDB.log_error(f"Error in number: {e}", color='red')
            return Result(self.__table,[])

    def limit(self, limit) -> "Result":
        try:
            return Result(self.__table,self.__data[:limit])
        except Exception as e:
            YamoDB.log_error(f"Error in limit: {e}", color='red')
            return Result(self.__table,[])

    def print(self):
        try:
            print(self.__data)
        except Exception as e:
            YamoDB.log_error(f"Error in print: {e}", color='red')

    def column(self, column) -> "Result":
        try:
            return Result(self.__table,[x[column] for x in self.__data if column in x])
        except Exception as e:
            YamoDB.log_error(f"Error in column: {e}", color='red')
            return Result(self.__table,[])

    def where(self, where: dict) -> "Result":
        try:
            def apply_condition(item, condition):
                field, value = condition
                item_value = item.get(field)
                if(value == 'NULL'):
                    return item_value is None
                elif(value == 'NOT NULL'):
                    return item_value is not None
                elif(value == 'IS NULL'):
                    return item_value is None
                elif(value == 'IS NOT NULL'):
                    return item_value is not None
                elif(value == None):
                    return item_value is None
                elif value.startswith('='):
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
                elif value.startswith('NULL'):
                    return item_value is None
                else:
                    return item_value == value

            result = self.__data
            for field, condition in where.items():
                result = [item for item in result if apply_condition(item, (field, condition))]
            return Result(self.__table,result)
        except Exception as e:
            YamoDB.log_error(f"Error in where: {e}", color='red')
            return Result(self.__table,[])

    def like(self, like: dict) -> "Result":
        try:
            def match(value, pattern):
                if pattern.endswith('%'):  
                    return value.startswith(pattern[:-1])  
                if pattern.startswith('%'):  
                    return value.endswith(pattern[1:])  
                return value == pattern  

            return Result([
                x for x in self.__data if all(match(x[key], value) for key, value in like.items())
            ])
        except Exception as e:
            YamoDB.log_error(f"Error in like: {e}", color='red')
            return Result(self.__table,[])

    def not_like(self, not_like: dict) -> "Result":
        try:
            def does_not_match(value, pattern):
                if pattern.endswith('%'):  
                    return not value.startswith(pattern[:-1])  
                if pattern.startswith('%'):  
                    return not value.endswith(pattern[1:])  
                return value != pattern  

            return Result(self.__table,[
                x for x in self.__data if all(does_not_match(x[key], value) for key, value in not_like.items())
            ])
        except Exception as e:
            YamoDB.log_error(f"Error in not_like: {e}", color='red')
            return Result(self.__table,[])

    def group_by(self, column: str) -> "Result":
        try:
            groups = defaultdict(list)
            for item in self.__data:
                key = item[column]
                groups[key].append(item)
            return Result(self.__table,dict(groups))
        except Exception as e:
            YamoDB.log_error(f"Error in group_by: {e}", color='red')
            return Result(self.__table,[])

    def distinct(self) -> "Result":
        try:
            return Result(self.__table,list({str(item): item for item in self.__data}.values()))
        except Exception as e:
            YamoDB.log_error(f"Error in distinct: {e}", color='red')
            return Result(self.__table,[])

    def count(self) -> "Result":
        try:
            return Result(self.__table,len(self.__data))
        except Exception as e:
            YamoDB.log_error(f"Error in count: {e}", color='red')
            return Result(self.__table,0)

    def sum(self) -> "Result":
        try:
            return Result(self.__table,sum(float(x) for x in self.__data))
        except Exception as e:
            YamoDB.log_error(f"Error in sum: {e}", color='red')
            return Result(self.__table,0)

    def avg(self) -> "Result":
        try:
            return Result(self.__table,sum(float(x) for x in self.__data) / len(self.__data))
        except Exception as e:
            YamoDB.log_error(f"Error in avg: {e}", color='red')
            return Result(self.__table,0)

    def decrypt(self, column=None) -> "Result":
        try:
            if column:  
                return Result(self.__table,[
                    {**item, column: YamoDB.decrypt(item[column])} if column in item else item
                    for item in self.__data
                ])
            else:
                for item in self.__data:
                    for key in item.keys():
                        try:
                            item[key] = YamoDB.decrypt(item[key])
                        except Exception as e:
                            pass
                return Result(self.__table,self.__data)
        except Exception as e:
            YamoDB.log_error(f"Error in decrypt: {e}", color='red')
            return Result(self.__table,[])

    def update(self, new_data: dict, commit=True) -> "Result":
        if not self.__data:
            YamoDB.log_error("No data to update.", color='red')
            return self  # Retorna o Result, independentemente de ter dados ou não
        
        try:
            cursor = YamoDB.db.cursor()
            updated_data = []  # Lista para armazenar dados atualizados

            for item in self.__data:
                set_clause = ", ".join([f"{key} = ?" for key in new_data.keys()])
                values = tuple(new_data.values())
                
                where_conditions = []
                where_values = []

                for key, value in item.items():
                    if value is None:
                        where_conditions.append(f"{key} IS NULL")  # Usa IS NULL para None
                    else:
                        where_conditions.append(f"{key} = ?")
                        where_values.append(value)

                where_clause = " AND ".join(where_conditions)
                query = f"UPDATE {self.__table} SET {set_clause} WHERE {where_clause}"
                
                updated_data.append({**item, **new_data})  # Combina o item original com os novos dados
                
                if commit:
                    cursor.execute(query, values + tuple(where_values))

            if commit:
                YamoDB.db.commit()  # Faz o commit se commit for True
                if YamoDB.debug_mode:
                    YamoDB.log_info("Data updated successfully.", color='green')

            return Result(self.__table, updated_data)
            
        except sqlite3.Error as e:
            YamoDB.log_error(f"Error updating data: {e}", color='red')
            return self  # Retorna o Result sem

    def delete(self, commit=True) -> "Result":
        if not self.__data:
            YamoDB.log_error("No data to delete.", color='red')
            return self  # Retorna o Result, independentemente de ter dados ou não
        
        try:
            cursor = YamoDB.db.cursor()
            deleted_data = []  # Lista para armazenar dados deletados (caso commit seja False)

            for item in self.__data:
                where_conditions = []
                values = []

                for key, value in item.items():
                    if value is None:
                        where_conditions.append(f"{key} IS NULL")  # Usa IS NULL para None
                    else:
                        where_conditions.append(f"{key} = ?")
                        values.append(value)

                where_clause = " AND ".join(where_conditions)
                query = f"DELETE FROM {self.__table} WHERE {where_clause}"
                
                deleted_data.append(item)
                if commit:
                    
                    cursor.execute(query, tuple(values))

            if commit:
                YamoDB.db.commit()  # Faz o commit se commit for True
                if YamoDB.debug_mode:
                    YamoDB.log_info("Data deleted successfully.", color='green')

            return Result(self.__table, [item for item in self.__data if item not in deleted_data])
            
            

        except sqlite3.Error as e:
            YamoDB.log_error(f"Error deleting data: {e}", color='red')
            return self  # Retorna o Result sem alterações em caso de erro


    def is_empty(self) -> bool:
        try:
            return len(self.__data) == 0
        except Exception as e:
            YamoDB.log_error(f"Error in is_empty: {e}", color='red')
            return True

    def random_sample(self, n: int = 1) -> "Result":
        try:
            sample = random.sample(self.__data, n)
            return Result(self.__table,sample)
        except Exception as e:
            YamoDB.log_error(f"Error in random_sample: {e}", color='red')
            return Result(self.__table,[])

    def exclude(self, condition: dict) -> "Result":
        try:
            return Result(self.__table,[x for x in self.__data if all(x[key] != value for key, value in condition.items())])
        except Exception as e:
            YamoDB.log_error(f"Error in exclude: {e}", color='red')
            return Result(self.__table,[])

    def apply(self, func) -> "Result":
        try:
            return Result(self.__table,[func(item) for item in self.__data])
        except Exception as e:
            YamoDB.log_error(f"Error in apply: {e}", color='red')
            return Result(self.__table,self.__table,[])

    def to_yamtimes(self) -> YamTimes:
        try:
            return YamTimes().from_string(self.__data)
        except Exception as e:
            YamoDB.log_error(f"Error in to_yamtimes: {e}", color='red')
            return YamTimes()

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
    

class YamoDB():
    NULL = None
    secret = None
    db = None
    db_name = None
    delete_old_db = False
    debug_mode = False  
    time = YamTimes
    
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

            secret_key = adjust_key(YamoDB.secret)

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
                    
                        return False  

                secret_key = adjust_key(YamoDB.secret)

                if 'a' not in content or 'l' not in content:
                    raise ValueError("Conteúdo inválido: keys 'a' ou 'l' não encontradas.")

                iv = bytes.fromhex(content['a'])
                encrypted_content = bytes.fromhex(content['l'])

                cipher = Cipher(algorithms.AES(secret_key), modes.CTR(iv), backend=default_backend())
                decryptor = cipher.decryptor()

                decrypted = decryptor.update(encrypted_content) + decryptor.finalize()

                return decrypted.decode()

            except Exception as e:
                
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
            return Result(row,results_dict)
        except sqlite3.Error as e:
            YamoDB.log_error(f"Error querying data: {e}", color='red')
            return []
        except Exception as e:
            YamoDB.log_error(f"Unexpected error: {e}", color='red')
            return []
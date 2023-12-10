from dataclasses import dataclass
from language_strings.language_string import LanguageString
from client_object import ClientObject
from datetime import datetime
from util import identity, parse_client_timestamp


@dataclass
class Clinic(ClientObject):
    id: str
    name: LanguageString
    updated_at: datetime

    def client_insert_values(self):
        return [self.id, self.name.id.replace('-', ''), self.format_ts(self.updated_at)]

    @classmethod
    def client_insert_sql(cls):
        return """INSERT INTO clinics (id, name, updated_at) VALUES (?, ?, ?)"""

    def client_update_values(self):
        return [self.name.id.replace('-', ''), self.format_ts(self.updated_at), self.id]

    @classmethod
    def client_update_sql(cls):
        return """UPDATE clinics SET name = ?, updated_at = ? WHERE id = ?"""

    def server_insert_values(self):
        return [self.id, self.name.id, self.updated_at]

    @classmethod
    def server_insert_sql(cls):
        return """INSERT INTO clinics (id, name, updated_at) VALUES (%s, %s, %s)"""

    def server_update_values(self):
        return [self.name.id, self.updated_at, self.id]

    @classmethod
    def server_update_sql(cls):
        return """UPDATE clinics SET name =%s, updated_at = %s WHERE id = %s"""

    @classmethod
    def db_columns_from_server(cls):
        return [('id', lambda s: s.replace('-', '')),
                ('name', cls.make_language_string),
                ('updated_at', identity)]

    @classmethod
    def db_columns_from_client(cls):
        return [('id', identity),
                ('name', cls.make_language_string),
                ('updated_at', parse_client_timestamp)]

    @classmethod
    def table_name(cls):
        return "clinics"

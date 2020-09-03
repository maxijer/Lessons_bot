import sqlite3


class Olymp:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def physics(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM "olymp"  WHERE "predmet" = "Физика"').fetchall()

    def math(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM "olymp"  WHERE "predmet" = "Математика"').fetchall()

    def inform(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM "olymp"  WHERE "predmet" = "Информатика"').fetchall()

import sqlite3
import enum


class Mode(enum.Enum):
    EASY = 0
    HARD = 1


def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Words
                 (word VARCHAR(100), mode INTEGER)''')
    cursor.execute("create table if not exists games (user_id integer, mode integer, score integer)")


def insert_words(file, cursor, mode):
    words = file.readlines()

    for word in words:
        cursor.execute("INSERT INTO Words (word, mode) VALUES (?, ?)", (word.rstrip(), mode))


def write():
    with open("easy.txt", "r") as easy, open("hard.txt", "r") as hard, sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()

        create_tables(cursor)

        insert_words(easy, cursor, Mode.EASY.value)
        conn.commit()

        insert_words(hard, cursor, Mode.HARD.value)
        conn.commit()


def get_word(mode):
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        res = cursor.execute("SELECT word FROM Words WHERE mode = ? ORDER BY RANDOM() LIMIT 1;", (mode.value, ))
        res, *_ = res.fetchone()
        return res

if __name__ == "__main__":
    write()

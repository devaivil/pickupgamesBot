import pandas as pd
import sqlite3

def import_games():
    try:
        # Чтение данных из Excel
        df = pd.read_excel('игры.xlsx', sheet_name='описание', header=0)

        # Задаем имена столбцов
        df.columns = ['id', 'name', 'genre', 'developer', 'description']

        # Создание соединения с базой данных SQLite
        conn = sqlite3.connect('mentor_games.db')

        # Запись данных в таблицу SQLite
        df.to_sql('games', conn, if_exists='replace', index=False)

        # Закрытие соединения с базой данных
        conn.close()
        print("Готово!")
    except Exception as e:
        print(e)


def import_games_parameters():
    try:
        # Чтение данных из Excel
        df = pd.read_excel('игры.xlsx', sheet_name='все игры', header=0)

        # Задаем имена столбцов
        df.columns = ['id', 'game_id', 'first_answer', 'second_answer', 'third_answer', 'fourth_answer', 'fifth_answer']

        # Создание соединения с базой данных SQLite
        conn = sqlite3.connect('mentor_games.db')

        # Запись данных в таблицу SQLite
        df.to_sql('games_parameters', conn, if_exists='replace', index=False)

        # Закрытие соединения с базой данных
        conn.close()
        print("Готово!")
    except Exception as e:
        print(e)


import_games()
import_games_parameters()
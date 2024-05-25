from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'database.db'  # Укажите путь к вашей базе данных

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Для удобного доступа к столбцам по имени
    return conn

# Инициализация базы данных и создание таблицы для примера (если необходимо)
def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS example (id INTEGER PRIMARY KEY, name TEXT)')
        conn.commit()
        conn.close()


# Главная страница с формой для ввода SQL-запроса
@app.route('/')
def index():
    return render_template('index.html', result='')

# Обработка SQL-запроса
@app.route('/execute', methods=['POST'])
def execute():
    query = request.form['query']
    result = ""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(query)
        if query.strip().upper().startswith("SELECT"):
            result = c.fetchall()
            result = format_result(result)
        else:
            conn.commit()
            result = "Query executed successfully"
        conn.close()
    except Exception as e:
        result = str(e)
    return render_template('index.html', result=result)

def format_result(result):
    if not result:
        return "No results"
    return "<br>".join([str(dict(row)) for row in result])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
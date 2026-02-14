from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar tabelas
def create_tables():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        amount REAL,
        date TEXT,
        FOREIGN KEY (member_id) REFERENCES members (id)
    )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    members = conn.execute('SELECT * FROM members').fetchall()
    transactions = conn.execute('SELECT * FROM transactions').fetchall()
    
    # Calcular total de gastos
    total_expenses = sum(transaction['amount'] for transaction in transactions)
    
    conn.close()
    return render_template('index.html', members=members, transactions=transactions, total_expenses=total_expenses)

@app.route('/add_member', methods=('GET', 'POST'))
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        conn.execute('INSERT INTO members (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_member.html')

@app.route('/add_transaction', methods=('GET', 'POST'))
def add_transaction():
    if request.method == 'POST':
        member_id = request.form['member_id']
        amount = request.form['amount']
        date = request.form['date']
        conn = get_db_connection()
        conn.execute('INSERT INTO transactions (member_id, amount, date) VALUES (?, ?, ?)', (member_id, amount, date))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_transaction.html')

if __name__ == '__main__':
    create_tables()  # Cria as tabelas ao iniciar
    app.run(debug=True)

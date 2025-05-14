from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Основен маршрут, който показва всички коли
@app.route('/')
def index():
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Cars')
    cars = c.fetchall()
    conn.close()
    return render_template('index.html', cars=cars)

# Маршрут за добавяне на нова кола
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        status = request.form['status']
        
        conn = sqlite3.connect('cars.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO Cars (make, model, year, price, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (make, model, year, price, status))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))

    return render_template('add_car.html')

# Маршрут за добавяне на разходи за кола
@app.route('/add_expense/<int:car_id>', methods=['GET', 'POST'])
def add_expense(car_id):
    if request.method == 'POST':
        expense_date = request.form['expense_date']
        amount = request.form['amount']
        description = request.form['description']
        
        conn = sqlite3.connect('cars.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO Car_Expenses (car_id, expense_date, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (car_id, expense_date, amount, description))
        conn.commit()
        conn.close()
        
        return redirect(url_for('view_expenses', car_id=car_id))

    return render_template('add_expense.html', car_id=car_id)

# Маршрут за показване на разходите за конкретна кола
@app.route('/car/<int:car_id>/expenses')
def view_expenses(car_id):
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()

    c.execute('SELECT * FROM Cars WHERE id = ?', (car_id,))
    car = c.fetchone()

    c.execute('SELECT * FROM Car_Expenses WHERE car_id = ?', (car_id,))
    expenses = c.fetchall()

    conn.close()
    return render_template('view_expenses.html', car=car, expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)

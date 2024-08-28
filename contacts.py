from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Contact

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phonebook.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        new_contact = Contact(name=name, phone=phone)
        db.session.add(new_contact)
        db.session.commit()
        flash('Contact added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone = request.form['phone']
        db.session.commit()
        flash('Contact updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7555)




from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MariaDB connection setup
def get_db_connection():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='#LAZIsky4470',
        database='PhoneBook'
    )
    if connection.is_connected():
        return connection
    else:
        raise Error("Could not connect to the database")

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Contacts')
    contacts = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Contacts (name, phone) VALUES (%s, %s)', (name, phone))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Contact added successfully!'}), 201
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        cursor.execute('UPDATE Contacts SET name = %s, phone = %s WHERE id = %s', (name, phone, id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Contact updated successfully!'}), 200
    cursor.execute('SELECT * FROM Contacts WHERE id = %s', (id,))
    contact = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete_contact(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Contacts WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'Contact deleted successfully!'}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7555, debug = True)

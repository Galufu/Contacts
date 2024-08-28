from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
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

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    contacts_list = [{'id': contact.id, 'name': contact.name, 'phone': contact.phone} for contact in contacts]
    return jsonify(contacts_list), 200

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
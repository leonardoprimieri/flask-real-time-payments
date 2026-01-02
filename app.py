from flask import Flask, jsonify, request, send_file, render_template
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'APP_SECRET_KEY'

db.init_app(app)

@app.route('/payments/pix', methods=['POST'])
def create_pix_payment():
    data = request.get_json()

    if 'value' not in data:
        return jsonify({"message": "Invalid value."}), 400

    current_date_plus_30_mins = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value=data['value'], expiration_date=current_date_plus_30_mins)

    pix = Pix()
    pix_data = pix.register_payment_on_partner_bank()
    new_payment.bank_payment_id = pix_data['bank_payment_id']
    new_payment.qr_code = pix_data['qr_code_path']

    db.session.add(new_payment)
    db.session.commit()


    return jsonify({"message": "Payment successfully created.", "payment": new_payment.to_dict()})

@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_image_qr_code(file_name):
    return send_file(f'static/img/{file_name}.png', mimetype='image/png')

@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation():
    return jsonify({"message": "Payment created."})

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
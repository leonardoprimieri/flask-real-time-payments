from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
    return jsonify({"message": "Payment created."})

@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation():
    return jsonify({"message": "Payment created."})

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    return f'<h1>Pix ID: {payment_id}</h1>'

if __name__ == '__main__':
    app.run(debug=True, port=8000)
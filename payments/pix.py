import uuid
import qrcode

class Pix:
    def __init__(self):
        pass

    @staticmethod
    def create_payment():
        bank_payment_id = str(uuid.uuid4())

        qr_code_image_name = f'qr_code_{bank_payment_id}'

        payment_hash =  f'payment_hash_{bank_payment_id}'

        qr_code = qrcode.make(payment_hash)
        qr_code.save(f'static/img/{qr_code_image_name}.png')

        return {
            "bank_payment_id": bank_payment_id,
            "qr_code_path": qr_code_image_name
        }
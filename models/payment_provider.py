import requests
from odoo import models, fields
from odoo.http import request

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('multisafepay', "MultiSafepay")], ondelete={'multisafepay': 'set default'})
    multisafepay_api_key = fields.Char("MultiSafepay API Key")


    def multisafepay_create_order(self, transaction_id):
        print('3multisafepay_create_order')
        self.ensure_one()
        print('self.ensure_one()',self.ensure_one())
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print('self.ensure_one()',base_url)
        print('=')

        payload = {
            "type": "redirect",
            "order_id": transaction_id.reference,
            "currency": transaction_id.currency_id.name,
            # "currency": 'EUR',
            "amount": int(transaction_id.amount * 100),
            "description": f"Order {transaction_id.reference}",
            "customer": {"locale": "en_US"},
            "payment_options": {
                "notification_url": f"{base_url}/payment/multisafepay/webhook",
                "redirect_url": f"{base_url}/payment/multisafepay/return",
                "cancel_url": f"{base_url}/payment/multisafepay/cancel",
                "notification_method": "POST"
            }
        }
        print('payload',payload)

        headers = {'api_key': self.multisafepay_api_key, 'Content-Type': 'application/json'}
        print('headers',headers)
        responce = requests.post("https://testapi.multisafepay.com/v1/json/orders/", headers=headers, json=payload)
        print('resp',responce.status_code)
        print('resp',responce.text)
        print('resp',responce.json())


        result = responce.json().get('data') or {}
        print('result')
        print(result)
        transaction_id.provider_reference = result.get('order_id')
        print('transaction_id.provider_reference',transaction_id.provider_reference)
        print('result.get('')',result.get('payment_url'))
        return result.get('payment_url')


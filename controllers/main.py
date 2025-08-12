import requests
from werkzeug.utils import redirect
from odoo import http
from odoo.http import request


class MultiSafepayController(http.Controller):
    @http.route('/payment/multisafepay/redirect/<int:transaction_id>', type='http', auth='public')
    def multisafepay_redirect(self, transaction_id):
        print('2multisafepay_redirect')
        transaction = request.env['payment.transaction'].sudo().browse(transaction_id)
        if not transaction or transaction.provider_id.code != 'multisafepay':
            return request.redirect('/shop/payment')
        redirect_url = transaction.provider_id.multisafepay_create_order(transaction)
        return redirect(redirect_url)



    @http.route('/payment/multisafepay/return', type='http', auth='public')
    def multisafepay_return(self, **kwargs):
        print('multisafepay_return')
        order_id = kwargs.get('transactionid')

        transaction_id = request.env['payment.transaction'].sudo().search([('reference', '=', order_id)], limit=1)
        if transaction_id:
            provider = transaction_id.provider_id
            api_key = provider.multisafepay_api_key
            headers = {'api_key': api_key, 'Content-Type': 'application/json'}
            resp = requests.get(f"https://testapi.multisafepay.com/v1/json/orders/{order_id}", headers=headers)

            if resp.status_code == 200:
                data = resp.json().get('data', {})
                transaction_id.provider_reference = data.get('transaction_id')
            transaction_id._set_done()
        return request.redirect('/payment/status')


    @http.route('/payment/multisafepay/cancel', type='http', auth='public')
    def multisafepay_cancel(self, **kwargs):
        print('multisafepay_cancel')
        reference = kwargs.get('order_id') or kwargs.get('transactionid')
        transaction_id = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)
        transaction_id._set_canceled()
        return request.redirect('/payment/status?cancel=true')
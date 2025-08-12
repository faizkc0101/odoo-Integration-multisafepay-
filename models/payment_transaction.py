from odoo import models

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        print('1,_get_specific_rendering_values')
        rendering_values = super()._get_specific_rendering_values(processing_values)
        print(processing_values)

        if self.provider_code == 'multisafepay':
            return {
                'provider_id': self.provider_id.id,
                'payment_method_id': self.payment_method_id.id ,
                'flow': 'redirect',
                'api_url': f"/payment/multisafepay/redirect/{self.id}",
                'return_url': processing_values.get("return_url", "/payment/status"),
                'reference': self.reference,
                'partner_id': self.partner_id.id,
                'amount': self.amount,
                'currency_id': self.currency_id.id,
            }
        return rendering_values



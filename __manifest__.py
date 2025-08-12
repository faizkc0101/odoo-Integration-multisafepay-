{
    "name": "Multisafepay",
    "version": "1.0",
    "depends": ["payment", "website_sale"],
    "sequence": 1,
    "category": "Payment",
    "summary": "Integration with Multisafepay ",
    "data": [
        'data/payment_provider.xml',
        "data/payment_method.xml",
        "views/multisafepay_template.xml",
        "views/paymeny_provider_view.xml",
    ],
    "installable": True,
    "application": False
}

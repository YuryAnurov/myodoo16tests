# -*- coding: utf-8 -*-
{
    'name': 'estate',
    'version': '1.0',
    'summary': 'short one',
    'description': 'Description of estate',
    'depends': ['base',
                ],
    'data': [
        'views/estate_property_views.xml',
        'views/estate_view.xml',
        'views/estate_form.xml',
        'views/estate_search.xml',
        # порядок критичен, снчала action, потом меню, которое на него ссылается
        'views/estate_type_property_views.xml',
        'views/tags_views.xml',
        'views/offer_form.xml',
        'views/offer_view.xml',
        'views/estate_menus.xml',
        'views/estate_type_view.xml',
        'views/estate_type_form.xml',
        # 'reports/report.xml',
        # 'reports/report_card.xml',
        'security/ir.model.access.csv',
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

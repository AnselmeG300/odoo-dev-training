# -*- coding: utf-8 -*-
{
    'name': 'Estate',
    'depends': ['base'],
    'category': 'Tutorials',
    'version': '1.0',
    'summary': 'Real Estate Management',
    'description': """
    Module for managing real estate properties, offers, types, and tags.    
    """,
    'author': 'Anselme Gildas TCHASSEM BOUTCHOUANG',
    'license': 'LGPL-3',
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'data/estate.property.csv',
        'data/estate.property.type.csv',
        'data/estate.property.tag.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ]
}
{
    'name': 'estate',
    'depends': ['base'],
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
    ],
}

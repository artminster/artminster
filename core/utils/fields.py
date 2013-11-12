from django.utils.translation import ugettext as _
from django.db import models, connection
from django.utils.text import capfirst
from itertools import chain
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode, smart_unicode
from django import forms
from itertools import chain
from django.conf import settings
from django.contrib.admin import widgets
from django.utils.html import escape
from django.forms.fields import EMPTY_VALUES, Field
from django.forms import ValidationError
from django.db.models.signals import post_delete, post_save
from south.modelsinspector import add_introspection_rules
from django.db.models import OneToOneField
from django.db.models.fields.related import SingleRelatedObjectDescriptor

qn = connection.ops.quote_name

import re

uk_landline_re = re.compile(r'^[0]{1}[1-9]{1}[0-9]{9}$')
uk_landline_no08or09_re = re.compile(r'^[0]{1}[1-7]{1}[0-9]{9}$')
uk_mobile_re = re.compile(r'^(07)[0-9]{9}')
international_number_re = re.compile(r'^[+]?([0-9]*[\.\s\-\(\)]|[0-9]+){3,24}$')

from django.db.models import OneToOneField
from django.db.models.fields.related import SingleRelatedObjectDescriptor


class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
    def __get__(self, instance, instance_type=None):
        try:
            return super(AutoSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
        except self.related.model.DoesNotExist:
            obj = self.related.model(**{self.related.field.name: instance})
            obj.save()
            return obj


class AutoOneToOneField(OneToOneField):
    '''
    OneToOneField creates related object on first call if it doesnt exist yet.
    Use it instead of original OneToOne field.

    example:
        
        class MyProfile(models.Model):
            user = AutoOneToOneField(User, primary_key=True)
            home_page = models.URLField(max_length=255, blank=True)
            icq = models.IntegerField(max_length=255, null=True)
    '''
    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        from south.modelsinspector import introspector
        field_class = OneToOneField.__module__ + "." + OneToOneField.__name__
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


            
# ISO 3166-1 country names and codes adapted from http://opencountrycodes.appspot.com/python/
COUNTRIES = [
    ('GB', _('United Kingdom')),
    ('US', _('United States')),
    ('AF', _('Afghanistan')), 
    ('AX', _('Aland Islands')), 
    ('AL', _('Albania')), 
    ('DZ', _('Algeria')), 
    ('AS', _('American Samoa')), 
    ('AD', _('Andorra')), 
    ('AO', _('Angola')), 
    ('AI', _('Anguilla')), 
    ('AQ', _('Antarctica')), 
    ('AG', _('Antigua and Barbuda')), 
    ('AR', _('Argentina')), 
    ('AM', _('Armenia')), 
    ('AW', _('Aruba')), 
    ('AU', _('Australia')), 
    ('AT', _('Austria')), 
    ('AZ', _('Azerbaijan')), 
    ('BS', _('Bahamas')), 
    ('BH', _('Bahrain')), 
    ('BD', _('Bangladesh')), 
    ('BB', _('Barbados')), 
    ('BY', _('Belarus')), 
    ('BE', _('Belgium')), 
    ('BZ', _('Belize')), 
    ('BJ', _('Benin')), 
    ('BM', _('Bermuda')), 
    ('BT', _('Bhutan')), 
    ('BO', _('Bolivia')), 
    ('BA', _('Bosnia and Herzegovina')), 
    ('BW', _('Botswana')), 
    ('BV', _('Bouvet Island')), 
    ('BR', _('Brazil')), 
    ('BN', _('Brunei Darussalam')), 
    ('BG', _('Bulgaria')), 
    ('BF', _('Burkina Faso')), 
    ('BI', _('Burundi')), 
    ('KH', _('Cambodia')), 
    ('CM', _('Cameroon')), 
    ('CA', _('Canada')), 
    ('CV', _('Cape Verde')), 
    ('KY', _('Cayman Islands')), 
    ('CF', _('Central African Republic')), 
    ('TD', _('Chad')), 
    ('CL', _('Chile')), 
    ('CN', _('China')), 
    ('CX', _('Christmas Island')), 
    ('CC', _('Cocos Islands')), 
    ('CO', _('Colombia')), 
    ('KM', _('Comoros')), 
    ('CG', _('Congo')), 
    ('CD', _('Congo')), 
    ('CK', _('Cook Islands')), 
    ('CR', _('Costa Rica')), 
    ('CI', _("Cote d'Ivoire")), 
    ('HR', _('Croatia')), 
    ('CU', _('Cuba')), 
    ('CY', _('Cyprus')), 
    ('CZ', _('Czech Republic')), 
    ('DK', _('Denmark')), 
    ('DJ', _('Djibouti')), 
    ('DM', _('Dominica')), 
    ('DO', _('Dominican Republic')), 
    ('EC', _('Ecuador')), 
    ('EG', _('Egypt')), 
    ('SV', _('El Salvador')), 
    ('GQ', _('Equatorial Guinea')), 
    ('ER', _('Eritrea')), 
    ('EE', _('Estonia')), 
    ('ET', _('Ethiopia')), 
    ('FK', _('Falkland Islands')), 
    ('FO', _('Faroe Islands')), 
    ('FJ', _('Fiji')), 
    ('FI', _('Finland')), 
    ('FR', _('France')), 
    ('GF', _('French Guiana')), 
    ('PF', _('French Polynesia')), 
    ('GA', _('Gabon')), 
    ('GM', _('Gambia')), 
    ('GE', _('Georgia')), 
    ('DE', _('Germany')), 
    ('GH', _('Ghana')), 
    ('GI', _('Gibraltar')), 
    ('GR', _('Greece')), 
    ('GL', _('Greenland')), 
    ('GD', _('Grenada')), 
    ('GP', _('Guadeloupe')), 
    ('GU', _('Guam')), 
    ('GT', _('Guatemala')), 
    ('GG', _('Guernsey')), 
    ('GN', _('Guinea')), 
    ('GW', _('Guinea-Bissau')), 
    ('GY', _('Guyana')), 
    ('HT', _('Haiti')),
    ('HN', _('Honduras')), 
    ('HK', _('Hong Kong')), 
    ('HU', _('Hungary')), 
    ('IS', _('Iceland')), 
    ('IN', _('India')), 
    ('ID', _('Indonesia')), 
    ('IR', _('Iran')), 
    ('IQ', _('Iraq')), 
    ('IE', _('Ireland')), 
    ('IM', _('Isle of Man')), 
    ('IL', _('Israel')), 
    ('IT', _('Italy')), 
    ('JM', _('Jamaica')), 
    ('JP', _('Japan')), 
    ('JE', _('Jersey')), 
    ('JO', _('Jordan')), 
    ('KZ', _('Kazakhstan')), 
    ('KE', _('Kenya')), 
    ('KI', _('Kiribati')), 
    ('KP', _('Korea')), 
    ('KR', _('Korea, Republic of')), 
    ('KW', _('Kuwait')), 
    ('KG', _('Kyrgyzstan')), 
    ('LA', _('Lao')), 
    ('LV', _('Latvia')), 
    ('LB', _('Lebanon')), 
    ('LS', _('Lesotho')), 
    ('LR', _('Liberia')), 
    ('LY', _('Libyan Arab Jamahiriya')), 
    ('LI', _('Liechtenstein')), 
    ('LT', _('Lithuania')), 
    ('LU', _('Luxembourg')), 
    ('MO', _('Macao')), 
    ('MK', _('Macedonia')), 
    ('MG', _('Madagascar')), 
    ('MW', _('Malawi')), 
    ('MY', _('Malaysia')), 
    ('MV', _('Maldives')), 
    ('ML', _('Mali')), 
    ('MT', _('Malta')), 
    ('MH', _('Marshall Islands')), 
    ('MQ', _('Martinique')), 
    ('MR', _('Mauritania')), 
    ('MU', _('Mauritius')), 
    ('YT', _('Mayotte')), 
    ('MX', _('Mexico')), 
    ('MD', _('Moldova')), 
    ('MC', _('Monaco')), 
    ('MN', _('Mongolia')), 
    ('ME', _('Montenegro')), 
    ('MS', _('Montserrat')), 
    ('MA', _('Morocco')), 
    ('MZ', _('Mozambique')), 
    ('MM', _('Myanmar')), 
    ('NA', _('Namibia')), 
    ('NR', _('Nauru')), 
    ('NP', _('Nepal')), 
    ('NL', _('Netherlands')), 
    ('AN', _('Netherlands Antilles')), 
    ('NC', _('New Caledonia')), 
    ('NZ', _('New Zealand')), 
    ('NI', _('Nicaragua')), 
    ('NE', _('Niger')), 
    ('NG', _('Nigeria')), 
    ('NU', _('Niue')), 
    ('NF', _('Norfolk Island')), 
    ('MP', _('Northern Mariana Islands')), 
    ('NO', _('Norway')), 
    ('OM', _('Oman')), 
    ('PK', _('Pakistan')), 
    ('PW', _('Palau')),  
    ('PA', _('Panama')), 
    ('PG', _('Papua New Guinea')), 
    ('PY', _('Paraguay')), 
    ('PE', _('Peru')), 
    ('PH', _('Philippines')), 
    ('PN', _('Pitcairn')), 
    ('PL', _('Poland')), 
    ('PT', _('Portugal')), 
    ('PR', _('Puerto Rico')), 
    ('QA', _('Qatar')), 
    ('RE', _('Reunion')), 
    ('RO', _('Romania')), 
    ('RU', _('Russian Federation')), 
    ('RW', _('Rwanda')), 
    ('BL', _('Saint Barthelemy')), 
    ('SH', _('Saint Helena')), 
    ('KN', _('Saint Kitts and Nevis')), 
    ('LC', _('Saint Lucia')), 
    ('MF', _('Saint Martin')), 
    ('WS', _('Samoa')), 
    ('SM', _('San Marino')), 
    ('ST', _('Sao Tome and Principe')), 
    ('SA', _('Saudi Arabia')), 
    ('SN', _('Senegal')), 
    ('RS', _('Serbia')), 
    ('SC', _('Seychelles')), 
    ('SL', _('Sierra Leone')), 
    ('SG', _('Singapore')), 
    ('SK', _('Slovakia')), 
    ('SI', _('Slovenia')), 
    ('SB', _('Solomon Islands')), 
    ('SO', _('Somalia')), 
    ('ZA', _('South Africa')),  
    ('ES', _('Spain')), 
    ('LK', _('Sri Lanka')), 
    ('SD', _('Sudan')), 
    ('SR', _('Suriname')), 
    ('SJ', _('Svalbard and Jan Mayen')), 
    ('SZ', _('Swaziland')), 
    ('SE', _('Sweden')), 
    ('CH', _('Switzerland')), 
    ('SY', _('Syrian Arab Republic')), 
    ('TW', _('Taiwan')), 
    ('TJ', _('Tajikistan')), 
    ('TZ', _('Tanzania')), 
    ('TH', _('Thailand')), 
    ('TL', _('Timor-Leste')), 
    ('TG', _('Togo')), 
    ('TK', _('Tokelau')), 
    ('TO', _('Tonga')), 
    ('TT', _('Trinidad and Tobago')), 
    ('TN', _('Tunisia')), 
    ('TR', _('Turkey')), 
    ('TM', _('Turkmenistan')), 
    ('TC', _('Turks and Caicos Islands')), 
    ('TV', _('Tuvalu')), 
    ('UG', _('Uganda')), 
    ('UA', _('Ukraine')), 
    ('AE', _('United Arab Emirates')),
    ('UY', _('Uruguay')), 
    ('UZ', _('Uzbekistan')), 
    ('VU', _('Vanuatu')), 
    ('VE', _('Venezuela')), 
    ('VN', _('Viet Nam')), 
    ('VG', _('Virgin Islands, British')), 
    ('VI', _('Virgin Islands, U.S.')), 
    ('WF', _('Wallis and Futuna')), 
    ('EH', _('Western Sahara')), 
    ('YE', _('Yemen')), 
    ('ZM', _('Zambia')), 
    ('ZW', _('Zimbabwe')), 
]

class CountryField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', COUNTRIES)

        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"
        

# SOUTH INTROSPECTION RULES
add_introspection_rules([], ["^filebrowser\.fields\.FileBrowseField"])
add_introspection_rules([], ["^artminster\.core\.utils\.fields\.CountryField"])
from .models import User, City, Property, Review, Amenity
from modeltranslation.translator import TranslationOptions,register

@register(User)
class ProductTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name')

@register(City)
class ProductTranslationOptions(TranslationOptions):
    fields = ('city_name',)

@register(Property)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Review)
class ProductTranslationOptions(TranslationOptions):
    fields = ('comment',)

@register(Amenity)
class ProductTranslationOptions(TranslationOptions):
    fields = ('amenity_name',)
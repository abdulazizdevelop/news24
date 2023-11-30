
from modeltranslation.translator import register , TranslationOptions
from .models import Category, Tags, News


@register(News)
class NewsTranslationOptions(TranslationOptions):
    field= ('title', 'body')
    
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    field = ('name',)
    
    
    
@register(Tags)
class TagsTranslationOptions(TranslationOptions):
    field = ('name',)
    

from django.contrib import admin
from .models import Legend,Planeswalker,GreenSpells,BlueSpells,BlackSpells,WhiteSpells,RedSpells,ColorlessSpells,MulticolorSpells

# Register your models here.
admin.site.register(Legend)
admin.site.register(Planeswalker) 
admin.site.register(GreenSpells) 
admin.site.register(BlueSpells) 
admin.site.register(BlackSpells) 
admin.site.register(WhiteSpells) 
admin.site.register(RedSpells) 
admin.site.register(ColorlessSpells) 
admin.site.register(MulticolorSpells)  
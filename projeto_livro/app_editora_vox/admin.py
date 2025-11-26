from django.contrib import admin
from app_editora_vox.models import Autor, Editora, Livro, Publica

# Register your models here.

admin.site.site_header = "Administração da Editora Vox"
admin.site.site_title = "Administração da Editora Vox"

admin.site.register(Autor)
admin.site.register(Livro)
admin.site.register(Editora)
admin.site.register(Publica)
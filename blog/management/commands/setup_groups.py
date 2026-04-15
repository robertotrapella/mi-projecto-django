from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Article


class Command(BaseCommand):
    help = 'Crea los grupos y permisos iniciales'

    def handle(self, *args, **options):
        ct = ContentType.objects.get_for_model(Article)

        # --- Grupo: Lector ---
        lector, created = Group.objects.get_or_create(name='Lector')
        lector.permissions.set([
            Permission.objects.get(codename='view_article', content_type=ct),
        ])
        self.stdout.write(f'Grupo "Lector": {"creado" if created else "actualizado"}')

        # --- Grupo: Escritor ---
        escritor, created = Group.objects.get_or_create(name='Escritor')
        escritor.permissions.set([
            Permission.objects.get(codename='view_article', content_type=ct),
            Permission.objects.get(codename='add_article', content_type=ct),
            Permission.objects.get(codename='change_article', content_type=ct),
        ])
        self.stdout.write(f'Grupo "Escritor": {"creado" if created else "actualizado"}')

        # --- Grupo: Editor ---
        editor, created = Group.objects.get_or_create(name='Editor')
        editor.permissions.set([
            Permission.objects.get(codename='view_article', content_type=ct),
            Permission.objects.get(codename='add_article', content_type=ct),
            Permission.objects.get(codename='change_article', content_type=ct),
            Permission.objects.get(codename='delete_article', content_type=ct),
            Permission.objects.get(codename='publish_article', content_type=ct),
            Permission.objects.get(codename='feature_article', content_type=ct),
        ])
        self.stdout.write(f'Grupo "Editor": {"creado" if created else "actualizado"}')

        self.stdout.write(self.style.SUCCESS('Grupos configurados correctamente.'))
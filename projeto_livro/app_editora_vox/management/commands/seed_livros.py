import random
from decimal import Decimal, ROUND_HALF_UP

from django.core.management.base import BaseCommand, CommandError

try:
    from faker import Faker
    from faker.providers import date_time, isbn, lorem
except ImportError:  # fallback amigavel quando Faker nao esta instalado
    Faker = None
    date_time = isbn = lorem = None

from app_editora_vox.models import Editora, Livro


class Command(BaseCommand):
    help = 'Gera registros falsos de livros usando Faker.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quantidade',
            type=int,
            default=100,
            help='Numero de livros a serem criados (padrao: 100).',
        )

    def handle(self, *args, **options):
        if Faker is None:
            raise CommandError('Biblioteca Faker nao encontrada. Instale com "pip install Faker".')

        quantidade = options['quantidade']
        fake = Faker('pt_BR')
        fake.add_provider(isbn)
        fake.add_provider(lorem)
        fake.add_provider(date_time)

        editoras = list(Editora.objects.all())
        if not editoras:
            # Cria editoras basicas quando a base esta vazia para manter a integridade referencial.
            for _ in range(3):
                editoras.append(Editora.objects.create(nome=fake.company()))
            self.stdout.write(self.style.WARNING('Nenhuma editora existente. Foram criadas editoras ficticias.'))

        novos_livros = []
        for _ in range(quantidade):
            preco_float = fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=10, max_value=400)
            preco = Decimal(str(preco_float)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            novos_livros.append(
                Livro(
                    ISBN=fake.unique.isbn13(separator=''),
                    titulo=fake.sentence(nb_words=6).rstrip('.'),
                    publicacao=fake.date_between(start_date='-10y', end_date='today'),
                    preco=preco,
                    estoque=random.randint(0, 200),
                    editora=random.choice(editoras),
                )
            )

        criados = Livro.objects.bulk_create(novos_livros, ignore_conflicts=True)
        fake.unique.clear()

        self.stdout.write(self.style.SUCCESS(f'{len(criados)} livros foram gerados com sucesso.'))

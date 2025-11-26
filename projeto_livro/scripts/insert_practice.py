import os
import sys
from pathlib import Path
import django
from decimal import Decimal


def setup_django():
    # Garantir que o diretório raiz do projeto esteja em sys.path quando
    # o script for executado diretamente (sys.path[0] = pasta do script)
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_livro.settings')
    django.setup()


def main():
    setup_django()

    from app_editora_vox.models import Autor, Editora, Livro, Publica

    print('--- Inserções: criar um registro em cada tabela ---')
    # Criar editora
    editora, created = Editora.objects.get_or_create(nome='Editora Exemplo')
    print(f'Editora: id={editora.id}, nome={editora.nome} (created={created})')

    # Criar autor
    autor, created = Autor.objects.get_or_create(nome='José Machado')
    print(f'Autor: id={autor.id}, nome={autor.nome} (created={created})')

    # Criar livro
    livro, created = Livro.objects.get_or_create(
        ISBN='9780000000001',
        defaults={
            'titulo': 'Livro de Exemplo',
            'publicacao': '2020-01-01',
            'preco': Decimal('49.90'),
            'estoque': 10,
            'editora': editora,
        }
    )
    print(f'Livro: id={livro.id}, titulo={livro.titulo}, ISBN={livro.ISBN} (created={created})')

    # Criar publica (ligação autor-livro)
    publica, created = Publica.objects.get_or_create(livro=livro, autor=autor)
    print(f'Publica: livro_id={publica.livro.id}, autor_id={publica.autor.id} (created={created})')

    print('\n--- Listar todos os livros cadastrados ---')
    for l in Livro.objects.all():
        print(f'id={l.id} | ISBN={l.ISBN} | titulo={l.titulo} | preco={l.preco} | editora_id={l.editora.id}')

    print('\n--- Listar todos autores que possuem "Machado" no nome ---')
    autores_machado = Autor.objects.filter(nome__icontains='Machado')
    for a in autores_machado:
        print(f'id={a.id} | nome={a.nome}')

    print('\n--- Listar todos os autores de um livro, dado o seu ISBN ---')
    isbn_busca = '9780000000001'
    try:
        livro_busca = Livro.objects.get(ISBN=isbn_busca)
        autores_do_livro = Autor.objects.filter(publica__livro=livro_busca).distinct()
        print(f'Autores do livro ISBN={isbn_busca}:')
        for a in autores_do_livro:
            print(f' - id={a.id} | nome={a.nome}')
    except Livro.DoesNotExist:
        print(f'Livro com ISBN {isbn_busca} não encontrado')

    print('\n--- Atualizar o nome de uma determinada editora, dado seu id ---')
    editora_id = editora.id
    nova_nome = 'Editora Exemplo Atualizada'
    Editora.objects.filter(id=editora_id).update(nome=nova_nome)
    editora.refresh_from_db()
    print(f'Editora atualizada: id={editora.id} | nome={editora.nome}')

    print('\n--- Atualizar, em 10%, os preços dos livros de uma determinada editora ---')
    editora_para_aumento_id = editora.id
    livros_da_editora = Livro.objects.filter(editora__id=editora_para_aumento_id)
    for l in livros_da_editora:
        old = l.preco
        novo = (old * Decimal('1.10')).quantize(Decimal('0.01'))
        Livro.objects.filter(id=l.id).update(preco=novo)
        print(f'Livro id={l.id} | preco antiga={old} -> nova={novo}')

    print('\n--- Remover todas as publicações de um determinado autor ---')
    autor_para_remover = autor  # usamos o autor criado acima
    pub_count = Publica.objects.filter(autor=autor_para_remover).count()
    Publica.objects.filter(autor=autor_para_remover).delete()
    print(f'Removidas {pub_count} publicações do autor id={autor_para_remover.id} nome={autor_para_remover.nome}')


if __name__ == '__main__':
    main()

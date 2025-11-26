from django.db import models


class Editora(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.id})"


class Livro(models.Model):
    id = models.AutoField(primary_key=True)
    ISBN = models.CharField(max_length=13, unique=True)
    titulo = models.CharField(max_length=200)
    publicacao = models.DateField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    estoque = models.IntegerField()
    editora = models.ForeignKey(Editora, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} ({self.id})"


class Autor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.id})"


class Publica(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('livro', 'autor')  

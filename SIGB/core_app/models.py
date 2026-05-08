from django.db import models
from simple_history.models import HistoricalRecords


class Historico(models.Model):
    historico = HistoricalRecords(inherit=True)

    def get_nome_modulo(self):
        if self.instance:
            return self.instance._meta.verbose_name
        return "Módulo"

    def get_identificador(self):
        return (
            getattr(self, 'nome_completo', None) or 
            getattr(self, 'prefixo', None) or 
            getattr(self, 'titulo', None) or 
            getattr(self, 'nome', None) or 
            getattr(self, 'tipo', None) or 
            f"ID: {self.id}"
        )

    class Meta:
        abstract = True

class Patente(Historico):
    nome = models.CharField(max_length=100)
    nivel = models.PositiveIntegerField()

    def __str__(self):
        return str(self.nome)


class Perfil(Historico):
    nivel = models.CharField(max_length=20)

    def __str__(self):
        return str(self.nivel)


class Bombeiro(Historico):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=255, unique=True)
    data_ingresso = models.DateField()
    tipo_sanguineo = models.CharField(max_length=3)
    status = models.CharField(max_length=100)
    patente = models.ForeignKey(Patente, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nome_completo)


class Viatura(Historico):
    prefixo = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=50)
    placa = models.CharField(max_length=7, unique=True)
    tipo = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

    def __str__(self):
        return str(self.prefixo + " " + self.modelo)


class Manutencao(Historico):
    viatura = models.ForeignKey(Viatura, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    descricao = models.TextField()
    tipo = models.CharField(max_length=30, unique=False)
    status = models.CharField(max_length=30, unique=False)
    
    def __str__(self):
        return str(self.viatura)


class TipoEvento(Historico):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.nome)


class Evento(Historico):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    local = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.titulo)


class EventoBombeiro(Historico):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    bombeiro = models.ForeignKey(Bombeiro, on_delete=models.CASCADE)
    funcao = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.evento)


class ViaturaEvento(Historico):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    viatura = models.ForeignKey(Viatura, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.evento)


class Ocorrencia(Historico):
    tipo = models.CharField(max_length=100)
    gravidade = models.CharField(max_length=10)
    descricao = models.TextField()
    vitimas = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.tipo)


class Escala(Historico):
    nome = models.CharField(max_length=200, default="")
    data_inicio = models.DateField()
    data_fim = models.DateField()
    descricao = models.TextField(default="")
    
    def __str__(self):
        return str(self.nome)


class EscalaBombeiro(Historico):
    escala = models.ForeignKey(Escala, on_delete=models.CASCADE)
    bombeiro = models.ForeignKey(Bombeiro, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.bombeiro)


class Treinamento(Historico):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    
    def __str__(self):
        return str(self.nome)


class TreinamentoBombeiro(Historico):
    bombeiro = models.ForeignKey(Bombeiro, on_delete=models.CASCADE)
    treinamento = models.ForeignKey(Treinamento, on_delete=models.CASCADE)
    data_conclusao = models.DateField()
    
    def __str__(self):
        return str(self.bombeiro)

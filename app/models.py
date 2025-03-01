from app import db
from datetime import datetime


#tabela pesquisa
class Pesquisa(db.Model):
    __tablename__ = 'pesquisa' #especificando o nome da tabela
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #indentificador único
    usuario_id=db.Column(db.Integer, db.ForeignKey('usuario.id'),nullable=False) #ligação com o usuario
    origem = db.Column(db.String(300), nullable=False)
    destino = db.Column(db.String(300), nullable=False)
    data_e_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    filtros = db.relationship('Filtros',backref='pesquisa',lazy=True)
    historico = db.relationship('HistoricoPesquisa', back_populates='pesquisa', lazy=True, cascade="all, delete-orphan")
    resultados = db.relationship('ResultadoPesquisa', backref='pesquisa', lazy=True)


    def __repr__(self):
        return f"<Pesquisa {self.id} - {self.origem} -> {self.destino}>"
    
class Filtros(db.Model):
    __tablename__ = 'filtros'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    pesquisa_id = db.Column(db.Integer,db.ForeignKey('pesquisa.id',ondelete="CASCADE"),nullable=False)

    modo_transporte = db.Column(db.Enum('carro','moto','bicicleta','ônibus','a pé',),nullable=False)
    evitar_rodovias = db.Column(db.Boolean,nullable=False,default=False)
    evitar_transito_pesado = db.Column(db.Boolean,nullable=False,default=False)
    evitar_pedagios = db.Column(db.Boolean,nullable=False,default=False)
    evitar_estradas_nao_pavimentadas = db.Column(db.Boolean,nullable=False,default=False)
    rota_mais_curta = db.Column(db.Boolean,nullable=False,default=False)
    rota_mais_longa = db.Column(db.Boolean,nullable=False,default=False)

    def __repr__(self):
        return f"<Filtros {self.id} - {self.pesquisa_id}>"
    
    @staticmethod
    def validar_rotas(rota_curta, rota_longa):
        if rota_curta and rota_longa:
            raise ValueError("A pesquisa não pode ter as opções 'rota mais curta' e 'rota mais longa' ativadas ao mesmo tempo.")
        
class HistoricoPesquisa(db.Model):
    __tablename__ = "historico_pesquisa"
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    usuario_id=db.Column(db.Integer, db.ForeignKey('usuario.id'),nullable=False)
    pesquisa_id = db.Column(db.Integer, db.ForeignKey('pesquisa.id', ondelete='CASCADE'),nullable=False)
    data_pesquisa = db.Column(db.DateTime, default=datetime.utcnow,nullable=False)
    vezes_pesquisada = db.Column(db.Integer, nullable=False,default=1)

    # Relacionamento com a tabela Usuario
    usuario = db.relationship('Usuario', back_populates='historico_pesquisa')

    # Relacionamento com a tabela Pesquisa
    pesquisa = db.relationship('Pesquisa', back_populates='historico')

    def __repr__(self):
        return f"<HistoricoPesquisa{self.id} - Pesquisa {self.pesquisa_id} ({self.vezes_pesquisada} vezes)>"
    
class ResultadoPesquisa(db.Model):
    __tablename__ = "resultado_pesquisa"
    id = db.Column(db.Integer , primary_key=True , autoincrement = True)# Identificador único
    pesquisa_id = db.Column(db.Integer , db.ForeignKey('pesquisa.id') , nullable=False)# Relacionamento com a pesquisa
    rota = db.Column(db.String(300), nullable=False) # JSON com detalhes da rota
    distancia = db.Column(db.Float, nullable=False) # Distância total da rota (km)
    duracao = db.Column(db.Integer, nullable=False)  # Tempo total estimado da rota (em minutos)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # Data e hora do armazenamento

    def __repr__(self):
        return f"<ResultadoPesquisa {self.id} - Rota {self.rota[:50]}... (Distancia: {self.distancia} km , Tempo: {self.duracao}min)>"
    
    def format_for_use(self):
        return {
            'id': self.id,
            'rota': self.rota[:50] + '...',  # Resumo da rota
            'distancia': f"{self.distancia} km", # Exibe a distância
            'duracao': f"{self.duracao} minutos", # Exibe a duração
            'criado_em': self.criado_em.strftime("%d/%m/%Y %H:%M") # Formata a data de criação
        }

class Usuario(db.Model):
    __tablename__="usuario"
    id=db.Column(db.Integer, primary_key=True, autoincrement = True)
    nome= db.Column(db.String(50), nullable=False)
    #relacionamento com pesquisa
    pesquisa=db.relationship('Pesquisa',backref='usuario',lazy=True)
    #relacionamento com historico_pesquisa
    historico_pesquisa=db.relationship('HistoricoPesquisa', back_populates='usuario',lazy=True)

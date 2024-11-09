from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, UTC

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    data_registro = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    # Relacionamento com inscrições
    inscricoes = db.relationship('Inscricao', backref='aluno', lazy=True)

class Oficina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    professor = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    dia_semana = db.Column(db.String(20), nullable=False)
    vagas_total = db.Column(db.Integer, nullable=False)
    vagas_disponiveis = db.Column(db.Integer, nullable=False)
    imagem = db.Column(db.String(200))
    categoria = db.Column(db.String(50))  # ex: 'dança', 'música', 'financeiro'
    ativa = db.Column(db.Boolean, default=True)
    # Relacionamento com inscrições
    inscricoes = db.relationship('Inscricao', backref='oficina', lazy=True)

class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    oficina_id = db.Column(db.Integer, db.ForeignKey('oficina.id'), nullable=False)
    data_inscricao = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    status = db.Column(db.String(20), default='ativa')  # ativa, cancelada, concluída

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    assunto = db.Column(db.String(255), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_envio = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
class SolicitacaoCredito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    finalidade = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    renda = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Em Análise')
    data_solicitacao = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    usuario = db.relationship('Usuario', backref='solicitacoes_credito')

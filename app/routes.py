from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.models import Usuario, Oficina, Inscricao, Contato, SolicitacaoCredito
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/projetos')
def projetos():
    return render_template('projetos.html')
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        assunto = request.form.get('assunto')
        mensagem = request.form.get('mensagem')

        novo_contato = Contato(
            nome=nome,
            email=email,
            assunto=assunto,
            mensagem=mensagem
        )

        try:
            db.session.add(novo_contato)
            db.session.commit()
            flash('Mensagem enviada com sucesso!', 'success')
        except:
            db.session.rollback()
            flash('Erro ao enviar mensagem. Tente novamente.', 'danger')

        return redirect(url_for('contato'))

    return render_template('contato.html')

@app.route('/banco')
def banco():
    return render_template('banco.html')


from app.models import Usuario, Oficina, Inscricao, Contato, SolicitacaoCredito  # Atualize o import


@app.route('/solicitar-credito', methods=['GET', 'POST'])
@login_required
def solicitar_credito():
    if request.method == 'POST':
        nova_solicitacao = SolicitacaoCredito(
            usuario_id=current_user.id,
            valor=float(request.form.get('valor')),
            finalidade=request.form.get('finalidade'),
            descricao=request.form.get('descricao'),
            renda=float(request.form.get('renda'))
        )

        try:
            db.session.add(nova_solicitacao)
            db.session.commit()
            flash('Solicitação enviada com sucesso! Entraremos em contato em breve.', 'success')
            return redirect(url_for('banco'))
        except:
            db.session.rollback()
            flash('Erro ao enviar solicitação. Tente novamente.', 'danger')

    return render_template('solicitar_credito.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos', 'danger')

    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado', 'danger')
        else:
            senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')
            usuario = Usuario(nome=nome, email=email, senha=senha_hash)
            db.session.add(usuario)
            db.session.commit()
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Rotas de Oficinas
@app.route('/oficinas')
def oficinas():
    # Busca todas as oficinas ativas do banco
    todas_oficinas = Oficina.query.filter_by(ativa=True).all()
    return render_template('oficinas.html', oficinas=todas_oficinas)

@app.route('/oficina/<int:oficina_id>')
def oficina_detalhes(oficina_id):
    oficina = Oficina.query.get_or_404(oficina_id)
    outras_oficinas = Oficina.query.filter(Oficina.id != oficina_id).limit(3).all()

    ja_inscrito = False
    if current_user.is_authenticated:
        ja_inscrito = Inscricao.query.filter_by(
            aluno_id=current_user.id,
            oficina_id=oficina_id,
            status='ativa'
        ).first() is not None

    return render_template('oficina_detalhes.html',
                         oficina=oficina,
                         outras_oficinas=outras_oficinas,
                         ja_inscrito=ja_inscrito)


@app.route('/oficina/<int:oficina_id>/inscrever', methods=['POST'])
@login_required
def inscrever_oficina(oficina_id):
    # Verifica se o usuário está logado
    if not current_user.is_authenticated:
        flash('Por favor, faça login para se inscrever.', 'warning')
        return redirect(url_for('login'))

    oficina = Oficina.query.get_or_404(oficina_id)

    # Verifica se já está inscrito
    inscricao_existente = Inscricao.query.filter_by(
        aluno_id=current_user.id,
        oficina_id=oficina_id,
        status='ativa'
    ).first()

    if inscricao_existente:
        flash('Você já está inscrito nesta oficina!', 'info')
        return redirect(url_for('minhas_oficinas'))

    # Verifica vagas disponíveis
    if oficina.vagas_disponiveis <= 0:
        flash('Desculpe, não há mais vagas disponíveis.', 'warning')
        return redirect(url_for('oficinas'))

    # Cria nova inscrição
    nova_inscricao = Inscricao(aluno_id=current_user.id, oficina_id=oficina_id)
    oficina.vagas_disponiveis -= 1

    try:
        db.session.add(nova_inscricao)
        db.session.commit()
        flash('Inscrição realizada com sucesso!', 'success')
    except:
        db.session.rollback()
        flash('Erro ao realizar inscrição. Tente novamente.', 'danger')

    return redirect(url_for('minhas_oficinas'))


@app.route('/minhas-oficinas')
@login_required
def minhas_oficinas():
    inscricoes = Inscricao.query.filter_by(
        aluno_id=current_user.id,
        status='ativa'
    ).all()
    return render_template('minhas_oficinas.html', inscricoes=inscricoes)


@app.route('/cancelar-inscricao/<int:inscricao_id>', methods=['POST'])
@login_required
def cancelar_inscricao(inscricao_id):
    inscricao = Inscricao.query.get_or_404(inscricao_id)

    # Verifica se a inscrição pertence ao usuário logado
    if inscricao.aluno_id != current_user.id:
        flash('Você não tem permissão para cancelar esta inscrição.', 'danger')
        return redirect(url_for('minhas_oficinas'))

    # Atualiza vagas disponíveis da oficina
    oficina = Oficina.query.get(inscricao.oficina_id)
    oficina.vagas_disponiveis += 1

    # Cancela a inscrição
    inscricao.status = 'cancelada'

    try:
        db.session.commit()
        flash('Inscrição cancelada com sucesso!', 'success')
    except:
        db.session.rollback()
        flash('Erro ao cancelar inscrição. Tente novamente.', 'danger')

    return redirect(url_for('minhas_oficinas'))
@app.route('/debug/oficinas')
def debug_oficinas():
    oficinas = Oficina.query.all()
    for oficina in oficinas:
        print(f"ID: {oficina.id} - Nome: {oficina.nome}")
    return "Check console"
from app import app, db, login_manager
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import Contato, Produto, Usuario

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/quem_somos')
def quem_somos():
  return render_template('quem_somos.html')

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
  produtos = Produto.query.all()
  return render_template('produtos.html', produtos=produtos)


@app.route('/add_usuario', methods=['GET', 'POST'])
@login_required
def add_usuario():
  if not current_user.is_authenticated:
    return current_app.login_manager.unauthorized()

  if request.method == 'POST':
    usuario = request.form['usuario']
    senha = request.form['senha']
    user = Usuario(usuario=usuario, senha=senha)
    db.session.add(user)
    db.session.commit()
    flash("Usuário cadastrado com sucesso!")
    return redirect(url_for('home'))

  return render_template('add_usuario.html')


@app.route('/add_produto', methods=['GET', 'POST'])
@login_required
def add_produto():
  if not current_user.is_authenticated:
    return current_app.login_manager.unauthorized()

  if request.method == 'POST':
    codigo = request.form["codigo"]
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    preco = request.form["preco"]
    foto = request.form["foto"]
    produto = Produto(codigo=codigo, nome=nome, descricao=descricao, preco=preco, foto=foto)
    db.session.add(produto)
    db.session.commit()
    flash("Produto cadastrado com sucesso!")
    return redirect(url_for('add_produto'))
  return render_template('add_produto.html')


@app.route('/contato', methods=['GET', 'POST'])
def contato():
  if request.method == 'POST':
    nome = request.form["nome"]
    cidade = request.form["cidade"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    mensagem = request.form["mensagem"]
    contato = Contato(nome=nome, cidade=cidade, telefone=telefone, email=email, mensagem=mensagem)
    db.session.add(contato)
    db.session.commit()
    flash("Mensagem enviada com sucesso!")
    return redirect(url_for('contato'))
  return render_template('contato.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    usuario = request.form['usuario']
    pwd = request.form['senha']
    user = Usuario.query.filter_by(usuario=usuario).first()
    if not user or not user.verify_password(pwd):
      flash("Usuário ou senha inválidos!")
      return redirect(url_for('login'))
    login_user(user)
    flash("Bem-vindo! Voce está logado!")
    return redirect(url_for('home'))

  return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/info')
def info():
  return render_template('info.html')


@app.route('/admin')
@login_required
def admin():
  if current_user.is_authenticated:
    return render_template('admin/index.html')
  else:
    return current_app.login_manager.unauthorized()


from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placar_igreja.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
db = SQLAlchemy(app)

# Modelos do Banco de Dados
class Equipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    pontuacao_total = db.Column(db.Integer, default=0)
    registros = db.relationship('Registro', backref='equipe', lazy=True)
    
    @property
    def divisao(self):
        """Calcula a divisão baseada na pontuação (top 5 = A, resto = B)"""
        todas_equipes = Equipe.query.order_by(Equipe.pontuacao_total.desc()).all()
        posicao = todas_equipes.index(self) + 1
        return 'A' if posicao <= 5 else 'B'

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Quantidade de pessoas e pessoas novas
    qtd_pessoas = db.Column(db.Integer, default=0)
    qtd_pessoas_novas = db.Column(db.Integer, default=0)
    
    # Células Elite
    qtd_celulas_elite = db.Column(db.Integer, default=0)
    
    # Terça-feira
    qtd_pessoas_terca = db.Column(db.Integer, default=0)
    qtd_pessoas_novas_terca = db.Column(db.Integer, default=0)
    
    # Arena
    qtd_pessoas_arena = db.Column(db.Integer, default=0)
    qtd_pessoas_novas_arena = db.Column(db.Integer, default=0)
    
    # Domingo
    qtd_pessoas_domingo = db.Column(db.Integer, default=0)
    qtd_pessoas_novas_domingo = db.Column(db.Integer, default=0)
    
    # Parceiro de Deus (valor arrecadado)
    valor_arrecadacao_parceiro = db.Column(db.Float, default=0.0)
    
    # Pontuação calculada
    pontuacao = db.Column(db.Integer, default=0)

# Sistema de pontuação
PONTUACAO_CONFIG = {
    'pessoas_novas': 10,
    'celulas_elite': 15,
    'pessoas_terca': 5,
    'pessoas_novas_terca': 10,
    'pessoas_arena': 8,
    'pessoas_novas_arena': 15,
    'pessoas_domingo': 3,
    'pessoas_novas_domingo': 8,
    'valor_arrecadacao': 0.1  # 0.1 ponto por real arrecadado
}

def calcular_pontuacao(registro):
    """Calcula a pontuação baseada nos novos critérios estabelecidos"""
    pontos = 0
    
    # Pessoas novas (geral)
    pontos += registro.qtd_pessoas_novas * PONTUACAO_CONFIG['pessoas_novas']
    
    # Células Elite
    pontos += registro.qtd_celulas_elite * PONTUACAO_CONFIG['celulas_elite']
    
    # Terça-feira
    pontos += registro.qtd_pessoas_terca * PONTUACAO_CONFIG['pessoas_terca']
    pontos += registro.qtd_pessoas_novas_terca * PONTUACAO_CONFIG['pessoas_novas_terca']
    
    # Arena
    pontos += registro.qtd_pessoas_arena * PONTUACAO_CONFIG['pessoas_arena']
    pontos += registro.qtd_pessoas_novas_arena * PONTUACAO_CONFIG['pessoas_novas_arena']
    
    # Domingo
    pontos += registro.qtd_pessoas_domingo * PONTUACAO_CONFIG['pessoas_domingo']
    pontos += registro.qtd_pessoas_novas_domingo * PONTUACAO_CONFIG['pessoas_novas_domingo']
    
    # Parceiro de Deus (valor arrecadado)
    pontos += registro.valor_arrecadacao_parceiro * PONTUACAO_CONFIG['valor_arrecadacao']
    
    return int(pontos)

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/placar')
def placar():
    # Busca todas as equipes ordenadas por pontuação
    todas_equipes = Equipe.query.order_by(Equipe.pontuacao_total.desc()).all()
    
    # Top 5 = Divisão A, resto = Divisão B
    equipes_a = todas_equipes[:5]
    equipes_b = todas_equipes[5:]
    
    return render_template('placar.html', equipes_a=equipes_a, equipes_b=equipes_b)

@app.route('/cadastrar_equipe', methods=['GET', 'POST'])
def cadastrar_equipe():
    if request.method == 'POST':
        nome = request.form['nome']
        
        nova_equipe = Equipe(nome=nome)
        db.session.add(nova_equipe)
        db.session.commit()
        
        flash(f'Equipe {nome} cadastrada com sucesso!', 'success')
        return redirect(url_for('placar'))
    
    return render_template('cadastrar_equipe.html')

@app.route('/registrar_atividade', methods=['GET', 'POST'])
def registrar_atividade():
    if request.method == 'POST':
        from datetime import datetime
        
        equipe_id = request.form['equipe_id']
        data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date()
        data_fim = datetime.strptime(request.form['data_fim'], '%Y-%m-%d').date()
        
        # Coleta os dados do formulário
        qtd_pessoas = int(request.form.get('qtd_pessoas', 0))
        qtd_pessoas_novas = int(request.form.get('qtd_pessoas_novas', 0))
        qtd_celulas_elite = int(request.form.get('qtd_celulas_elite', 0))
        qtd_pessoas_terca = int(request.form.get('qtd_pessoas_terca', 0))
        qtd_pessoas_novas_terca = int(request.form.get('qtd_pessoas_novas_terca', 0))
        qtd_pessoas_arena = int(request.form.get('qtd_pessoas_arena', 0))
        qtd_pessoas_novas_arena = int(request.form.get('qtd_pessoas_novas_arena', 0))
        qtd_pessoas_domingo = int(request.form.get('qtd_pessoas_domingo', 0))
        qtd_pessoas_novas_domingo = int(request.form.get('qtd_pessoas_novas_domingo', 0))
        valor_arrecadacao_parceiro = float(request.form.get('valor_arrecadacao_parceiro', 0))
        
        # Cria o registro
        novo_registro = Registro(
            equipe_id=equipe_id,
            data_inicio=data_inicio,
            data_fim=data_fim,
            qtd_pessoas=qtd_pessoas,
            qtd_pessoas_novas=qtd_pessoas_novas,
            qtd_celulas_elite=qtd_celulas_elite,
            qtd_pessoas_terca=qtd_pessoas_terca,
            qtd_pessoas_novas_terca=qtd_pessoas_novas_terca,
            qtd_pessoas_arena=qtd_pessoas_arena,
            qtd_pessoas_novas_arena=qtd_pessoas_novas_arena,
            qtd_pessoas_domingo=qtd_pessoas_domingo,
            qtd_pessoas_novas_domingo=qtd_pessoas_novas_domingo,
            valor_arrecadacao_parceiro=valor_arrecadacao_parceiro
        )
        
        # Calcula a pontuação
        novo_registro.pontuacao = calcular_pontuacao(novo_registro)
        
        # Salva no banco
        db.session.add(novo_registro)
        
        # Atualiza pontuação total da equipe
        equipe = Equipe.query.get(equipe_id)
        equipe.pontuacao_total += novo_registro.pontuacao
        
        db.session.commit()
        
        flash(f'Atividade registrada! Pontos ganhos: {novo_registro.pontuacao}', 'success')
        return redirect(url_for('placar'))
    
    equipes = Equipe.query.all()
    return render_template('registrar_atividade.html', equipes=equipes)

@app.route('/historico/<int:equipe_id>')
def historico_equipe(equipe_id):
    equipe = Equipe.query.get_or_404(equipe_id)
    registros = Registro.query.filter_by(equipe_id=equipe_id).order_by(Registro.data_registro.desc()).all()
    return render_template('historico.html', equipe=equipe, registros=registros)

@app.route('/editar_equipe/<int:equipe_id>', methods=['GET', 'POST'])
def editar_equipe(equipe_id):
    equipe = Equipe.query.get_or_404(equipe_id)
    
    if request.method == 'POST':
        nome_antigo = equipe.nome
        equipe.nome = request.form['nome']
        
        db.session.commit()
        
        flash(f'Equipe "{nome_antigo}" atualizada para "{equipe.nome}" com sucesso!', 'success')
        return redirect(url_for('placar'))
    
    return render_template('editar_equipe.html', equipe=equipe)

@app.route('/relatorios')
def relatorios():
    equipes = Equipe.query.all()
    return render_template('relatorios.html', equipes=equipes)

@app.route('/relatorio_periodo', methods=['POST'])
def relatorio_periodo():
    from datetime import datetime
    
    data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date()
    data_fim = datetime.strptime(request.form['data_fim'], '%Y-%m-%d').date()
    equipe_id = request.form.get('equipe_id')
    
    # Filtrar registros por período
    query = Registro.query.filter(
        Registro.data_inicio >= data_inicio,
        Registro.data_fim <= data_fim
    )
    
    if equipe_id:
        query = query.filter(Registro.equipe_id == equipe_id)
    
    registros = query.order_by(Registro.data_registro.desc()).all()
    equipes = Equipe.query.all()
    
    return render_template('relatorio_resultado.html', 
                         registros=registros, 
                         equipes=equipes,
                         data_inicio=data_inicio,
                         data_fim=data_fim,
                         equipe_selecionada=equipe_id)

@app.route('/excluir_equipe/<int:equipe_id>', methods=['POST'])
def excluir_equipe(equipe_id):
    equipe = Equipe.query.get_or_404(equipe_id)
    nome_equipe = equipe.nome
    
    # Excluir todos os registros da equipe primeiro
    Registro.query.filter_by(equipe_id=equipe_id).delete()
    
    # Excluir a equipe
    db.session.delete(equipe)
    db.session.commit()
    
    flash(f'Equipe "{nome_equipe}" excluída com sucesso!', 'success')
    return redirect(url_for('placar'))

@app.route('/api/pontuacao_config')
def api_pontuacao_config():
    return jsonify(PONTUACAO_CONFIG)

def init_db():
    """Inicializa o banco de dados limpo para produção"""
    db.create_all()
    print("Banco de dados inicializado e pronto para produção!")

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=False, host='0.0.0.0', port=5001)

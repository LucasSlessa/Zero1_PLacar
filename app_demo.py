from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

# Dados em memória para demonstração (simula Google Sheets)
equipes_data = []
registros_data = []

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
    pontos += registro.get('qtd_pessoas_novas', 0) * PONTUACAO_CONFIG['pessoas_novas']
    
    # Células Elite
    pontos += registro.get('qtd_celulas_elite', 0) * PONTUACAO_CONFIG['celulas_elite']
    
    # Terça-feira
    pontos += registro.get('qtd_pessoas_terca', 0) * PONTUACAO_CONFIG['pessoas_terca']
    pontos += registro.get('qtd_pessoas_novas_terca', 0) * PONTUACAO_CONFIG['pessoas_novas_terca']
    
    # Arena
    pontos += registro.get('qtd_pessoas_arena', 0) * PONTUACAO_CONFIG['pessoas_arena']
    pontos += registro.get('qtd_pessoas_novas_arena', 0) * PONTUACAO_CONFIG['pessoas_novas_arena']
    
    # Domingo
    pontos += registro.get('qtd_pessoas_domingo', 0) * PONTUACAO_CONFIG['pessoas_domingo']
    pontos += registro.get('qtd_pessoas_novas_domingo', 0) * PONTUACAO_CONFIG['pessoas_novas_domingo']
    
    # Parceiro de Deus (valor arrecadado)
    pontos += registro.get('valor_arrecadacao_parceiro', 0) * PONTUACAO_CONFIG['valor_arrecadacao']
    
    return int(pontos)

def get_equipes(data_inicio=None, data_fim=None):
    """Obtém todas as equipes ordenadas por pontuação (total ou por período)"""
    if data_inicio and data_fim:
        # Busca pontuação por período
        equipes = get_equipes_por_periodo(data_inicio, data_fim)
    else:
        # Busca pontuação total (comportamento original)
        equipes = sorted(equipes_data, key=lambda x: x.get('pontuacao_total', 0), reverse=True)
    
    # Adiciona divisão baseada na posição
    for i, equipe in enumerate(equipes):
        equipe['divisao'] = 'A' if i < 5 else 'B'
        equipe['posicao'] = i + 1
    
    return equipes

def get_equipes_por_periodo(data_inicio, data_fim):
    """Obtém equipes com pontuação calculada para um período específico"""
    # Cria cópia das equipes para não modificar os dados originais
    equipes = []
    for equipe_original in equipes_data:
        equipe = equipe_original.copy()
        
        # Calcula pontuação no período
        pontuacao_periodo = 0
        registros_periodo = 0
        
        for registro in registros_data:
            if (registro['equipe_id'] == equipe['id'] and 
                data_inicio <= registro['data_inicio'] <= data_fim):
                pontuacao_periodo += registro['pontuacao']
                registros_periodo += 1
        
        equipe['pontuacao_periodo'] = pontuacao_periodo
        equipe['registros_periodo'] = registros_periodo
        equipes.append(equipe)
    
    # Ordena por pontuação do período
    equipes.sort(key=lambda x: x.get('pontuacao_periodo', 0), reverse=True)
    
    return equipes

def get_equipe_by_id(equipe_id):
    """Obtém uma equipe específica pelo ID"""
    for equipe in equipes_data:
        if str(equipe.get('id')) == str(equipe_id):
            return equipe
    return None

def criar_equipe(nome):
    """Cria uma nova equipe"""
    novo_id = max([e.get('id', 0) for e in equipes_data], default=0) + 1
    
    nova_equipe = {
        'id': novo_id,
        'nome': nome,
        'pontuacao_total': 0,
        'data_criacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    equipes_data.append(nova_equipe)
    return True

def atualizar_pontuacao_equipe(equipe_id, pontos_adicionais):
    """Atualiza a pontuação de uma equipe"""
    for equipe in equipes_data:
        if str(equipe.get('id')) == str(equipe_id):
            equipe['pontuacao_total'] = equipe.get('pontuacao_total', 0) + pontos_adicionais
            return True
    return False

def criar_registro(dados):
    """Cria um novo registro de atividade"""
    novo_id = max([r.get('id', 0) for r in registros_data], default=0) + 1
    
    # Calcula pontuação
    pontuacao = calcular_pontuacao(dados)
    
    # Obtém nome da equipe
    equipe = get_equipe_by_id(dados['equipe_id'])
    equipe_nome = equipe['nome'] if equipe else 'Desconhecida'
    
    # Cria registro
    novo_registro = {
        'id': novo_id,
        'equipe_id': dados['equipe_id'],
        'equipe_nome': equipe_nome,
        'data_inicio': dados['data_inicio'],
        'data_fim': dados['data_fim'],
        'data_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'qtd_pessoas': dados.get('qtd_pessoas', 0),
        'qtd_pessoas_novas': dados.get('qtd_pessoas_novas', 0),
        'qtd_celulas_elite': dados.get('qtd_celulas_elite', 0),
        'qtd_pessoas_terca': dados.get('qtd_pessoas_terca', 0),
        'qtd_pessoas_novas_terca': dados.get('qtd_pessoas_novas_terca', 0),
        'qtd_pessoas_arena': dados.get('qtd_pessoas_arena', 0),
        'qtd_pessoas_novas_arena': dados.get('qtd_pessoas_novas_arena', 0),
        'qtd_pessoas_domingo': dados.get('qtd_pessoas_domingo', 0),
        'qtd_pessoas_novas_domingo': dados.get('qtd_pessoas_novas_domingo', 0),
        'valor_arrecadacao_parceiro': dados.get('valor_arrecadacao_parceiro', 0),
        'pontuacao': pontuacao
    }
    
    registros_data.append(novo_registro)
    
    # Atualiza pontuação da equipe
    atualizar_pontuacao_equipe(dados['equipe_id'], pontuacao)
    
    return pontuacao

# Rotas Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/placar')
def placar():
    # Verifica se há filtros de período
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Obtém equipes (total ou por período)
    equipes = get_equipes(data_inicio, data_fim)
    equipes_a = [e for e in equipes if e.get('divisao') == 'A']
    equipes_b = [e for e in equipes if e.get('divisao') == 'B']
    
    # Informações do período para o template
    periodo_info = {
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'is_periodo': bool(data_inicio and data_fim)
    }
    
    return render_template('placar.html', 
                         equipes_a=equipes_a, 
                         equipes_b=equipes_b, 
                         periodo=periodo_info)

@app.route('/placar_periodo', methods=['POST'])
def placar_periodo():
    """Rota para filtrar placar por período"""
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    
    return redirect(url_for('placar', data_inicio=data_inicio, data_fim=data_fim))

@app.route('/cadastrar_equipe', methods=['GET', 'POST'])
def cadastrar_equipe():
    if request.method == 'POST':
        nome = request.form['nome']
        
        if criar_equipe(nome):
            flash(f'Equipe {nome} cadastrada com sucesso!', 'success')
        else:
            flash('Erro ao cadastrar equipe.', 'error')
        
        return redirect(url_for('placar'))
    
    return render_template('cadastrar_equipe.html')

@app.route('/registrar_atividade', methods=['GET', 'POST'])
def registrar_atividade():
    if request.method == 'POST':
        dados = {
            'equipe_id': request.form['equipe_id'],
            'data_inicio': request.form['data_inicio'],
            'data_fim': request.form['data_fim'],
            'qtd_pessoas': int(request.form.get('qtd_pessoas', 0)),
            'qtd_pessoas_novas': int(request.form.get('qtd_pessoas_novas', 0)),
            'qtd_celulas_elite': int(request.form.get('qtd_celulas_elite', 0)),
            'qtd_pessoas_terca': int(request.form.get('qtd_pessoas_terca', 0)),
            'qtd_pessoas_novas_terca': int(request.form.get('qtd_pessoas_novas_terca', 0)),
            'qtd_pessoas_arena': int(request.form.get('qtd_pessoas_arena', 0)),
            'qtd_pessoas_novas_arena': int(request.form.get('qtd_pessoas_novas_arena', 0)),
            'qtd_pessoas_domingo': int(request.form.get('qtd_pessoas_domingo', 0)),
            'qtd_pessoas_novas_domingo': int(request.form.get('qtd_pessoas_novas_domingo', 0)),
            'valor_arrecadacao_parceiro': float(request.form.get('valor_arrecadacao_parceiro', 0))
        }
        
        pontuacao = criar_registro(dados)
        if pontuacao:
            flash(f'Atividade registrada! Pontos ganhos: {pontuacao}', 'success')
        else:
            flash('Erro ao registrar atividade.', 'error')
        
        return redirect(url_for('placar'))
    
    equipes = get_equipes()
    return render_template('registrar_atividade.html', equipes=equipes)

@app.route('/relatorios')
def relatorios():
    equipes = get_equipes()
    return render_template('relatorios.html', equipes=equipes)

@app.route('/relatorio_periodo', methods=['POST'])
def relatorio_periodo():
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    equipe_id = request.form.get('equipe_id')
    
    # Filtra registros por período
    registros_filtrados = []
    for registro in registros_data:
        if data_inicio <= registro['data_inicio'] <= data_fim:
            if not equipe_id or str(registro['equipe_id']) == str(equipe_id):
                registros_filtrados.append(registro)
    
    equipes = get_equipes()
    
    return render_template('relatorio_resultado.html', 
                         registros=registros_filtrados, 
                         equipes=equipes,
                         data_inicio=datetime.strptime(data_inicio, '%Y-%m-%d').date(),
                         data_fim=datetime.strptime(data_fim, '%Y-%m-%d').date(),
                         equipe_selecionada=equipe_id)

@app.route('/editar_equipe/<int:equipe_id>', methods=['GET', 'POST'])
def editar_equipe(equipe_id):
    equipe = get_equipe_by_id(equipe_id)
    if not equipe:
        flash('Equipe não encontrada!', 'error')
        return redirect(url_for('placar'))
    
    if request.method == 'POST':
        nome_antigo = equipe['nome']
        equipe['nome'] = request.form['nome']
        
        flash(f'Equipe "{nome_antigo}" atualizada para "{equipe["nome"]}" com sucesso!', 'success')
        return redirect(url_for('placar'))
    
    return render_template('editar_equipe.html', equipe=equipe)

@app.route('/excluir_equipe/<int:equipe_id>', methods=['POST'])
def excluir_equipe(equipe_id):
    equipe = get_equipe_by_id(equipe_id)
    if not equipe:
        flash('Equipe não encontrada!', 'error')
        return redirect(url_for('placar'))
    
    nome_equipe = equipe['nome']
    
    # Remove equipe
    equipes_data[:] = [e for e in equipes_data if e['id'] != equipe_id]
    
    # Remove registros da equipe
    registros_data[:] = [r for r in registros_data if r['equipe_id'] != equipe_id]
    
    flash(f'Equipe "{nome_equipe}" excluída com sucesso!', 'success')
    return redirect(url_for('placar'))

@app.route('/historico/<int:equipe_id>')
def historico_equipe(equipe_id):
    equipe = get_equipe_by_id(equipe_id)
    if not equipe:
        flash('Equipe não encontrada!', 'error')
        return redirect(url_for('placar'))
    
    # Filtra registros da equipe
    registros = [r for r in registros_data if r['equipe_id'] == equipe_id]
    registros.sort(key=lambda x: x['data_registro'], reverse=True)
    
    return render_template('historico.html', equipe=equipe, registros=registros)

@app.route('/status')
def status():
    """Rota para verificar status do sistema"""
    status_info = {
        'modo': 'demonstracao',
        'equipes_cadastradas': len(equipes_data),
        'registros_total': len(registros_data),
        'google_sheets_connected': False
    }
    return jsonify(status_info)

@app.route('/api/pontuacao_config')
def api_pontuacao_config():
    return jsonify(PONTUACAO_CONFIG)

if __name__ == '__main__':
    print("🚀 ZERO 1 iniciado em MODO DEMONSTRAÇÃO!")
    print("📊 Os dados ficam apenas na memória (serão perdidos ao reiniciar)")
    print("🔧 Para usar Google Sheets, configure seguindo GOOGLE_SHEETS_SETUP.md")
    print("🌐 Acesse: http://localhost:5003")
    
    app.run(debug=False, host='0.0.0.0', port=5003)

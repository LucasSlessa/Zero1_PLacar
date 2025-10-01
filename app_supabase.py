from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from supabase import create_client, Client
from datetime import datetime, date
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

# Configuração do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Sistema de pontuação
PONTUACAO_CONFIG = {
    'pessoas_novas': 10,
    'celulas_realizadas': 10,
    'celulas_elite': 10,
    'pessoas_terca': 10,
    'pessoas_novas_terca': 10,
    'pessoas_arena': 10,
    'pessoas_novas_arena': 10,
    'pessoas_domingo': 10,
    'pessoas_novas_domingo': 10,
    'valor_arrecadacao': 10  # 10 pontos por real arrecadado
}

def calcular_pontuacao(registro):
    """Calcula a pontuação baseada nos novos critérios estabelecidos"""
    pontos = 0
    
    # Pessoas novas (geral)
    pontos += registro.get('qtd_pessoas_novas', 0) * PONTUACAO_CONFIG['pessoas_novas']
    
    # Células Realizadas
    pontos += registro.get('qtd_celulas_realizadas', 0) * PONTUACAO_CONFIG['celulas_realizadas']
    
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

def init_database():
    """Inicializa as tabelas no Supabase"""
    try:
        # Verifica se as tabelas existem tentando fazer uma consulta
        supabase.table('equipes').select('*').limit(1).execute()
        print("✅ Tabelas já existem no Supabase!")
        return True
    except Exception as e:
        print("⚠️  Tabelas não encontradas. Você precisa criar as tabelas no Supabase.")
        print("📋 Execute os comandos SQL no painel do Supabase:")
        print("""
-- Criar tabela de equipes
CREATE TABLE equipes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    logo_url TEXT,
    pontuacao_total INTEGER DEFAULT 0,
    data_criacao TIMESTAMP DEFAULT NOW(),
    data_atualizacao TIMESTAMP DEFAULT NOW()
);

-- Criar tabela de registros
CREATE TABLE registros (
    id SERIAL PRIMARY KEY,
    equipe_id INTEGER REFERENCES equipes(id) ON DELETE CASCADE,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    data_registro TIMESTAMP DEFAULT NOW(),
    qtd_pessoas INTEGER DEFAULT 0,
    qtd_pessoas_novas INTEGER DEFAULT 0,
    qtd_celulas_elite INTEGER DEFAULT 0,
    qtd_pessoas_terca INTEGER DEFAULT 0,
    qtd_pessoas_novas_terca INTEGER DEFAULT 0,
    qtd_pessoas_arena INTEGER DEFAULT 0,
    qtd_pessoas_novas_arena INTEGER DEFAULT 0,
    qtd_pessoas_domingo INTEGER DEFAULT 0,
    qtd_pessoas_novas_domingo INTEGER DEFAULT 0,
    valor_arrecadacao_parceiro DECIMAL(10,2) DEFAULT 0,
    pontuacao INTEGER DEFAULT 0
);

-- Habilitar RLS (Row Level Security) - opcional
ALTER TABLE equipes ENABLE ROW LEVEL SECURITY;
ALTER TABLE registros ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas as operações (para desenvolvimento)
CREATE POLICY "Enable all operations for equipes" ON equipes FOR ALL USING (true);
CREATE POLICY "Enable all operations for registros" ON registros FOR ALL USING (true);
        """)
        return False

def get_equipes(data_inicio=None, data_fim=None):
    """Obtém todas as equipes ordenadas por pontuação (total ou por período)"""
    try:
        if data_inicio and data_fim:
            # Busca pontuação por período
            equipes = get_equipes_por_periodo(data_inicio, data_fim)
        else:
            # Busca pontuação total (comportamento original)
            response = supabase.table('equipes').select('*').order('pontuacao_total', desc=True).execute()
            equipes = response.data
        
        # Adiciona divisão baseada na posição
        for i, equipe in enumerate(equipes):
            equipe['divisao'] = 'A' if i < 5 else 'B'
            equipe['posicao'] = i + 1
        
        return equipes
    except Exception as e:
        print(f"Erro ao obter equipes: {e}")
        return []

def get_equipes_por_periodo(data_inicio, data_fim):
    """Obtém equipes com pontuação calculada para um período específico"""
    try:
        # Busca todas as equipes
        response_equipes = supabase.table('equipes').select('*').execute()
        equipes = response_equipes.data
        
        # Para cada equipe, calcula pontuação no período
        for equipe in equipes:
            # Busca registros da equipe no período
            response_registros = supabase.table('registros').select('pontuacao').eq('equipe_id', equipe['id']).gte('data_inicio', data_inicio).lte('data_fim', data_fim).execute()
            
            # Soma pontuação do período
            pontuacao_periodo = sum(registro['pontuacao'] for registro in response_registros.data)
            equipe['pontuacao_periodo'] = pontuacao_periodo
            
            # Conta registros no período
            equipe['registros_periodo'] = len(response_registros.data)
        
        # Ordena por pontuação do período
        equipes.sort(key=lambda x: x.get('pontuacao_periodo', 0), reverse=True)
        
        return equipes
    except Exception as e:
        print(f"Erro ao obter equipes por período: {e}")
        return []

def get_equipe_by_id(equipe_id):
    """Obtém uma equipe específica pelo ID"""
    try:
        response = supabase.table('equipes').select('*').eq('id', equipe_id).execute()
        if response.data:
            equipe = response.data[0]
            # Adiciona divisão
            todas_equipes = get_equipes()
            for i, e in enumerate(todas_equipes):
                if e['id'] == equipe['id']:
                    equipe['divisao'] = 'A' if i < 5 else 'B'
                    equipe['posicao'] = i + 1
                    break
            return equipe
        return None
    except Exception as e:
        print(f"Erro ao obter equipe: {e}")
        return None

def criar_equipe(nome, logo_url=None):
    """Cria uma nova equipe com logo opcional"""
    try:
        equipe_data = {
            'nome': nome,
            'pontuacao_total': 0,
            'logo_url': logo_url or ''
        }
        response = supabase.table('equipes').insert(equipe_data).execute()
        if response.data:
            print(f"✅ Equipe '{nome}' criada com sucesso no Supabase!")
            return True
        return False
    except Exception as e:
        print(f"❌ Erro ao criar equipe no Supabase: {e}")
        return False

def atualizar_pontuacao_equipe(equipe_id, pontos_adicionais):
    """Atualiza a pontuação de uma equipe"""
    try:
        # Busca pontuação atual
        response = supabase.table('equipes').select('pontuacao_total').eq('id', equipe_id).execute()
        if response.data:
            pontuacao_atual = response.data[0]['pontuacao_total']
            nova_pontuacao = pontuacao_atual + pontos_adicionais
            
            # Atualiza pontuação
            supabase.table('equipes').update({
                'pontuacao_total': nova_pontuacao
            }).eq('id', equipe_id).execute()
            return True
        return False
    except Exception as e:
        print(f"Erro ao atualizar pontuação: {e}")
        return False

def criar_registro(dados):
    """Cria um novo registro de atividade"""
    try:
        # Calcula pontuação
        pontuacao = calcular_pontuacao(dados)
        
        # Cria registro
        response = supabase.table('registros').insert({
            'equipe_id': dados['equipe_id'],
            'data_inicio': dados['data_inicio'],
            'data_fim': dados['data_fim'],
            'qtd_pessoas': dados.get('qtd_pessoas', 0),
            'qtd_pessoas_novas': dados.get('qtd_pessoas_novas', 0),
            'qtd_celulas': dados.get('qtd_celulas', 0),
            'qtd_celulas_realizadas': dados.get('qtd_celulas_realizadas', 0),
            'qtd_celulas_elite': dados.get('qtd_celulas_elite', 0),
            'qtd_pessoas_terca': dados.get('qtd_pessoas_terca', 0),
            'qtd_pessoas_novas_terca': dados.get('qtd_pessoas_novas_terca', 0),
            'qtd_pessoas_arena': dados.get('qtd_pessoas_arena', 0),
            'qtd_pessoas_novas_arena': dados.get('qtd_pessoas_novas_arena', 0),
            'qtd_pessoas_domingo': dados.get('qtd_pessoas_domingo', 0),
            'qtd_pessoas_novas_domingo': dados.get('qtd_pessoas_novas_domingo', 0),
            'valor_arrecadacao_parceiro': dados.get('valor_arrecadacao_parceiro', 0),
            'pontuacao': pontuacao
        }).execute()
        
        if response.data:
            # Atualiza pontuação da equipe
            atualizar_pontuacao_equipe(dados['equipe_id'], pontuacao)
            return pontuacao
        return False
    except Exception as e:
        print(f"Erro ao criar registro: {e}")
        return False

def get_registros_por_periodo(data_inicio, data_fim, equipe_id=None):
    """Obtém registros filtrados por período"""
    try:
        query = supabase.table('registros').select('*, equipes(nome)').gte('data_inicio', data_inicio).lte('data_fim', data_fim)
        
        if equipe_id:
            query = query.eq('equipe_id', equipe_id)
        
        response = query.order('data_registro', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Erro ao obter registros: {e}")
        return []

def get_registros_equipe(equipe_id):
    """Obtém registros de uma equipe específica"""
    try:
        response = supabase.table('registros').select('*').eq('equipe_id', equipe_id).order('data_registro', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Erro ao obter registros da equipe: {e}")
        return []

def editar_equipe(equipe_id, nome, logo_url=None):
    """Edita o nome e/ou logo de uma equipe"""
    try:
        update_data = {'nome': nome, 'data_atualizacao': datetime.now().isoformat()}
        if logo_url is not None:
            update_data['logo_url'] = logo_url
        response = supabase.table('equipes').update(update_data).eq('id', equipe_id).execute()
        if response.data:
            print(f"✅ Equipe atualizada no Supabase!")
            return True
        return False
    except Exception as e:
        print(f"❌ Erro ao editar equipe: {e}")
        return False

def excluir_equipe(equipe_id):
    """Exclui uma equipe e todos seus registros"""
    try:
        # O CASCADE na foreign key já remove os registros automaticamente
        response = supabase.table('equipes').delete().eq('id', equipe_id).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Erro ao excluir equipe: {e}")
        return False

# Rotas Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/placar')
def placar():
    # Verifica se há filtros de período
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    sem_divisoes = request.args.get('sem_divisoes', '0') == '1'
    
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
                         todas_equipes=equipes,
                         sem_divisoes=sem_divisoes,
                         periodo=periodo_info)

@app.route('/cadastrar_equipe', methods=['GET', 'POST'])
def cadastrar_equipe():
    if request.method == 'POST':
        nome = request.form['nome']
        logo_url = request.form.get('logo_url', '').strip()
        
        if criar_equipe(nome, logo_url):
            flash(f'Equipe {nome} cadastrada com sucesso!', 'success')
        else:
            flash('Erro ao cadastrar equipe. Verifique a conexão com Supabase.', 'error')
        
        return redirect(url_for('placar'))
    
    return render_template('cadastrar_equipe.html')

@app.route('/registrar_atividade', methods=['GET', 'POST'])
def registrar_atividade():
    if request.method == 'POST':
        dados = {
            'equipe_id': int(request.form['equipe_id']),
            'data_inicio': request.form['data_inicio'],
            'data_fim': request.form['data_fim'],
            'qtd_pessoas': int(request.form.get('qtd_pessoas', 0)),
            'qtd_pessoas_novas': int(request.form.get('qtd_pessoas_novas', 0)),
            'qtd_celulas': int(request.form.get('qtd_celulas', 0)),
            'qtd_celulas_realizadas': int(request.form.get('qtd_celulas_realizadas', 0)),
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
            flash('Erro ao registrar atividade. Verifique a conexão com Supabase.', 'error')
        
        return redirect(url_for('placar'))
    
    equipes = get_equipes()
    return render_template('registrar_atividade.html', equipes=equipes)

@app.route('/placar_periodo', methods=['POST'])
def placar_periodo():
    """Rota para filtrar placar por período"""
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    
    return redirect(url_for('placar', data_inicio=data_inicio, data_fim=data_fim))

@app.route('/relatorios')
def relatorios():
    equipes = get_equipes()
    return render_template('relatorios.html', equipes=equipes)

@app.route('/relatorio_periodo', methods=['POST'])
def relatorio_periodo():
    data_inicio = request.form['data_inicio']
    data_fim = request.form['data_fim']
    equipe_id = request.form.get('equipe_id')
    
    registros = get_registros_por_periodo(data_inicio, data_fim, equipe_id)
    equipes = get_equipes()
    
    return render_template('relatorio_resultado.html', 
                         registros=registros, 
                         equipes=equipes,
                         data_inicio=datetime.strptime(data_inicio, '%Y-%m-%d').date(),
                         data_fim=datetime.strptime(data_fim, '%Y-%m-%d').date(),
                         equipe_selecionada=equipe_id)

@app.route('/analise_ia')
def analise_ia():
    """Página de análise com IA"""
    equipes = get_equipes()
    return render_template('analise_ia.html', equipes=equipes)

@app.route('/gerar_analise_ia', methods=['POST'])
def gerar_analise_ia():
    """Gera análise com IA usando API gratuita"""
    try:
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        tipo_analise = request.form['tipo_analise']
        equipe_id = request.form.get('equipe_id')
        ocultar_posicoes = request.form.get('ocultar_posicoes') == '1'
        
        # Busca dados
        registros = get_registros_por_periodo(data_inicio, data_fim, equipe_id)
        equipes = get_equipes()
        
        if not registros:
            return jsonify({
                'success': False,
                'error': 'Nenhum registro encontrado para o período selecionado'
            })
        
        # Prepara dados para análise
        analise_html = gerar_analise_com_ia(registros, equipes, tipo_analise, data_inicio, data_fim, ocultar_posicoes)
        
        return jsonify({
            'success': True,
            'html': analise_html
        })
        
    except Exception as e:
        print(f"Erro ao gerar análise: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

def gerar_analise_com_ia(registros, equipes, tipo_analise, data_inicio, data_fim, ocultar_posicoes=False):
    """Gera análise usando IA gratuita (Groq API)"""
    
    # Agrupa dados por equipe
    dados_por_equipe = {}
    for registro in registros:
        equipe_id = registro['equipe_id']
        if equipe_id not in dados_por_equipe:
            equipe_info = next((e for e in equipes if e['id'] == equipe_id), None)
            equipe_nome = equipe_info['nome'] if equipe_info else 'Desconhecida'
            equipe_logo = equipe_info.get('logo_url', '') if equipe_info else ''
            dados_por_equipe[equipe_id] = {
                'nome': equipe_nome,
                'logo_url': equipe_logo,
                'total_pontos': 0,
                'pessoas_novas': 0,
                'pessoas_novas_terca': 0,
                'pessoas_novas_arena': 0,
                'pessoas_novas_domingo': 0,
                'celulas_realizadas': 0,
                'celulas_elite': 0,
                'pessoas_terca': 0,
                'pessoas_arena': 0,
                'pessoas_domingo': 0,
                'arrecadacao': 0,
                'registros_count': 0
            }
        
        dados = dados_por_equipe[equipe_id]
        dados['total_pontos'] += registro.get('pontuacao', 0)
        dados['pessoas_novas'] += registro.get('qtd_pessoas_novas', 0)
        dados['pessoas_novas_terca'] += registro.get('qtd_pessoas_novas_terca', 0)
        dados['pessoas_novas_arena'] += registro.get('qtd_pessoas_novas_arena', 0)
        dados['pessoas_novas_domingo'] += registro.get('qtd_pessoas_novas_domingo', 0)
        dados['celulas_realizadas'] += registro.get('qtd_celulas_realizadas', 0)
        dados['celulas_elite'] += registro.get('qtd_celulas_elite', 0)
        dados['pessoas_terca'] += registro.get('qtd_pessoas_terca', 0)
        dados['pessoas_arena'] += registro.get('qtd_pessoas_arena', 0)
        dados['pessoas_domingo'] += registro.get('qtd_pessoas_domingo', 0)
        dados['arrecadacao'] += registro.get('valor_arrecadacao_parceiro', 0)
        dados['registros_count'] += 1
    
    # Gera análise sem IA externa (local)
    html = gerar_analise_local(dados_por_equipe, tipo_analise, data_inicio, data_fim, ocultar_posicoes)
    
    return html

def gerar_analise_local(dados_por_equipe, tipo_analise, data_inicio, data_fim, ocultar_posicoes=False):
    """Gera análise inteligente local (sem API externa)"""
    
    html = f"""
    <div class="alert alert-info">
        <i class="fas fa-calendar"></i> Período: <strong>{data_inicio}</strong> até <strong>{data_fim}</strong>
        {('<div class="mt-2"><i class="fas fa-eye-slash"></i> <strong>Modo Surpresa Ativado</strong> - Posições ocultas</div>' if ocultar_posicoes else '')}
    </div>
    """
    
    # Análise Individual
    if tipo_analise in ['completa', 'individual']:
        html += '<h4 class="mt-4"><i class="fas fa-user-circle text-primary"></i> Análise Individual Detalhada por Equipe</h4>'
        
        # Calcula ranking
        ranking_list = sorted(dados_por_equipe.items(), key=lambda x: x[1]['total_pontos'], reverse=True)
        total_equipes = len(ranking_list)
        
        # Iniciar carousel APENAS se modo surpresa estiver ativo E houver mais de uma equipe
        usar_carousel = ocultar_posicoes and total_equipes > 1
        
        # Se modo surpresa, embaralhar ordem (aleatória)
        if usar_carousel:
            import random
            ranking_list = list(ranking_list)
            random.shuffle(ranking_list)
        
        if usar_carousel:
            html += '''
            <div class="alert alert-success">
                <i class="fas fa-info-circle"></i> <strong>Modo Apresentação:</strong> Use as <strong>setas abaixo</strong> ou <strong>arraste</strong> para navegar entre as equipes. 
                <span class="badge bg-primary">{} equipes</span>
            </div>
            <div style="position: relative;">
            <div id="carouselAnalise" class="carousel slide" data-bs-ride="false">
                <div class="carousel-indicators">
            '''.format(total_equipes)
            
            # Indicadores
            for idx in range(total_equipes):
                active = 'active' if idx == 0 else ''
                html += f'<button type="button" data-bs-target="#carouselAnalise" data-bs-slide-to="{idx}" class="{active}" aria-current="{"true" if idx == 0 else "false"}"></button>'
            
            html += '</div><div class="carousel-inner">'
        
        for idx, (equipe_id, dados) in enumerate(ranking_list, 1):
            pontos_fortes = []
            areas_atencao = []
            recomendacoes = []
            detalhes_pontuacao = []
            
            # Determinar posição e divisão
            posicao = idx
            divisao = "A" if posicao <= 5 else "B"
            medal = '🥇' if posicao == 1 else ('🥈' if posicao == 2 else ('🥉' if posicao == 3 else ''))
            
            # Calcular diferença para top 5 (sempre, para uso posterior)
            diff_para_top5 = 0
            if posicao > 5 and len(ranking_list) >= 5:
                diff_para_top5 = ranking_list[4][1]['total_pontos'] - dados['total_pontos']
            
            # Análise de posição (oculta se modo surpresa ativado)
            if ocultar_posicoes:
                explicacao_posicao = f"🎯 <strong>Análise de Desempenho:</strong> Veja abaixo os pontos fortes, áreas de atenção e recomendações estratégicas para a equipe {dados['nome']}."
            else:
                if posicao == 1:
                    explicacao_posicao = f"🏆 <strong>Líder Absoluto!</strong> A equipe {dados['nome']} conquistou o 1º lugar com <strong>{dados['total_pontos']} pontos</strong>, demonstrando excelência em todas as áreas."
                elif posicao <= 3:
                    explicacao_posicao = f"{medal} <strong>Pódio Garantido!</strong> A equipe está em <strong>{posicao}º lugar</strong> na Divisão A com <strong>{dados['total_pontos']} pontos</strong>, mostrando desempenho excepcional."
                elif posicao <= 5:
                    explicacao_posicao = f"⭐ <strong>Divisão A!</strong> A equipe está em <strong>{posicao}º lugar</strong> entre as top 5, com <strong>{dados['total_pontos']} pontos</strong>. Continue assim para manter a posição!"
                else:
                    explicacao_posicao = f"🎯 <strong>Divisão B</strong> - Posição <strong>{posicao}º</strong> com <strong>{dados['total_pontos']} pontos</strong>. Faltam apenas <strong>{diff_para_top5} pontos</strong> para alcançar a Divisão A!"
            
            # Detalhamento da pontuação
            if dados['pessoas_novas'] > 0:
                pts = dados['pessoas_novas'] * 10
                detalhes_pontuacao.append(f"👥 <strong>Pessoas Novas:</strong> {dados['pessoas_novas']} pessoas × 10pts = <span class='badge bg-success'>{pts} pontos</span>")
            
            if dados['celulas_realizadas'] > 0:
                pts = dados['celulas_realizadas'] * 10
                detalhes_pontuacao.append(f"⚪ <strong>Células Realizadas:</strong> {dados['celulas_realizadas']} células × 10pts = <span class='badge bg-primary'>{pts} pontos</span>")
            
            if dados['celulas_elite'] > 0:
                pts = dados['celulas_elite'] * 10
                detalhes_pontuacao.append(f"⭐ <strong>Células Elite:</strong> {dados['celulas_elite']} células × 10pts = <span class='badge bg-warning'>{pts} pontos</span>")
            
            if dados['pessoas_terca'] > 0:
                pts = dados['pessoas_terca'] * 10
                detalhes_pontuacao.append(f"🗓️ <strong>Terça-feira:</strong> {dados['pessoas_terca']} pessoas × 10pts = <span class='badge bg-info'>{pts} pontos</span>")
            
            if dados['pessoas_novas_terca'] > 0:
                pts = dados['pessoas_novas_terca'] * 15
                detalhes_pontuacao.append(f"🌟 <strong>Pessoas Novas (Terça):</strong> {dados['pessoas_novas_terca']} pessoas × 15pts = <span class='badge bg-info'>{pts} pontos</span>")
            
            if dados['pessoas_arena'] > 0:
                pts = dados['pessoas_arena'] * 10
                detalhes_pontuacao.append(f"🔥 <strong>Arena:</strong> {dados['pessoas_arena']} pessoas × 10pts = <span class='badge bg-danger'>{pts} pontos</span>")
            
            if dados['pessoas_novas_arena'] > 0:
                pts = dados['pessoas_novas_arena'] * 15
                detalhes_pontuacao.append(f"🌟 <strong>Pessoas Novas (Arena):</strong> {dados['pessoas_novas_arena']} pessoas × 15pts = <span class='badge bg-danger'>{pts} pontos</span>")
            
            if dados['pessoas_domingo'] > 0:
                pts = dados['pessoas_domingo'] * 10
                detalhes_pontuacao.append(f"⛪ <strong>Domingo:</strong> {dados['pessoas_domingo']} pessoas × 10pts = <span class='badge bg-secondary'>{pts} pontos</span>")
            
            if dados['pessoas_novas_domingo'] > 0:
                pts = dados['pessoas_novas_domingo'] * 15
                detalhes_pontuacao.append(f"🌟 <strong>Pessoas Novas (Domingo):</strong> {dados['pessoas_novas_domingo']} pessoas × 15pts = <span class='badge bg-secondary'>{pts} pontos</span>")
            
            if dados['arrecadacao'] > 0:
                pts = dados['arrecadacao'] * 10
                detalhes_pontuacao.append(f"💰 <strong>Parceiro de Deus:</strong> R$ {dados['arrecadacao']:.2f} × 10pts = <span class='badge bg-success'>{int(pts)} pontos</span>")
            
            if not detalhes_pontuacao:
                detalhes_pontuacao.append("📄 Nenhuma pontuação registrada neste período")
            
            # Análise de pontos fortes
            if dados['pessoas_novas'] > 10:
                pontos_fortes.append(f"🌟 <strong>Excelência em Evangelismo:</strong> {dados['pessoas_novas']} pessoas novas conquistadas - um dos melhores resultados!")
            elif dados['pessoas_novas'] >= 5:
                pontos_fortes.append(f"👍 <strong>Bom Evangelismo:</strong> {dados['pessoas_novas']} pessoas novas - resultado sólido")
            
            if dados['celulas_elite'] > 5:
                pontos_fortes.append(f"⭐ <strong>Destaque em Células Elite:</strong> {dados['celulas_elite']} células elite mostram compromisso com excelência")
            elif dados['celulas_elite'] >= 3:
                pontos_fortes.append(f"✨ <strong>Células de Qualidade:</strong> {dados['celulas_elite']} células elite - bom padrão")
            
            if dados['arrecadacao'] > 100:
                pontos_fortes.append(f"💰 <strong>Comprometimento Financeiro Forte:</strong> R$ {dados['arrecadacao']:.2f} em Parceiro de Deus demonstra engajamento")
            
            if dados['pessoas_arena'] > 20:
                pontos_fortes.append(f"🔥 <strong>Participação Massiva na Arena:</strong> {dados['pessoas_arena']} pessoas - excelente mobilização!")
            
            if dados['pessoas_domingo'] > 20:
                pontos_fortes.append(f"⛪ <strong>Presença Forte no Domingo:</strong> {dados['pessoas_domingo']} pessoas - ótima frequência")
            
            # Áreas de atenção
            if dados['pessoas_novas'] < 5:
                areas_atencao.append(f"⚠️ <strong>Evangelismo Precisa Crescer:</strong> Apenas {dados['pessoas_novas']} pessoas novas - invista mais em estratégias de alcance")
                recomendacoes.append("💡 Implementar campanha de convites pessoais e eventos evangelisticos")
            
            if dados['celulas_realizadas'] < dados['registros_count'] * 3:
                areas_atencao.append(f"⚠️ <strong>Células Abaixo do Esperado:</strong> {dados['celulas_realizadas']} células realizadas - potencial para mais")
                recomendacoes.append("💡 Fortalecer comprometimento dos líderes e criar suporte contínuo")
            
            if dados['pessoas_domingo'] < 15:
                areas_atencao.append(f"⚠️ <strong>Presença no Domingo Baixa:</strong> {dados['pessoas_domingo']} pessoas - criar cultura de frequência")
                recomendacoes.append("💡 Campanha de valorização dos cultos dominicais e followup de ausentes")
            
            if dados['arrecadacao'] < 50:
                areas_atencao.append(f"⚠️ <strong>Parceiro de Deus Precisa Atenção:</strong> R$ {dados['arrecadacao']:.2f} - ensinar sobre contribuição")
                recomendacoes.append("💡 Workshop sobre benefícios de ser Parceiro de Deus e impacto do dízimo")
            
            # Recomendações específicas por posição (só se não for modo surpresa)
            if not ocultar_posicoes:
                if posicao == 1:
                    recomendacoes.append("🏆 Manter o ritmo e servir de exemplo para outras equipes")
                elif posicao > 5 and diff_para_top5 > 0:
                    recomendacoes.append(f"🎯 Foco total nos próximos {diff_para_top5} pontos para alcançar Divisão A")
            
            if not pontos_fortes:
                pontos_fortes.append("🎯 Equipe em fase de desenvolvimento - todo esforço é valioso!")
            if not areas_atencao:
                areas_atencao.append("✅ Nenhuma área crítica - parabéns pelo equilíbrio!")
            if not recomendacoes:
                recomendacoes.append("🎉 Continue investindo no que já funciona bem!")
            
            # Preparar logo
            logo_html = ''
            if dados.get('logo_url'):
                logo_html = f'<img src="{dados["logo_url"]}" alt="{dados["nome"]}" style="width: 40px; height: 40px; object-fit: contain; margin-right: 10px; border-radius: 8px; background: white; padding: 2px;">'
            
            # Definir cor do card (neutra se modo surpresa)
            if ocultar_posicoes:
                card_bg = 'bg-primary'
                card_text = 'text-white'
            else:
                card_bg = 'bg-warning' if posicao <= 3 else ('bg-success' if posicao <= 5 else 'bg-light')
                card_text = 'text-white' if posicao <= 5 else 'text-dark'
            
            # Wrapper do carousel APENAS se modo surpresa ativo
            carousel_item_start = f'<div class="carousel-item {"active" if idx == 1 else ""}">' if usar_carousel else ''
            carousel_item_end = '</div>' if usar_carousel else ''
            
            html += f"""
            {carousel_item_start}
            <div class="card mb-4 border-{'' if posicao <= 5 and not ocultar_posicoes else 'secondary'}">
                <div class="card-header {card_bg} {card_text}">
                    <h5 class="mb-0 d-flex align-items-center {'justify-content-center' if ocultar_posicoes else 'justify-content-between'}">
                        <span class="d-flex align-items-center">
                            {logo_html}
                            {'' if ocultar_posicoes else medal} {dados['nome']}
                        </span>
                        {'' if ocultar_posicoes else f'<span class="badge {"bg-light text-dark" if posicao <= 5 else "bg-success"}">Divisão {divisao} - {dados["total_pontos"]} pts</span>'}
                    </h5>
                </div>
                <div class="card-body">
                    <!-- Explicação da Posição -->
                    <div class="alert alert-{'success' if posicao <= 5 else 'info'} mb-3">
                        <h6 class="alert-heading"><i class="fas fa-map-marked-alt"></i> Por que esta posição?</h6>
                        <p class="mb-0">{explicacao_posicao}</p>
                    </div>
                    
                    <!-- Detalhamento da Pontuação -->
                    <h6 class="text-primary mb-3"><i class="fas fa-calculator"></i> Como a Equipe Pontuou:</h6>
                    <div class="row mb-3">
                        <div class="col-12">
                            <ul class="list-unstyled">
                                {''.join([f'<li class="mb-2">{d}</li>' for d in detalhes_pontuacao])}
                            </ul>
                            {'' if ocultar_posicoes else f'''
                            <div class="alert alert-secondary mt-2">
                                <strong><i class="fas fa-equals"></i> Total:</strong> {dados['total_pontos']} pontos acumulados
                            </div>
                            '''}
                        </div>
                    </div>
                    
                    <hr>
                    
                    <!-- Pontos Fortes e Áreas -->
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <h6 class="text-success"><i class="fas fa-check-circle"></i> Pontos Fortes</h6>
                            <ul class="list-unstyled">
                                {''.join([f'<li class="mb-2">{p}</li>' for p in pontos_fortes])}
                            </ul>
                        </div>
                        <div class="col-md-6 mb-3">
                            <h6 class="text-warning"><i class="fas fa-exclamation-triangle"></i> Áreas de Atenção</h6>
                            <ul class="list-unstyled">
                                {''.join([f'<li class="mb-2">{a}</li>' for a in areas_atencao])}
                            </ul>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <!-- Recomendações -->
                    <h6 class="text-info"><i class="fas fa-lightbulb"></i> Recomendações Estratégicas</h6>
                    <ul class="list-unstyled">
                        {''.join([f'<li class="mb-2">{r}</li>' for r in recomendacoes])}
                    </ul>
                </div>
            </div>
            {carousel_item_end}
            """
        
        # Fechar carousel APENAS se modo surpresa estava ativo
        if usar_carousel:
            import json
            from html import escape as html_escape
            # Pegar as 3 primeiras equipes do ranking original (antes de embaralhar)
            ranking_original = sorted(dados_por_equipe.items(), key=lambda x: x[1]['total_pontos'], reverse=True)
            
            primeiro = ranking_original[0][1] if len(ranking_original) > 0 else None
            segundo = ranking_original[1][1] if len(ranking_original) > 1 else None
            terceiro = ranking_original[2][1] if len(ranking_original) > 2 else None
            
            # Preparar dados JSON seguros com escape HTML
            primeiro_json = html_escape(json.dumps({"nome": primeiro["nome"], "logo": primeiro.get("logo_url", ""), "pontos": primeiro["total_pontos"]})) if primeiro else html_escape('{}')
            segundo_json = html_escape(json.dumps({"nome": segundo["nome"], "logo": segundo.get("logo_url", ""), "pontos": segundo["total_pontos"]})) if segundo else html_escape('{}')
            terceiro_json = html_escape(json.dumps({"nome": terceiro["nome"], "logo": terceiro.get("logo_url", ""), "pontos": terceiro["total_pontos"]})) if terceiro else html_escape('{}')
            
            html += '''
            </div>
            </div>
            <!-- Controles fora do carousel -->
            <div class="d-flex justify-content-center gap-3 mt-4 mb-4">
                <button class="btn btn-primary btn-lg" type="button" data-bs-target="#carouselAnalise" data-bs-slide="prev">
                    <i class="fas fa-chevron-left"></i> Anterior
                </button>
                <button class="btn btn-primary btn-lg" type="button" data-bs-target="#carouselAnalise" data-bs-slide="next">
                    Próximo <i class="fas fa-chevron-right"></i>
                </button>
            </div>
            
            <!-- Botões de Revelação do Pódio -->
            <div class="mt-5 mb-5">
                <h4 class="text-center mb-4">
                    <i class="fas fa-trophy text-warning"></i> Revelação do Pódio
                </h4>
                <div class="row g-3">
                    <div class="col-md-4">
                        <button class="btn btn-warning btn-lg w-100 py-4 btn-revelar" data-posicao="3" data-equipe="''' + terceiro_json + '''" style="font-size: 1.2rem;">
                            <i class="fas fa-medal" style="font-size: 2rem;"></i><br>
                            <strong>Revelar 3º Lugar</strong>
                            <br><small>🥉 Bronze</small>
                        </button>
                    </div>
                    <div class="col-md-4">
                        <button class="btn btn-secondary btn-lg w-100 py-4 btn-revelar" data-posicao="2" data-equipe="''' + segundo_json + '''" style="font-size: 1.2rem;">
                            <i class="fas fa-medal" style="font-size: 2rem;"></i><br>
                            <strong>Revelar 2º Lugar</strong>
                            <br><small>🥈 Prata</small>
                        </button>
                    </div>
                    <div class="col-md-4">
                        <button class="btn btn-success btn-lg w-100 py-4 btn-revelar" data-posicao="1" data-equipe="''' + primeiro_json + '''" style="font-size: 1.2rem;">
                            <i class="fas fa-crown" style="font-size: 2rem;"></i><br>
                            <strong>Revelar 1º Lugar</strong>
                            <br><small>🥇 Ouro - CAMPEÃO</small>
                        </button>
                    </div>
                </div>
            </div>
            
            </div>
            '''
    
    # Análise Comparativa (oculta se modo surpresa ativado)
    if tipo_analise in ['completa', 'comparativa'] and not ocultar_posicoes:
        html += '<h4 class="mt-4"><i class="fas fa-balance-scale text-info"></i> Análise Comparativa</h4>'
        
        # Ranking
        ranking = sorted(dados_por_equipe.items(), key=lambda x: x[1]['total_pontos'], reverse=True)
        
        html += '<div class="card mb-3"><div class="card-body">'
        html += '<h6><i class="fas fa-medal text-warning"></i> Ranking Geral</h6>'
        html += '<table class="table table-sm">'
        html += '<thead><tr><th>Posição</th><th>Equipe</th><th>Pontos</th><th>Destaque</th></tr></thead><tbody>'
        
        for idx, (equipe_id, dados) in enumerate(ranking, 1):
            medal = '🥇' if idx == 1 else ('🥈' if idx == 2 else ('🥉' if idx == 3 else ''))
            destaque = ''
            if dados['pessoas_novas'] == max(d['pessoas_novas'] for d in dados_por_equipe.values()):
                destaque += '🌟 Evangelismo '
            if dados['celulas_elite'] == max(d['celulas_elite'] for d in dados_por_equipe.values()):
                destaque += '⭐ Células Elite '
            
            # Logo da equipe
            logo_td = ''
            if dados.get('logo_url'):
                logo_td = f'<img src="{dados["logo_url"]}" alt="{dados["nome"]}" style="width: 30px; height: 30px; object-fit: contain; margin-right: 8px; border-radius: 6px; background: white; padding: 2px;">'
            
            html += f"<tr><td>{medal} {idx}º</td><td>{logo_td}<strong>{dados['nome']}</strong></td><td>{dados['total_pontos']}</td><td><small>{destaque}</small></td></tr>"
        
        html += '</tbody></table></div></div>'
        
        # Comparação por categoria
        html += '<div class="row">'
        categorias = [
            ('pessoas_novas', 'Pessoas Novas', 'success', 'user-plus'),
            ('celulas_elite', 'Células Elite', 'warning', 'star'),
            ('pessoas_arena', 'Arena', 'danger', 'fire'),
            ('arrecadacao', 'Arrecação', 'info', 'dollar-sign')
        ]
        
        for campo, nome, cor, icone in categorias:
            melhor = max(dados_por_equipe.items(), key=lambda x: x[1][campo])
            valor = melhor[1][campo]
            if campo == 'arrecadacao':
                valor_fmt = f"R$ {valor:.2f}"
            else:
                valor_fmt = str(int(valor))
            
            html += f"""
            <div class="col-md-3 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-{icone} fa-2x text-{cor} mb-2"></i>
                        <h6>{nome}</h6>
                        <p class="mb-0"><strong>{melhor[1]['nome']}</strong></p>
                        <p class="text-{cor} mb-0">{valor_fmt}</p>
                    </div>
                </div>
            </div>
            """
        
        html += '</div>'
    
    # Recomendações Gerais
    if tipo_analise in ['completa', 'recomendacoes']:
        html += '<h4 class="mt-4"><i class="fas fa-rocket text-success"></i> Recomendações Estratégicas Gerais</h4>'
        html += '<div class="card"><div class="card-body">'
        
        total_pessoas_novas = sum(d['pessoas_novas'] for d in dados_por_equipe.values())
        media_pessoas_novas = total_pessoas_novas / len(dados_por_equipe) if dados_por_equipe else 0
        
        recomendacoes_gerais = []
        
        if media_pessoas_novas > 8:
            recomendacoes_gerais.append({
                'titulo': '🎉 Crescimento Evangélistico Forte',
                'desc': 'O número de pessoas novas está excelente! Continue investindo em eventos de convite e treinamento de evangelismo.',
                'tipo': 'success'
            })
        else:
            recomendacoes_gerais.append({
                'titulo': '🎯 Foco em Evangelismo',
                'desc': 'Implementar campanha intensiva de evangelismo. Sugestões: eventos sociais, visitas, treinamento de líderes.',
                'tipo': 'warning'
            })
        
        recomendacoes_gerais.append({
            'titulo': '📈 Planejamento Estratégico',
            'desc': 'Definir metas claras para o próximo período baseadas nesta análise. Estabelecer KPIs e acompanhamento semanal.',
            'tipo': 'info'
        })
        
        recomendacoes_gerais.append({
            'titulo': '🎖️ Reconhecimento e Motivação',
            'desc': 'Celebrar vitórias publicamente. Criar sistema de reconhecimento para equipes e líderes que se destacam.',
            'tipo': 'primary'
        })
        
        for rec in recomendacoes_gerais:
            html += f"""
            <div class="alert alert-{rec['tipo']} mb-3">
                <h6 class="alert-heading">{rec['titulo']}</h6>
                <p class="mb-0">{rec['desc']}</p>
            </div>
            """
        
        html += '</div></div>'
    
    html += '<div class="alert alert-light mt-4"><i class="fas fa-info-circle"></i> <small>Análise gerada em ' + datetime.now().strftime('%d/%m/%Y às %H:%M') + '</small></div>'
    
    return html

@app.route('/editar_equipe/<int:equipe_id>', methods=['GET', 'POST'])
def editar_equipe_route(equipe_id):
    equipe = get_equipe_by_id(equipe_id)
    if not equipe:
        flash('Equipe não encontrada!', 'error')
        return redirect(url_for('placar'))
    
    if request.method == 'POST':
        nome_antigo = equipe['nome']
        novo_nome = request.form['nome']
        logo_url = request.form.get('logo_url', '').strip()
        
        if editar_equipe(equipe_id, novo_nome, logo_url):
            flash(f'Equipe "{nome_antigo}" atualizada com sucesso!', 'success')
        else:
            flash('Erro ao atualizar equipe.', 'error')
        
        return redirect(url_for('placar'))
    
    return render_template('editar_equipe.html', equipe=equipe)

@app.route('/excluir_equipe/<int:equipe_id>', methods=['POST'])
def excluir_equipe_route(equipe_id):
    equipe = get_equipe_by_id(equipe_id)
    if not equipe:
        flash('Equipe não encontrada!', 'error')
        return redirect(url_for('placar'))
    
    nome_equipe = equipe['nome']
    
    if excluir_equipe(equipe_id):
        flash(f'Equipe "{nome_equipe}" excluída com sucesso!', 'success')
    else:
        flash('Erro ao excluir equipe.', 'error')
    
    return redirect(url_for('placar'))

@app.route('/historico/<int:equipe_id>')
def historico_equipe(equipe_id):
    equipe = get_equipe_by_id(equipe_id)
    if not equipe:
        flash('Equipe não encontrada!', 'error')
        return redirect(url_for('placar'))
    
    registros = get_registros_equipe(equipe_id)
    return render_template('historico.html', equipe=equipe, registros=registros)

@app.route('/editar_registro/<int:registro_id>', methods=['GET', 'POST'])
def editar_registro_route(registro_id):
    """Rota para editar um registro"""
    try:
        # Busca o registro
        response = supabase.table('registros').select('*').eq('id', registro_id).execute()
        if not response.data:
            flash('Registro não encontrado!', 'error')
            return redirect(url_for('placar'))
        
        registro = response.data[0]
        equipe = get_equipe_by_id(registro['equipe_id'])
        
        if request.method == 'POST':
            # Atualiza os dados
            dados_atualizados = {
                'data_inicio': request.form['data_inicio'],
                'data_fim': request.form['data_fim'],
                'qtd_pessoas': int(request.form.get('qtd_pessoas', 0)),
                'qtd_pessoas_novas': int(request.form.get('qtd_pessoas_novas', 0)),
                'qtd_celulas': int(request.form.get('qtd_celulas', 0)),
                'qtd_celulas_realizadas': int(request.form.get('qtd_celulas_realizadas', 0)),
                'qtd_celulas_elite': int(request.form.get('qtd_celulas_elite', 0)),
                'qtd_pessoas_terca': int(request.form.get('qtd_pessoas_terca', 0)),
                'qtd_pessoas_novas_terca': int(request.form.get('qtd_pessoas_novas_terca', 0)),
                'qtd_pessoas_arena': int(request.form.get('qtd_pessoas_arena', 0)),
                'qtd_pessoas_novas_arena': int(request.form.get('qtd_pessoas_novas_arena', 0)),
                'qtd_pessoas_domingo': int(request.form.get('qtd_pessoas_domingo', 0)),
                'qtd_pessoas_novas_domingo': int(request.form.get('qtd_pessoas_novas_domingo', 0)),
                'valor_arrecadacao_parceiro': float(request.form.get('valor_arrecadacao_parceiro', 0))
            }
            
            # Recalcula pontuação
            nova_pontuacao = calcular_pontuacao(dados_atualizados)
            dados_atualizados['pontuacao'] = nova_pontuacao
            
            # Pontuação antiga
            pontuacao_antiga = registro['pontuacao']
            diferenca = nova_pontuacao - pontuacao_antiga
            
            # Atualiza registro
            supabase.table('registros').update(dados_atualizados).eq('id', registro_id).execute()
            
            # Atualiza pontuação total da equipe
            equipe_response = supabase.table('equipes').select('pontuacao_total').eq('id', registro['equipe_id']).execute()
            if equipe_response.data:
                nova_pontuacao_total = equipe_response.data[0]['pontuacao_total'] + diferenca
                supabase.table('equipes').update({'pontuacao_total': nova_pontuacao_total}).eq('id', registro['equipe_id']).execute()
            
            flash(f'Registro atualizado! Nova pontuação: {nova_pontuacao}', 'success')
            return redirect(url_for('historico_equipe', equipe_id=registro['equipe_id']))
        
        return render_template('editar_registro.html', registro=registro, equipe=equipe)
    
    except Exception as e:
        print(f"Erro ao editar registro: {e}")
        flash('Erro ao editar registro.', 'error')
        return redirect(url_for('placar'))

@app.route('/excluir_registro/<int:registro_id>', methods=['POST'])
def excluir_registro_route(registro_id):
    """Rota para excluir um registro"""
    try:
        # Busca o registro
        response = supabase.table('registros').select('*').eq('id', registro_id).execute()
        if not response.data:
            flash('Registro não encontrado!', 'error')
            return redirect(url_for('placar'))
        
        registro = response.data[0]
        equipe_id = registro['equipe_id']
        pontuacao = registro['pontuacao']
        
        # Exclui o registro
        supabase.table('registros').delete().eq('id', registro_id).execute()
        
        # Atualiza pontuação da equipe (subtrai)
        equipe_response = supabase.table('equipes').select('pontuacao_total').eq('id', equipe_id).execute()
        if equipe_response.data:
            nova_pontuacao_total = max(0, equipe_response.data[0]['pontuacao_total'] - pontuacao)
            supabase.table('equipes').update({'pontuacao_total': nova_pontuacao_total}).eq('id', equipe_id).execute()
        
        flash('Registro excluído com sucesso!', 'success')
        return redirect(url_for('historico_equipe', equipe_id=equipe_id))
    
    except Exception as e:
        print(f"Erro ao excluir registro: {e}")
        flash('Erro ao excluir registro.', 'error')
        return redirect(url_for('placar'))

@app.route('/status')
def status():
    """Rota para verificar status da conexão"""
    try:
        # Testa conexão
        response = supabase.table('equipes').select('count').execute()
        equipes_count = len(get_equipes())
        
        status_info = {
            'supabase_connected': True,
            'supabase_url': SUPABASE_URL,
            'equipes_cadastradas': equipes_count,
            'modo': 'producao'
        }
    except Exception as e:
        status_info = {
            'supabase_connected': False,
            'error': str(e),
            'modo': 'erro'
        }
    
    return jsonify(status_info)

@app.route('/api/pontuacao_config')
def api_pontuacao_config():
    return jsonify(PONTUACAO_CONFIG)

if __name__ == '__main__':
    print("🚀 ZERO 1 iniciado com Supabase!")
    print(f"🔗 Conectando em: {SUPABASE_URL}")
    
    # Inicializa banco
    if init_database():
        print("✅ Banco de dados pronto!")
    else:
        print("⚠️  Configure as tabelas no Supabase primeiro!")
    
    print("🌐 Acesse: http://localhost:5004")
    app.run(debug=False, host='0.0.0.0', port=5004)

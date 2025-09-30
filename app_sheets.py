from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime, date
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

# Configuração do Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# ID da planilha do Google Sheets (você precisará criar uma planilha e colocar o ID aqui)
SPREADSHEET_ID = "1BcD3FgH4JkL5MnO6PqR7StU8VwX9YzA0"  # Substitua pelo ID real da sua planilha

class SheetsDB:
    def __init__(self):
        self.gc = None
        self.sheet = None
        self.init_connection()
    
    def init_connection(self):
        """Inicializa conexão com Google Sheets usando credenciais"""
        try:
            # Tenta usar credenciais de arquivo JSON (para produção)
            if os.path.exists('credentials.json'):
                creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
                self.gc = gspread.authorize(creds)
            else:
                # Para desenvolvimento, usa credenciais padrão
                print("⚠️  Arquivo credentials.json não encontrado!")
                print("📋 Para usar Google Sheets, você precisa:")
                print("1. Criar um projeto no Google Cloud Console")
                print("2. Ativar a API do Google Sheets")
                print("3. Criar credenciais de conta de serviço")
                print("4. Baixar o arquivo JSON e renomear para 'credentials.json'")
                print("5. Compartilhar a planilha com o email da conta de serviço")
                return False
                
            # Abre a planilha
            self.sheet = self.gc.open_by_key(SPREADSHEET_ID)
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar com Google Sheets: {e}")
            return False
    
    def get_worksheet(self, name):
        """Obtém ou cria uma aba da planilha"""
        try:
            return self.sheet.worksheet(name)
        except gspread.WorksheetNotFound:
            # Cria a aba se não existir
            return self.sheet.add_worksheet(title=name, rows=1000, cols=20)
    
    def init_sheets(self):
        """Inicializa as abas da planilha com cabeçalhos"""
        if not self.gc:
            return False
            
        try:
            # Aba de Equipes
            equipes_ws = self.get_worksheet('Equipes')
            if not equipes_ws.get('A1'):
                equipes_ws.append_row(['ID', 'Nome', 'Pontuacao_Total', 'Data_Criacao'])
            
            # Aba de Registros
            registros_ws = self.get_worksheet('Registros')
            if not registros_ws.get('A1'):
                registros_ws.append_row([
                    'ID', 'Equipe_ID', 'Equipe_Nome', 'Data_Inicio', 'Data_Fim', 'Data_Registro',
                    'Qtd_Pessoas', 'Qtd_Pessoas_Novas', 'Qtd_Celulas_Elite',
                    'Qtd_Pessoas_Terca', 'Qtd_Pessoas_Novas_Terca',
                    'Qtd_Pessoas_Arena', 'Qtd_Pessoas_Novas_Arena',
                    'Qtd_Pessoas_Domingo', 'Qtd_Pessoas_Novas_Domingo',
                    'Valor_Arrecadacao_Parceiro', 'Pontuacao'
                ])
            
            print("✅ Planilhas inicializadas com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao inicializar planilhas: {e}")
            return False

# Instância global do banco de dados
db = SheetsDB()

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

def get_equipes():
    """Obtém todas as equipes da planilha"""
    if not db.gc:
        return []
    
    try:
        ws = db.get_worksheet('Equipes')
        records = ws.get_all_records()
        
        # Ordena por pontuação (maior para menor)
        equipes = sorted(records, key=lambda x: x.get('Pontuacao_Total', 0), reverse=True)
        
        # Adiciona divisão baseada na posição
        for i, equipe in enumerate(equipes):
            equipe['divisao'] = 'A' if i < 5 else 'B'
            equipe['posicao'] = i + 1
        
        return equipes
    except Exception as e:
        print(f"Erro ao obter equipes: {e}")
        return []

def get_equipe_by_id(equipe_id):
    """Obtém uma equipe específica pelo ID"""
    equipes = get_equipes()
    for equipe in equipes:
        if str(equipe.get('ID')) == str(equipe_id):
            return equipe
    return None

def criar_equipe(nome):
    """Cria uma nova equipe"""
    if not db.gc:
        return False
    
    try:
        ws = db.get_worksheet('Equipes')
        records = ws.get_all_records()
        
        # Gera novo ID
        novo_id = max([r.get('ID', 0) for r in records], default=0) + 1
        
        # Adiciona nova equipe
        ws.append_row([novo_id, nome, 0, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        return True
    except Exception as e:
        print(f"Erro ao criar equipe: {e}")
        return False

def atualizar_pontuacao_equipe(equipe_id, pontos_adicionais):
    """Atualiza a pontuação de uma equipe"""
    if not db.gc:
        return False
    
    try:
        ws = db.get_worksheet('Equipes')
        records = ws.get_all_records()
        
        for i, record in enumerate(records):
            if str(record.get('ID')) == str(equipe_id):
                nova_pontuacao = record.get('Pontuacao_Total', 0) + pontos_adicionais
                ws.update_cell(i + 2, 3, nova_pontuacao)  # Coluna C (Pontuacao_Total)
                return True
        return False
    except Exception as e:
        print(f"Erro ao atualizar pontuação: {e}")
        return False

def criar_registro(dados):
    """Cria um novo registro de atividade"""
    if not db.gc:
        return False
    
    try:
        ws = db.get_worksheet('Registros')
        records = ws.get_all_records()
        
        # Gera novo ID
        novo_id = max([r.get('ID', 0) for r in records], default=0) + 1
        
        # Calcula pontuação
        pontuacao = calcular_pontuacao(dados)
        
        # Obtém nome da equipe
        equipe = get_equipe_by_id(dados['equipe_id'])
        equipe_nome = equipe['Nome'] if equipe else 'Desconhecida'
        
        # Prepara dados para inserção
        row_data = [
            novo_id,
            dados['equipe_id'],
            equipe_nome,
            dados['data_inicio'],
            dados['data_fim'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            dados.get('qtd_pessoas', 0),
            dados.get('qtd_pessoas_novas', 0),
            dados.get('qtd_celulas_elite', 0),
            dados.get('qtd_pessoas_terca', 0),
            dados.get('qtd_pessoas_novas_terca', 0),
            dados.get('qtd_pessoas_arena', 0),
            dados.get('qtd_pessoas_novas_arena', 0),
            dados.get('qtd_pessoas_domingo', 0),
            dados.get('qtd_pessoas_novas_domingo', 0),
            dados.get('valor_arrecadacao_parceiro', 0),
            pontuacao
        ]
        
        # Adiciona registro
        ws.append_row(row_data)
        
        # Atualiza pontuação da equipe
        atualizar_pontuacao_equipe(dados['equipe_id'], pontuacao)
        
        return pontuacao
    except Exception as e:
        print(f"Erro ao criar registro: {e}")
        return False

# Rotas Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/placar')
def placar():
    equipes = get_equipes()
    equipes_a = [e for e in equipes if e.get('divisao') == 'A']
    equipes_b = [e for e in equipes if e.get('divisao') == 'B']
    return render_template('placar.html', equipes_a=equipes_a, equipes_b=equipes_b)

@app.route('/cadastrar_equipe', methods=['GET', 'POST'])
def cadastrar_equipe():
    if request.method == 'POST':
        nome = request.form['nome']
        
        if criar_equipe(nome):
            flash(f'Equipe {nome} cadastrada com sucesso!', 'success')
        else:
            flash('Erro ao cadastrar equipe. Verifique a conexão com Google Sheets.', 'error')
        
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
            flash('Erro ao registrar atividade. Verifique a conexão com Google Sheets.', 'error')
        
        return redirect(url_for('placar'))
    
    equipes = get_equipes()
    return render_template('registrar_atividade.html', equipes=equipes)

@app.route('/relatorios')
def relatorios():
    equipes = get_equipes()
    return render_template('relatorios.html', equipes=equipes)

@app.route('/status')
def status():
    """Rota para verificar status da conexão"""
    status_info = {
        'google_sheets_connected': db.gc is not None,
        'spreadsheet_id': SPREADSHEET_ID,
        'credentials_file': os.path.exists('credentials.json')
    }
    return jsonify(status_info)

if __name__ == '__main__':
    # Inicializa as planilhas
    if db.gc:
        db.init_sheets()
        print("🚀 ZERO 1 iniciado com Google Sheets!")
    else:
        print("⚠️  ZERO 1 iniciado SEM Google Sheets - modo demonstração")
    
    app.run(debug=False, host='0.0.0.0', port=5002)

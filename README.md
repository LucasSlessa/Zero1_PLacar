# ZERO 1 - Sistema de Placar

Um sistema inteligente para gerenciar a competição entre equipes, com divisões automáticas baseadas na pontuação e registro de atividades por período.

## 🎯 Funcionalidades

### ✅ Gerenciamento de Equipes
- Cadastro de equipes com divisão automática por pontuação
- Top 5 equipes = Divisão A, demais = Divisão B
- Visualização do placar em tempo real
- Histórico detalhado de cada equipe
- Edição e exclusão de equipes

### 📊 Sistema de Pontuação Avançado
- **Pessoas Novas (Geral)**: 10 pontos cada
- **Células Elite**: 15 pontos cada  
- **Pessoas Terça**: 5 pontos cada
- **Pessoas Novas Terça**: 10 pontos cada
- **Pessoas Arena**: 8 pontos cada
- **Pessoas Novas Arena**: 15 pontos cada
- **Pessoas Domingo**: 3 pontos cada
- **Pessoas Novas Domingo**: 8 pontos cada
- **Arrecadação Parceiro de Deus**: 0.1 ponto por real

### 📅 Registro por Período
- Registro de atividades com data inicial e final
- Substituição do sistema de semanas por períodos flexíveis
- Melhor controle temporal das atividades

### 📊 Sistema de Relatórios
- Relatórios detalhados por período
- Filtros por equipe específica ou todas
- Visualização de estatísticas consolidadas
- Dados de participação e arrecadação

### 🎮 Interface Moderna
- Design verde luxuoso e elegante
- Formulários intuitivos com validação
- Cálculo automático de pontuação em tempo real
- Navegação simples e responsiva

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou baixe o projeto**
```bash
cd /home/agrovisia/Desenvolvimento/placar
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute o sistema**
```bash
python app.py
```

4. **Acesse no navegador**
```
http://localhost:5000
```

## 📱 Como Usar

### 1. Primeira Execução
- O sistema iniciará com banco de dados limpo, pronto para produção
- Comece cadastrando suas equipes

### 2. Cadastrar Nova Equipe
- Acesse "Nova Equipe" no menu
- Informe o nome da equipe
- A divisão será determinada automaticamente pela pontuação
- Clique em "Cadastrar Equipe"

### 3. Registrar Atividades
- Acesse "Registrar Atividade" no menu
- Selecione a equipe
- Defina o período (data inicial e final)
- Preencha os dados de cada atividade:
  - Quantidade de pessoas e pessoas novas
  - Células Elite
  - Participação em Terça, Arena e Domingo
  - Valor de arrecadação do Parceiro de Deus
- O sistema calculará automaticamente a pontuação
- Clique em "Registrar Atividade"

### 4. Visualizar Placar
- Acesse "Placar" no menu
- Veja a classificação automática das Divisões A e B
- Top 5 equipes ficam na Divisão A
- Clique nos botões para ver histórico ou editar equipes

### 5. Gerar Relatórios
- Acesse "Relatórios" no menu
- Selecione o período desejado
- Opcionalmente filtre por equipe específica
- Visualize dados consolidados e detalhados

## 🗂️ Estrutura do Projeto

```
placar/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
├── placar_igreja.db      # Banco de dados SQLite (criado automaticamente)
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── placar.html
│   ├── registrar_atividade.html
│   ├── cadastrar_equipe.html
│   └── historico.html
└── static/              # Arquivos estáticos
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 🎨 Tecnologias Utilizadas

- **Backend**: Python Flask
- **Banco de Dados**: SQLite com SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework CSS**: Bootstrap 5
- **Ícones**: Font Awesome

## 📋 Critérios de Pontuação Detalhados

### Atividades com Quantidade
- **Pessoas**: Novos membros que se juntaram à equipe
- **Elite**: Membros que alcançaram status especial
- **Células**: Novas células/grupos formados
- **Parceiro de Deus**: Novos parceiros/apoiadores

### Atividades de Participação
- **Arena**: Participação em eventos especiais da igreja
- **Domingo**: Participação no culto dominical

## 🔧 Personalização

### Alterar Pontuação
Edite o dicionário `PONTUACAO_CONFIG` no arquivo `app.py`:

```python
PONTUACAO_CONFIG = {
    'pessoas_novas': 10,      # Altere aqui
    'elite_novos': 15,        # Altere aqui
    'celulas_novas': 5,       # Altere aqui
    'arena_participacao': 20, # Altere aqui
    'domingo_participacao': 10, # Altere aqui
    'parceiro_deus_novos': 25   # Altere aqui
}
```

### Adicionar Novas Atividades
1. Adicione campos na classe `Registro` no `app.py`
2. Atualize o formulário em `registrar_atividade.html`
3. Modifique a função `calcular_pontuacao()`

## 🐛 Solução de Problemas

### Erro ao executar
- Verifique se o Python 3.7+ está instalado
- Instale as dependências: `pip install -r requirements.txt`

### Banco de dados corrompido
- Delete o arquivo `placar_igreja.db`
- Execute novamente `python app.py`

### Porta já em uso
- Altere a porta no final do `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mude para 5001
```

## 📞 Suporte

Para dúvidas ou sugestões sobre o sistema, entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido com ❤️ para a comunidade da igreja**
# 🏆 ZERO 1 - Sistema de Placar Igreja

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-success.svg)](https://supabase.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema completo de gamificação para acompanhamento de atividades de equipes de igreja com divisões automáticas, relatórios e gestão de registros.

## ✨ Funcionalidades

- 🎯 **Divisões Automáticas** - Top 5 equipes na Divisão A
- 📈 **Sistema de Pontuação Unificado** - Todos os itens valem 10 pontos
- 📋 **Registro por Período** - Data inicial/final ao invés de semanas
- 📊 **Relatórios Detalhados** - Análise completa de desempenho
- ✏️ **Edição de Registros** - Edite e exclua registros facilmente
- 👀 **Visualização Flexível** - Com ou sem divisões
- 📱 **Design Responsivo** - Interface verde luxuosa

## 🎯 Sistema de Pontuação

Todos os itens pontuam **10 pontos cada**:

- 👥 **Pessoas Novas** (Geral)
- ⚪ **Células Realizadas**
- ⭐ **Células Elite**
- 🗓️ **Pessoas Terça** + Novas
- 🎯 **Pessoas Arena** + Novas
- ⛪ **Pessoas Domingo** + Novas
- 💰 **Arrecação Parceiro de Deus** (10 pts/real)

## 🚀 Como Usar

### **Opção 1: Hospedagem Gratuita (Recomendado)**

Veja o guia completo em [HOSPEDAGEM_GRATUITA.md](HOSPEDAGEM_GRATUITA.md)

**Deploy rápido no Render.com:**
1. Acesse [render.com](https://render.com)
2. Crie conta gratuita
3. "New +" → "Web Service"
4. Conecte este repositório
5. Configure variáveis de ambiente
6. Deploy! 🎉

### **Opção 2: Execução Local**

```bash
# Clone o repositório
git clone https://github.com/LucasSlessa/Zero1_PLacar.git
cd Zero1_PLacar

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais Supabase

# Execute
python app_supabase.py

# Acesse
http://localhost:5004
```

## 🛠️ Configuração

### **1. Supabase**

Crie um projeto gratuito em [supabase.com](https://supabase.com)

Execute os SQLs em [SUPABASE_SETUP.md](SUPABASE_SETUP.md)

### **2. Variáveis de Ambiente**

Crie arquivo `.env`:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_anon
```

## 📚 Documentação

- 📖 [Setup Supabase](SUPABASE_SETUP.md)
- 🔄 [Atualizações](SUPABASE_UPDATE.md)
- 🔄 [Novas Células](ATUALIZACAO_CELULAS.md)
- ☁️ [Hospedagem Gratuita](HOSPEDAGEM_GRATUITA.md)

## 📦 Estrutura do Projeto

```
Zero1_PLacar/
├── app_supabase.py          # Aplicação Flask principal
├── templates/               # Templates HTML
│   ├── base.html
│   ├── placar.html
│   ├── registrar_atividade.html
│   ├── historico.html
│   ├── editar_registro.html
│   └── relatorios.html
├── static/                  # Arquivos estáticos
│   ├── css/
│   └── js/
├── requirements.txt         # Dependências
├── render.yaml              # Config Render
├── .env.example             # Exemplo de env
└── README.md                # Este arquivo
```

## 💻 Tecnologias

- **Backend**: Python 3.12 + Flask 3.0
- **Banco**: Supabase (PostgreSQL)
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Deploy**: Render.com
- **UI**: Bootstrap 5 + Font Awesome

## ✨ Screenshots

### Placar com Divisões
![Placar](https://via.placeholder.com/800x400?text=Placar+com+Divisoes)

### Placar Unificado
![Placar Unificado](https://via.placeholder.com/800x400?text=Placar+Sem+Divisoes)

### Registrar Atividade
![Registro](https://via.placeholder.com/800x400?text=Registrar+Atividade)

## 🔧 Desenvolvimento

```bash
# Instalar em modo desenvolvimento
pip install -r requirements.txt

# Executar com debug
export FLASK_ENV=development
python app_supabase.py
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Changelog

### v1.0.0 (2025-09-30)
- ✅ Sistema completo de placar
- ✅ Divisões automáticas
- ✅ Sistema de pontuação unificado (10 pontos)
- ✅ Edição e exclusão de registros
- ✅ Visualização com/sem divisões
- ✅ Campos de células (planejadas/realizadas/elite)
- ✅ Interface verde luxuosa
- ✅ Pronto para produção

## 💬 Suporte

Para suporte, abra uma [issue](https://github.com/LucasSlessa/Zero1_PLacar/issues) ou contate o desenvolvedor.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🌟 Autor

**Lucas Slessa**
- GitHub: [@LucasSlessa](https://github.com/LucasSlessa)

---

**Feito com ❤️ para a comunidade!**

🚀 [Deploy no Render](https://render.com) | 📘 [Documentação](HOSPEDAGEM_GRATUITA.md) | ⭐ [Star no GitHub](https://github.com/LucasSlessa/Zero1_PLacar)

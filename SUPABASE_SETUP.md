# 🚀 Configuração do Supabase para ZERO 1

## 📋 Passo a Passo Rápido

### 1. Acessar o Painel do Supabase
1. Acesse: https://zpkbloqlperdvozbkunp.supabase.co
2. Faça login na sua conta Supabase

### 2. Criar as Tabelas
1. No painel lateral, clique em **"SQL Editor"**
2. Clique em **"New Query"**
3. **Cole e execute este código SQL:**

```sql
-- Criar tabela de equipes
CREATE TABLE equipes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    pontuacao_total INTEGER DEFAULT 0,
    data_criacao TIMESTAMP DEFAULT NOW()
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

-- Habilitar RLS (Row Level Security) - opcional para desenvolvimento
ALTER TABLE equipes ENABLE ROW LEVEL SECURITY;
ALTER TABLE registros ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas as operações (para desenvolvimento)
CREATE POLICY "Enable all operations for equipes" ON equipes FOR ALL USING (true);
CREATE POLICY "Enable all operations for registros" ON registros FOR ALL USING (true);
```

4. Clique em **"RUN"** para executar

### 3. Verificar se Funcionou
1. No painel lateral, clique em **"Table Editor"**
2. Você deve ver duas tabelas:
   - **equipes** (com colunas: id, nome, pontuacao_total, data_criacao)
   - **registros** (com todas as colunas de atividades)

### 4. Executar o Sistema
```bash
cd /home/agrovisia/Desenvolvimento/placar
source venv/bin/activate
pip install -r requirements.txt
python app_supabase.py
```

### 5. Testar
- Acesse: http://localhost:5004
- Verifique status: http://localhost:5004/status

## ✅ Vantagens do Supabase

🚀 **PostgreSQL na nuvem** - Banco robusto e confiável  
☁️ **Backup automático** - Seus dados estão seguros  
🔄 **Tempo real** - Múltiplas pessoas podem usar simultaneamente  
📊 **Interface visual** - Pode ver/editar dados no painel  
🆓 **Gratuito** - Até 500MB e 2GB de transferência  
🔒 **Seguro** - Autenticação e autorização integradas  
📱 **API REST** - Fácil integração com outras ferramentas  

## 🔧 Estrutura das Tabelas

### Tabela `equipes`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | SERIAL | ID único da equipe |
| nome | VARCHAR(100) | Nome da equipe |
| pontuacao_total | INTEGER | Pontuação acumulada |
| data_criacao | TIMESTAMP | Data de criação |

### Tabela `registros`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | SERIAL | ID único do registro |
| equipe_id | INTEGER | Referência à equipe |
| data_inicio | DATE | Data início do período |
| data_fim | DATE | Data fim do período |
| qtd_pessoas | INTEGER | Quantidade de pessoas |
| qtd_pessoas_novas | INTEGER | Pessoas novas (10 pts cada) |
| qtd_celulas_elite | INTEGER | Células elite (15 pts cada) |
| qtd_pessoas_terca | INTEGER | Pessoas terça (5 pts cada) |
| qtd_pessoas_novas_terca | INTEGER | Pessoas novas terça (10 pts cada) |
| qtd_pessoas_arena | INTEGER | Pessoas arena (8 pts cada) |
| qtd_pessoas_novas_arena | INTEGER | Pessoas novas arena (15 pts cada) |
| qtd_pessoas_domingo | INTEGER | Pessoas domingo (3 pts cada) |
| qtd_pessoas_novas_domingo | INTEGER | Pessoas novas domingo (8 pts cada) |
| valor_arrecadacao_parceiro | DECIMAL(10,2) | Valor arrecadado (0.1 pt/real) |
| pontuacao | INTEGER | Pontuação calculada |
| data_registro | TIMESTAMP | Data/hora do registro |

## 🚨 Solução de Problemas

### Erro: "relation does not exist"
- Execute os comandos SQL no painel do Supabase
- Verifique se as tabelas foram criadas corretamente

### Erro: "permission denied"
- Verifique se as políticas RLS foram criadas
- Confirme que está usando a API Key correta

### Erro de conexão
- Verifique se a URL do projeto está correta
- Confirme se a API Key não expirou

## 📊 Visualizar Dados

No painel do Supabase:
1. Vá em **"Table Editor"**
2. Clique em **"equipes"** ou **"registros"**
3. Veja todos os dados em tempo real
4. Pode editar diretamente se necessário

## 🔄 Migração de Dados

Se você tem dados no modo demonstração, eles serão perdidos ao trocar para Supabase. O sistema começará limpo e você pode recadastrar as equipes e atividades.

## 🎉 Pronto!

Após executar os comandos SQL, o sistema estará pronto para produção com:
- ✅ Dados persistentes na nuvem
- ✅ Acesso simultâneo de múltiplos usuários  
- ✅ Backup automático
- ✅ Interface para visualizar dados
- ✅ Performance de banco PostgreSQL

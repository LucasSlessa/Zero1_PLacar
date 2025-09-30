# 🔄 Atualização do Supabase para Suportar Logos e Períodos

## ⚠️ IMPORTANTE - Leia Primeiro!

Este sistema foi atualizado com:
1. **Suporte a Logos** nas equipes
2. **Filtro de Períodos** no placar (já implementado)
3. **Persistência real no Supabase** (não mais em RAM)

## 📋 Passo 1: Atualizar Tabela no Supabase

Acesse o painel do Supabase em: https://zpkbloqlperdvozbkunp.supabase.co

### 1.1. Ir para SQL Editor

1. No painel lateral esquerdo, clique em **"SQL Editor"**
2. Clique em **"New Query"**

### 1.2. Executar SQL de Atualização

**Se você JÁ TEM a tabela `equipes` criada:**

```sql
-- Adicionar coluna logo_url na tabela existente
ALTER TABLE equipes ADD COLUMN IF NOT EXISTS logo_url TEXT;
ALTER TABLE equipes ADD COLUMN IF NOT EXISTS data_atualizacao TIMESTAMP DEFAULT NOW();

-- Atualizar timestamp automaticamente
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_equipes_modtime
    BEFORE UPDATE ON equipes
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
```

**Se você NÃO TEM as tabelas ainda (primeira vez):**

```sql
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

-- Trigger para atualização automática de data
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_equipes_modtime
    BEFORE UPDATE ON equipes
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
```

### 1.3. Executar o SQL

1. Cole o SQL apropriado no editor
2. Clique em **"Run"** (ou pressione Ctrl+Enter)
3. Verifique se apareceu "Success" ✅

## 📋 Passo 2: Iniciar o Servidor Correto

**ATENÇÃO:** Certifique-se de rodar o `app_supabase.py` e NÃO o `app_demo.py`

```bash
# Parar qualquer servidor rodando
pkill -f "python.*app"

# Ativar ambiente virtual
cd /home/agrovisia/Desenvolvimento/placar
source venv/bin/activate

# Rodar o app com Supabase
python app_supabase.py
```

O servidor deve iniciar na porta **5002** e mostrar:
```
🚀 ZERO 1 iniciado com Supabase!
🔗 Conectando em: https://zpkbloqlperdvozbkunp.supabase.co
✅ Tabelas já existem no Supabase!
```

## 🧪 Passo 3: Testar as Funcionalidades

### 3.1. Testar Cadastro de Equipe com Logo

1. Acesse: http://localhost:5002
2. Clique em "Cadastrar Nova Equipe"
3. Preencha:
   - Nome: Teste Logo
   - URL da Logo: https://via.placeholder.com/100
4. Cadastre e verifique se a logo aparece no placar

### 3.2. Testar Filtro por Período

1. No placar, veja o card "Filtrar Placar por Período"
2. Selecione:
   - Data Início: 2025-01-01
   - Data Fim: 2025-01-31
3. Clique em "Filtrar Período"
4. Ou use os botões rápidos: "Este Mês", "Mês Passado", "Este Ano"

### 3.3. Verificar Persistência no Supabase

1. Cadastre uma equipe
2. No painel do Supabase, vá em **"Table Editor"** > **"equipes"**
3. Verifique se a equipe apareceu lá ✅
4. Registre uma atividade
5. Vá em **"Table Editor"** > **"registros"**
6. Verifique se o registro apareceu lá ✅

## 🎯 Funcionalidades Implementadas

### ✅ Sistema de Logos
- Campo opcional de URL da logo no cadastro
- Campo de logo na edição de equipes
- Preview da logo no formulário de edição
- Exibição de logo no placar (40x40px)
- Ícone padrão quando não há logo

### ✅ Placar por Período
- Filtro com data início e fim
- Botões rápidos para períodos comuns
- Cálculo de pontuação apenas do período
- Exibição de pontuação do período + total
- Divisões baseadas na pontuação do período

### ✅ Persistência no Supabase
- Todas as operações salvam no Supabase
- Logs detalhados de operações (✅ sucesso / ❌ erro)
- Conexão configurada via .env
- Cascade delete para registros

## 🔍 Solução de Problemas

### "Dados não aparecem no Supabase"
**Solução:** Certifique-se de estar rodando `app_supabase.py` e não `app_demo.py`

### "Erro ao criar equipe"
**Solução:** Verifique se as credenciais no `.env` estão corretas e se as tabelas foram criadas

### "Logo não aparece"
**Possíveis causas:**
1. URL da imagem está incorreta
2. Imagem está bloqueada por CORS
3. URL não é acessível publicamente

**Solução:** Use serviços como:
- Imgur: https://imgur.com/upload
- ImgBB: https://imgbb.com/
- Placeholder: https://via.placeholder.com/100

### "Período não funciona"
**Solução:** Certifique-se de que:
1. Há registros com datas no período selecionado
2. As datas estão no formato correto (YYYY-MM-DD)

## 📌 URLs de Logos de Teste

Use estas URLs para testar:
```
https://via.placeholder.com/100/0000FF/FFFFFF?text=EQUIPE+1
https://via.placeholder.com/100/FF0000/FFFFFF?text=EQUIPE+2
https://via.placeholder.com/100/00FF00/FFFFFF?text=EQUIPE+3
```

## 🚀 Próximos Passos

Após confirmar que tudo está funcionando:
1. Cadastre suas equipes reais com logos
2. Registre atividades com datas variadas
3. Teste os filtros de período
4. Compartilhe o sistema com sua equipe!

---

**Sistema atualizado e pronto para uso! 🎉**

# 📋 Atualização do Sistema - Células e Novos Pesos

## 🎯 Mudanças Implementadas

### **1. Novos Campos Adicionados**
- ✅ `qtd_celulas` - Quantidade de células planejadas (informativo)
- ✅ `qtd_celulas_realizadas` - Células que aconteceram (10 pontos cada)

### **2. Sistema de Pontuação Atualizado**
Todos os pesos foram padronizados para **10 pontos**:

| Item | Peso Anterior | Peso Novo |
|------|--------------|-----------|
| Pessoas Novas | 10 | 10 ✅ |
| Células Realizadas | - | **10** 🆕 |
| Células Elite | 15 | **10** ⬇️ |
| Pessoas Terça | 5 | **10** ⬆️ |
| Pessoas Novas Terça | 10 | 10 ✅ |
| Pessoas Arena | 8 | **10** ⬆️ |
| Pessoas Novas Arena | 15 | **10** ⬇️ |
| Pessoas Domingo | 3 | **10** ⬆️ |
| Pessoas Novas Domingo | 8 | **10** ⬆️ |
| Arrecadação (por R$) | 0.1 | **10** ⬆️ |

## 🔧 Atualização do Banco de Dados Supabase

### **Passo 1: Adicionar Novos Campos na Tabela `registros`**

Execute no SQL Editor do Supabase:

```sql
-- Adicionar campo qtd_celulas (informativo - quantidade planejada)
ALTER TABLE registros 
ADD COLUMN IF NOT EXISTS qtd_celulas INTEGER DEFAULT 0;

-- Adicionar campo qtd_celulas_realizadas (pontua 10 cada)
ALTER TABLE registros 
ADD COLUMN IF NOT EXISTS qtd_celulas_realizadas INTEGER DEFAULT 0;

-- Adicionar comentários para documentação
COMMENT ON COLUMN registros.qtd_celulas IS 'Quantidade de células planejadas (informativo)';
COMMENT ON COLUMN registros.qtd_celulas_realizadas IS 'Quantidade de células que aconteceram (10 pontos cada)';
```

### **Passo 2: Verificar Estrutura Atualizada**

```sql
-- Listar todas as colunas da tabela registros
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'registros' 
ORDER BY ordinal_position;
```

### **Passo 3: (Opcional) Recalcular Pontuações Antigas**

Se quiser recalcular as pontuações dos registros antigos com os novos pesos:

```sql
-- Função para recalcular pontuação com novos pesos (todos = 10)
CREATE OR REPLACE FUNCTION recalcular_pontuacao_registro(registro_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    pontos INTEGER := 0;
    reg RECORD;
BEGIN
    SELECT * INTO reg FROM registros WHERE id = registro_id;
    
    IF NOT FOUND THEN
        RETURN 0;
    END IF;
    
    -- Todos os pesos = 10
    pontos := pontos + (reg.qtd_pessoas_novas * 10);
    pontos := pontos + (COALESCE(reg.qtd_celulas_realizadas, 0) * 10);
    pontos := pontos + (reg.qtd_celulas_elite * 10);
    pontos := pontos + (reg.qtd_pessoas_terca * 10);
    pontos := pontos + (reg.qtd_pessoas_novas_terca * 10);
    pontos := pontos + (reg.qtd_pessoas_arena * 10);
    pontos := pontos + (reg.qtd_pessoas_novas_arena * 10);
    pontos := pontos + (reg.qtd_pessoas_domingo * 10);
    pontos := pontos + (reg.qtd_pessoas_novas_domingo * 10);
    pontos := pontos + (reg.valor_arrecadacao_parceiro * 10);
    
    -- Atualizar pontuação
    UPDATE registros SET pontuacao = pontos WHERE id = registro_id;
    
    RETURN pontos;
END;
$$ LANGUAGE plpgsql;

-- Recalcular TODOS os registros
DO $$
DECLARE
    reg RECORD;
BEGIN
    FOR reg IN SELECT id FROM registros LOOP
        PERFORM recalcular_pontuacao_registro(reg.id);
    END LOOP;
END $$;

-- Recalcular totais das equipes
UPDATE equipes e
SET pontuacao_total = (
    SELECT COALESCE(SUM(pontuacao), 0)
    FROM registros r
    WHERE r.equipe_id = e.id
),
data_atualizacao = NOW();
```

## 📝 Arquivos Modificados

### **Backend (app_supabase.py)**
1. ✅ `PONTUACAO_CONFIG` - Todos os pesos = 10
2. ✅ `calcular_pontuacao()` - Incluído células realizadas
3. ✅ `criar_registro()` - Campos qtd_celulas e qtd_celulas_realizadas
4. ✅ `registrar_atividade()` - Captura novos campos do form

### **Frontend (registrar_atividade.html)**
1. ✅ Seção de células em 3 colunas:
   - Quantidade de Células (planejadas)
   - Células Realizadas (10 pontos)
   - Células Elite (10 pontos)
2. ✅ Todos os labels atualizados com "(10 pontos cada)"
3. ✅ JavaScript `calcularPontuacao()` atualizado

## ✅ Como Testar

1. **Adicione os campos no Supabase** (SQL acima)
2. **Reinicie o servidor Flask**
3. **Acesse Registrar Atividade**
4. **Preencha os novos campos:**
   - Quantidade de Células: 5
   - Células Realizadas: 4
   - Células Elite: 2
5. **Observe a pontuação calculada em tempo real**
6. **Registre e confira no placar**

## 🎨 Layout dos Novos Campos

```
┌─────────────────────────────────────────────────┐
│ Células                                         │
├──────────────┬──────────────┬──────────────────┤
│ Qtd Células  │ Realizadas   │ Elite            │
│ (planejadas) │ (10 pts)     │ (10 pts)         │
│ [____5____]  │ [____4____]  │ [____2____]      │
└──────────────┴──────────────┴──────────────────┘

Pontuação deste exemplo: 
- Células Realizadas: 4 × 10 = 40 pontos
- Células Elite: 2 × 10 = 20 pontos
- Total parcial: 60 pontos
```

## 🔄 Compatibilidade

- ✅ Registros antigos continuam funcionando
- ✅ Novos campos têm valor padrão 0
- ✅ Não quebra relatórios existentes
- ✅ Cálculo automático de pontuação atualizado

## 📊 Impacto na Pontuação

Com os novos pesos, as equipes podem pontuar mais facilmente:
- **Antes**: Variação de 0.1 a 15 pontos por item
- **Agora**: Todos os itens valem 10 pontos (mais justo!)

---

**Status**: ✅ Implementado no código  
**Próximo passo**: Executar SQL no Supabase  
**Data**: 30/09/2025

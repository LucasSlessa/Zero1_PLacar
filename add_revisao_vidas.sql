-- Script para adicionar coluna qtd_revisao_vidas na tabela registros
-- Execute este script no painel do Supabase

-- Adicionar coluna qtd_revisao_vidas na tabela registros
ALTER TABLE registros 
ADD COLUMN IF NOT EXISTS qtd_revisao_vidas INTEGER DEFAULT 0;

-- Comentário da coluna (opcional)
COMMENT ON COLUMN registros.qtd_revisao_vidas IS 'Quantidade de revisões de vida realizadas';

-- Verificar se a coluna foi adicionada
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'registros' AND column_name = 'qtd_revisao_vidas';

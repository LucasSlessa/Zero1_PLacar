# 📊 Configuração do Google Sheets para ZERO 1

## 🎯 Passo a Passo para Configurar

### 1. Criar Projeto no Google Cloud Console
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Anote o nome do projeto

### 2. Ativar APIs Necessárias
1. No menu lateral, vá em **APIs e Serviços > Biblioteca**
2. Procure e ative as seguintes APIs:
   - **Google Sheets API**
   - **Google Drive API**

### 3. Criar Conta de Serviço
1. Vá em **APIs e Serviços > Credenciais**
2. Clique em **+ CRIAR CREDENCIAIS > Conta de serviço**
3. Preencha:
   - **Nome**: ZERO1-Service
   - **Descrição**: Conta de serviço para sistema ZERO 1
4. Clique em **CRIAR E CONTINUAR**
5. Pule as próximas etapas clicando em **CONCLUÍDO**

### 4. Gerar Chave JSON
1. Na lista de contas de serviço, clique na conta criada
2. Vá na aba **CHAVES**
3. Clique em **ADICIONAR CHAVE > Criar nova chave**
4. Selecione **JSON** e clique em **CRIAR**
5. O arquivo será baixado automaticamente
6. **Renomeie o arquivo para `credentials.json`**
7. **Mova o arquivo para a pasta do projeto** (`/home/agrovisia/Desenvolvimento/placar/`)

### 5. Criar Planilha no Google Sheets
1. Acesse [Google Sheets](https://sheets.google.com/)
2. Crie uma nova planilha
3. Renomeie para **"ZERO 1 - Sistema de Placar"**
4. **Copie o ID da planilha** da URL:
   ```
   https://docs.google.com/spreadsheets/d/[ESTE_É_O_ID]/edit
   ```

### 6. Compartilhar Planilha
1. Na planilha criada, clique em **Compartilhar**
2. **Adicione o email da conta de serviço** (encontrado no arquivo credentials.json no campo `client_email`)
3. Defina permissão como **Editor**
4. Clique em **Enviar**

### 7. Configurar o Sistema
1. Abra o arquivo `app_sheets.py`
2. Na linha 15, substitua o `SPREADSHEET_ID` pelo ID copiado:
   ```python
   SPREADSHEET_ID = "SEU_ID_AQUI"
   ```

### 8. Instalar Dependências
```bash
cd /home/agrovisia/Desenvolvimento/placar
source venv/bin/activate
pip install -r requirements.txt
```

### 9. Executar o Sistema
```bash
python app_sheets.py
```

## 🔧 Estrutura da Planilha

O sistema criará automaticamente duas abas:

### Aba "Equipes"
| ID | Nome | Pontuacao_Total | Data_Criacao |
|----|------|-----------------|--------------|
| 1  | Exemplo | 150 | 2024-01-01 |

### Aba "Registros"
| ID | Equipe_ID | Equipe_Nome | Data_Inicio | Data_Fim | ... | Pontuacao |
|----|-----------|-------------|-------------|----------|-----|-----------|
| 1  | 1 | Exemplo | 2024-01-01 | 2024-01-07 | ... | 50 |

## ✅ Verificar Configuração

Acesse `http://localhost:5002/status` para verificar se tudo está funcionando:

```json
{
  "google_sheets_connected": true,
  "spreadsheet_id": "seu_id_aqui",
  "credentials_file": true
}
```

## 🚨 Solução de Problemas

### Erro: "credentials.json não encontrado"
- Verifique se o arquivo está na pasta correta
- Certifique-se que o nome está exato: `credentials.json`

### Erro: "Permission denied"
- Verifique se compartilhou a planilha com o email da conta de serviço
- Confirme que a permissão é de "Editor"

### Erro: "Spreadsheet not found"
- Verifique se o ID da planilha está correto no código
- Certifique-se que a planilha não foi deletada

## 🎉 Vantagens do Google Sheets

✅ **Acesso em tempo real** - Múltiplas pessoas podem ver os dados  
✅ **Backup automático** - Google cuida da segurança dos dados  
✅ **Fácil visualização** - Pode ver/editar direto no navegador  
✅ **Sem problemas de banco** - Não precisa se preocupar com SQLite  
✅ **Colaborativo** - Equipe pode acessar os dados diretamente  
✅ **Gratuito** - Não tem custo adicional  

## 📱 Acesso Móvel

Com Google Sheets, sua equipe pode:
- Ver o placar pelo celular
- Acompanhar dados em tempo real
- Fazer análises personalizadas
- Exportar relatórios facilmente

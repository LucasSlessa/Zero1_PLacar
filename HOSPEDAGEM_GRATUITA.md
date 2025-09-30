# 🚀 Hospedagem Gratuita - ZERO 1

Guia completo para hospedar o sistema ZERO 1 gratuitamente na nuvem.

---

## 🏆 Opção Recomendada: Render.com

**Render** oferece hospedagem gratuita permanente para aplicações Python/Flask.

### ✅ Vantagens:
- ✅ **100% Gratuito** (tier gratuito permanente)
- ✅ **SSL automático** (HTTPS)
- ✅ **Deploy automático** via GitHub
- ✅ **Fácil configuração**
- ✅ **Suporte a variáveis de ambiente**
- ⚠️ **Desvantagem**: App "dorme" após 15 min de inatividade (reinicia em ~30s)

### 📋 Passo a Passo - Render.com

#### **1. Preparar Arquivos do Projeto**

Crie um arquivo `requirements.txt` na raiz do projeto:

```bash
cd /home/agrovisia/Desenvolvimento/placar
pip freeze > requirements.txt
```

Ou crie manualmente com as dependências principais:

```txt
Flask==3.0.0
supabase==2.3.0
python-dotenv==1.0.0
gunicorn==21.2.0
Werkzeug==3.0.1
```

#### **2. Criar arquivo `render.yaml`**

Crie na raiz do projeto:

```yaml
services:
  - type: web
    name: zero1-placar
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app_supabase:app
    envVars:
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.12.0
```

#### **3. Criar `.gitignore`**

Se ainda não existe:

```txt
venv/
__pycache__/
*.pyc
.env
*.db
.vscode/
.idea/
```

#### **4. Fazer Push para GitHub**

```bash
# Já foi feito, mas caso precise:
git add .
git commit -m "Preparado para deploy no Render"
git push origin main
```

#### **5. Deploy no Render**

1. **Acesse**: https://render.com
2. **Crie conta gratuita** (pode usar GitHub)
3. **Clique**: "New +" → "Web Service"
4. **Conecte o GitHub**: Autorize o Render a acessar seu repositório
5. **Selecione**: `Zero1_PLacar`
6. **Configure**:
   - **Name**: `zero1-placar`
   - **Region**: Oregon (US West) - mais rápido BR
   - **Branch**: `main`
   - **Root Directory**: (deixe vazio)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app_supabase:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: **Free** ✅

7. **Adicionar Variáveis de Ambiente**:
   - Clique em "Advanced"
   - Adicione:
     - `SUPABASE_URL` = `https://zpkbloqlperdvozbkunp.supabase.co`
     - `SUPABASE_KEY` = `sua_chave_do_supabase`

8. **Clique**: "Create Web Service"

9. **Aguarde**: Deploy ~5 minutos

10. **Acesse**: `https://zero1-placar.onrender.com` 🎉

---

## 🔧 Configurações Adicionais Render

### **Manter App Sempre Ativo**

O app gratuito "dorme" após 15 min. Para mantê-lo ativo:

**Opção 1: Cron-Job (Recomendado - Gratuito)**

Use **cron-job.org**:
1. Acesse: https://cron-job.org
2. Crie conta gratuita
3. Adicione job:
   - **URL**: `https://zero1-placar.onrender.com/status`
   - **Interval**: A cada 10 minutos
   - **Enabled**: Sim

**Opção 2: UptimeRobot (Gratuito)**

1. Acesse: https://uptimerobot.com
2. Crie monitor:
   - **URL**: `https://zero1-placar.onrender.com`
   - **Type**: HTTP(s)
   - **Interval**: 5 minutos

---

## 🎯 Alternativas Gratuitas

### **2. Railway.app**

- ✅ **Muito fácil de usar**
- ✅ **Deploy automático GitHub**
- ⚠️ **Limite**: 500 horas/mês (gratuito)
- 🔗 https://railway.app

**Deploy Railway:**
1. Acesse railway.app
2. "Start a New Project" → "Deploy from GitHub"
3. Selecione repositório
4. Adicione variáveis de ambiente
5. Deploy automático!

### **3. PythonAnywhere**

- ✅ **Especializado em Python**
- ✅ **Sempre ativo**
- ⚠️ **Configuração manual**
- 🔗 https://www.pythonanywhere.com

**Deploy PythonAnywhere:**
1. Crie conta gratuita
2. Bash console:
```bash
git clone https://github.com/LucasSlessa/Zero1_PLacar.git
cd Zero1_PLacar
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Configure Web App manual

### **4. Fly.io**

- ✅ **Moderno e rápido**
- ✅ **3 apps gratuitos**
- ⚠️ **Requer cartão (não cobra)**
- 🔗 https://fly.io

**Deploy Fly.io:**
```bash
# Instale CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
fly launch
fly secrets set SUPABASE_URL=sua_url
fly secrets set SUPABASE_KEY=sua_key
fly deploy
```

### **5. Vercel (Serverless)**

- ✅ **Muito rápido**
- ⚠️ **Requer adaptação para serverless**
- 🔗 https://vercel.com

---

## 📊 Comparação

| Plataforma | Gratuito | Sempre Ativo | Facilidade | SSL | Limite |
|------------|----------|--------------|------------|-----|--------|
| **Render** | ✅ Sim | ⚠️ Dorme 15min | ⭐⭐⭐⭐⭐ | ✅ | Ilimitado |
| Railway | ✅ Sim | ✅ Sim | ⭐⭐⭐⭐⭐ | ✅ | 500h/mês |
| PythonAnywhere | ✅ Sim | ✅ Sim | ⭐⭐⭐ | ✅ | 1 app |
| Fly.io | ✅ Sim | ✅ Sim | ⭐⭐⭐⭐ | ✅ | 3 apps |
| Vercel | ✅ Sim | ✅ Sim | ⭐⭐⭐ | ✅ | Serverless |

---

## 🔒 Segurança - Variáveis de Ambiente

**⚠️ IMPORTANTE**: Nunca commite o arquivo `.env` com suas credenciais!

### **Como Configurar no Render:**

1. Dashboard do serviço
2. "Environment" no menu lateral
3. Adicionar variável:
   - Key: `SUPABASE_URL`
   - Value: Sua URL do Supabase
4. Adicionar outra:
   - Key: `SUPABASE_KEY`
   - Value: Sua chave anon do Supabase
5. "Save Changes"

---

## 🌐 Domínio Personalizado (Opcional)

### **Opção 1: Domínio Gratuito**

**Freenom** (domínios .tk, .ml, .ga):
- https://www.freenom.com
- Registre domínio gratuito
- Configure DNS no Render

### **Opção 2: Subdomínio Gratuito**

Use o padrão do Render:
- `https://zero1-placar.onrender.com`

Para customizar:
- Settings → "Custom Domains"
- Adicione seu domínio

---

## 🚀 Deploy Rápido - Checklist

- [ ] ✅ Criar `requirements.txt`
- [ ] ✅ Criar `render.yaml`
- [ ] ✅ Adicionar `.gitignore`
- [ ] ✅ Push para GitHub
- [ ] ✅ Criar conta Render.com
- [ ] ✅ Conectar repositório
- [ ] ✅ Adicionar variáveis de ambiente
- [ ] ✅ Deploy!
- [ ] ✅ Configurar cron-job (opcional)
- [ ] ✅ Testar aplicação

---

## 🆘 Problemas Comuns

### **1. App não inicia**
```bash
# Verifique logs no Render Dashboard
# Geralmente falta gunicorn
pip install gunicorn
```

### **2. Erro de importação**
```bash
# Certifique-se que requirements.txt está completo
pip freeze > requirements.txt
```

### **3. Variáveis de ambiente não funcionam**
- Verifique se adicionou no Render Dashboard
- Reinicie o serviço após adicionar

### **4. App muito lento**
- Normal no tier gratuito após "acordar"
- Use cron-job para manter ativo

---

## 💰 Custos

**Render Gratuito:**
- ✅ Hospedagem: **R$ 0,00**
- ✅ SSL: **R$ 0,00**
- ✅ Supabase (até 500MB): **R$ 0,00**
- ✅ Bandwidth: **100GB/mês grátis**
- **Total: R$ 0,00/mês** 🎉

---

## 📱 Acesso Móvel

Após deploy, acesse de qualquer dispositivo:
- 📱 **Mobile**: https://zero1-placar.onrender.com
- 💻 **Desktop**: https://zero1-placar.onrender.com
- 🖥️ **Tablet**: https://zero1-placar.onrender.com

---

## 📚 Links Úteis

- 🏠 **Render**: https://render.com
- 📖 **Docs Render**: https://render.com/docs
- 🗄️ **Supabase**: https://supabase.com
- 📦 **Repositório**: https://github.com/LucasSlessa/Zero1_PLacar
- ⏰ **Cron-Job**: https://cron-job.org
- 📊 **UptimeRobot**: https://uptimerobot.com

---

## 🎓 Próximos Passos

1. ✅ **Deploy no Render** (recomendado)
2. ✅ **Configurar cron-job** para manter ativo
3. ✅ **Testar em produção**
4. ✅ **Compartilhar URL** com equipe
5. ✅ **Monitorar uso** no dashboard

---

**Sistema pronto para produção! 🚀**

Escolha Render.com para começar em minutos!

# 🚀 Deploy Rápido - 5 Minutos

Guia ultra-rápido para colocar o ZERO 1 no ar **AGORA**!

---

## ✅ Checklist Pré-Deploy

- [x] ✅ Código no GitHub: `https://github.com/LucasSlessa/Zero1_PLacar`
- [x] ✅ `requirements.txt` criado
- [x] ✅ `render.yaml` configurado
- [x] ✅ `.gitignore` adicionado
- [x] ✅ README.md completo

**Status**: 🟢 PRONTO PARA DEPLOY!

---

## 🎯 Deploy em 5 Passos

### **1️⃣ Acesse Render.com** (30 segundos)
```
👉 https://render.com
```
- Clique em "Get Started for Free"
- Entre com GitHub (recomendado)

### **2️⃣ Crie Web Service** (30 segundos)
- Clique no botão "New +" no canto superior
- Selecione "Web Service"

### **3️⃣ Conecte Repositório** (1 minuto)
- Autorize Render a acessar GitHub
- Selecione: **Zero1_PLacar**
- Clique "Connect"

### **4️⃣ Configure Serviço** (2 minutos)

**Configurações Básicas:**
```yaml
Name: zero1-placar
Region: Oregon (US West)
Branch: main
Runtime: Python 3
```

**Build & Start:**
```bash
Build Command: pip install -r requirements.txt
Start Command: gunicorn app_supabase:app --bind 0.0.0.0:$PORT
```

**Plano:**
```
Instance Type: Free (✅ GRATUITO)
```

### **5️⃣ Adicione Variáveis** (1 minuto)

Clique em **"Advanced"** e adicione:

```env
SUPABASE_URL
👉 https://zpkbloqlperdvozbkunp.supabase.co

SUPABASE_KEY
👉 [Sua chave do Supabase]
```

**Onde encontrar:**
1. Acesse seu projeto no Supabase
2. Settings → API
3. Copie "Project URL" e "anon public"

---

## 🎉 DEPLOY!

Clique em **"Create Web Service"**

⏱️ Aguarde ~5 minutos...

✅ **URL do seu app**: `https://zero1-placar.onrender.com`

---

## 🔧 Configuração Extra (Opcional)

### **Manter App Ativo 24/7**

O app gratuito "dorme" após 15 min sem uso.

**Solução: Cron-Job.org (GRÁTIS)**

1. Acesse: https://cron-job.org
2. Crie conta gratuita
3. Novo job:
   - **Título**: Zero1 Keep Alive
   - **URL**: `https://zero1-placar.onrender.com/status`
   - **Intervalo**: A cada 10 minutos
   - **Enable**: ✅

**Pronto!** App sempre ativo! 🚀

---

## 📱 Testando

### **1. Acesse a URL**
```
https://zero1-placar.onrender.com
```

### **2. Navegue pelo Sistema**
- 🏠 Home
- 🏆 Placar
- ➕ Cadastrar Equipe
- 📝 Registrar Atividade
- 📊 Relatórios

### **3. Compartilhe**
Envie a URL para sua equipe! 🎉

---

## 🆘 Problemas?

### **App não carrega**
- Aguarde 30s (primeira requisição é lenta)
- Verifique logs no Dashboard Render
- Confirme variáveis de ambiente

### **Erro 500**
- Veja logs no Render
- Verifique SUPABASE_URL e SUPABASE_KEY
- Confirme que tabelas existem no Supabase

### **"Application Error"**
```bash
# No dashboard Render, clique em "Manual Deploy"
# Selecione "Clear build cache & deploy"
```

---

## 💰 Custos

```
Render Free Tier:     R$ 0,00/mês
Supabase Free:        R$ 0,00/mês
Domínio .onrender:    R$ 0,00/mês
SSL/HTTPS:            R$ 0,00/mês
──────────────────────────────
TOTAL:                R$ 0,00/mês ✅
```

**100% GRATUITO PARA SEMPRE!** 🎉

---

## 🌐 URLs

**Sua aplicação:**
```
🌍 Produção: https://zero1-placar.onrender.com
📊 Status:   https://zero1-placar.onrender.com/status
⚙️ Admin:    https://dashboard.render.com
```

**Supabase:**
```
🗄️ Database: https://supabase.com/dashboard/project/[seu-id]
📊 Tables:   https://supabase.com/dashboard/project/[seu-id]/editor
```

---

## 🎯 Próximos Passos

1. ✅ **Testar todas as funcionalidades**
2. ✅ **Configurar cron-job** (keep alive)
3. ✅ **Cadastrar equipes**
4. ✅ **Registrar atividades**
5. ✅ **Compartilhar com equipe**
6. 🎉 **Começar a usar!**

---

## 📞 Suporte

- 📖 [Documentação Completa](HOSPEDAGEM_GRATUITA.md)
- 🐛 [Reportar Bug](https://github.com/LucasSlessa/Zero1_PLacar/issues)
- 💬 [Discussões](https://github.com/LucasSlessa/Zero1_PLacar/discussions)

---

## 🚀 Dica Pro

**Domínio Personalizado (Gratuito):**

Render permite conectar domínio próprio GRÁTIS!

1. Registre domínio em: https://www.freenom.com
2. No Render: Settings → Custom Domain
3. Adicione seu domínio
4. Configure DNS conforme instruções
5. SSL automático incluído! ✅

---

**🎉 PARABÉNS! SEU SISTEMA ESTÁ NO AR! 🎉**

Acesse agora: **https://zero1-placar.onrender.com**

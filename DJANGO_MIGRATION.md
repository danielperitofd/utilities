# 🔄 Migração de Flask para Django

O projeto BmpConverter foi convertido de **Flask** para **Django**!

## 📁 Estrutura do Projeto Django

```
bmpconverter/
├── config/                      # Configurações do Django
│   ├── __init__.py
│   ├── settings.py             # Configurações gerais
│   ├── urls.py                 # URLs/Rotas
│   └── wsgi.py                 # WSGI para produção
│
├── converter/                   # App principal
│   ├── __init__.py
│   ├── apps.py                 # Configuração da app
│   └── views.py                # Views (lógica)
│
├── templates/                   # Templates HTML
│   └── index.html
│
├── static/                      # Arquivos estáticos
│   ├── styles.css
│   └── converted/              # Imagens convertidas
│
├── media/                       # Uploads e conversões
│   ├── uploads/                # Imagens carregadas
│   └── converted/              # BMPs convertidas
│
├── manage.py                    # Gerenciador Django
├── requirements_django.txt      # Dependências (Django)
└── requirements.txt             # Dependências (Flask - antigo)
```

## 🚀 Como Executar (Django)

### 1️⃣ Criar e Ativar Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

### 2️⃣ Instalar Dependências

```bash
pip install -r requirements_django.txt
```

### 3️⃣ Coletar Arquivos Estáticos (Produção)

```bash
python manage.py collectstatic --noinput
```

### 4️⃣ Rodar em Desenvolvimento

```bash
python manage.py runserver
```

Acesse: **http://localhost:8000**

### 5️⃣ Rodar em Produção (com Gunicorn)

```bash
gunicorn config.wsgi:application --workers 4 --bind 0.0.0.0:5000
```

## 📋 Arquivo settings.py

O arquivo `config/settings.py` contém:

- **BASE_DIR**: Diretório raiz
- **SECRET_KEY**: Chave de segurança (altere em produção!)
- **DEBUG**: `True` em desenvolvimento, `False` em produção
- **INSTALLED_APPS**: Apps instalados (apenas `converter`)
- **TEMPLATES**: Configuração de templates
- **MEDIA_ROOT/MEDIA_URL**: Pasta de uploads
- **STATIC_ROOT/STATIC_URL**: Pasta de estáticos

## 🔗 URLs Disponíveis

| Rota | Método | Função |
|------|--------|---------|
| `/` | GET/POST | Upload e conversão de imagens |
| `/download-image/<filename>/` | GET | Download de uma imagem |
| `/download-selected/` | POST | Download de selecionadas |
| `/download-all/` | POST | Download de todas |
| `/clear-images/` | POST | Limpar uploads e conversões |

## 📊 Comparação Flask vs Django

### Flask (Antigo)
- ✅ Leve e simples
- ✅ Menos boilerplate
- ❌ Menos segurança padrão
- ❌ Escalabilidade limitada

### Django (Novo)
- ✅ Framework completo
- ✅ Segurança integrada (CSRF, SQL Injection protection)
- ✅ ORM poderoso
- ✅ Admin interface
- ✅ Melhor para projetos maiores
- ❌ Mais "pesado"

## 🔐 Segurança

Django inclui proteções automáticas:
- **CSRF Protection**: Token `{% csrf_token %}` nos formulários
- **SQL Injection**: ORM protegido
- **XSS Prevention**: Templates escapam HTML por padrão
- **HTTPS Ready**: Configurável em produção

## 🌐 Deploy no Linux

Atualize o arquivo de serviço systemd:

```bash
sudo nano /etc/systemd/system/bmpconverter.service
```

```ini
[Unit]
Description=BMP Converter Django App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/utilities
Environment="PATH=/var/www/utilities/venv/bin"
ExecStart=/var/www/utilities/venv/bin/gunicorn config.wsgi:application --workers 4 --bind 127.0.0.1:5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Depois:

```bash
sudo systemctl daemon-reload
sudo systemctl restart bmpconverter
```

## 📝 Notas

- Os arquivos Flask (`app.py`) continuam no repositório
- A estrutura antiga em `utilities_old/` permanece intacta
- Ambos os projetos (Flask e Django) podem coexistir
- Para usar Django, use `requirements_django.txt`
- Para voltar ao Flask, use `requirements.txt` e rode `python app.py`

---

**Framework**: Django 5.0.1  
**Python**: 3.8+  
**Servidor**: Gunicorn + Cloudflare Tunnel

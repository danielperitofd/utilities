BmpConverter

BmpConverter é uma aplicação web simples desenvolvida com Python e Flask, que permite ao usuário carregar imagens, redimensioná-las e convertê-las para o formato BMP. A aplicação oferece uma interface intuitiva, onde as imagens convertidas podem ser visualizadas e baixadas individualmente ou em lote, com a opção de limpar o cache de imagens convertidas.

Funcionalidades

Upload de Imagens: Carregue várias imagens de uma vez através da interface web.
Redimensionamento: Escolha as dimensões para redimensionar as imagens antes da conversão.
Conversão para BMP: As imagens carregadas são automaticamente convertidas para o formato BMP.
Visualização em Galeria: Visualize as imagens convertidas em uma galeria interativa.
Download das Imagens: Faça o download de imagens selecionadas ou de todas as imagens convertidas.
Limpeza de Cache: Opção de limpar as imagens convertidas armazenadas, removendo-as do servidor.
Tecnologias Utilizadas

Python (Linguagem de Programação)
Flask (Framework Web)
HTML, CSS e JavaScript (Front-end)
Pillow (Biblioteca para Manipulação de Imagens)
Bootstrap (Framework CSS para estilização)
Como Executar o Projeto Localmente

Pré-requisitos
Python 3.6 ou superior
Pip (gerenciador de pacotes do Python)
Virtualenv (recomendado para criar um ambiente virtual)

Para clonar esse repositorio:

git clone https://github.com/seu-usuario/BmpConverter.git
cd BmpConverter

ATIVANDO AMBIENTE VIRRUAL

python -m venv venv
source venv/bin/activate  # No Windows, use: venv\Scripts\activate

INSTALANDO AS DEPENDÊNCIAS 

pip install -r requirements.txt


RODANDO A APLICACAO 

python app.py


ESTRUTURA DO PROJETO

BmpConverter/
│
├── app.py                 # Código principal da aplicação Flask
├── requirements.txt       # Lista de dependências do projeto
├── README.md              # Descrição do projeto
│
├── static/
│   ├── css/
│   │   └── styles.css     # Arquivo de estilo CSS personalizado
│   └── converted/         # Pasta para armazenar imagens convertidas
│
├── templates/
│   └── index.html         # Template HTML principal
│
├── uploads/               # Pasta para armazenar imagens carregadas
└── output/                # Pasta para armazenar arquivos temporários




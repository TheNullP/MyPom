# 🍅 MyPom - Seu Companheiro de Foco

O **MyPom** é uma aplicação completa de produtividade baseada na Técnica Pomodoro. Diferente de cronômetros simples, o MyPom oferece um ecossistema focado em dados, permitindo que você não apenas foque, mas analise sua evolução ao longo do tempo.

## 🚀 Funcionalidades Principais

- **Página Pomodoro Interativa:** Cronômetro inteligente com persistência de estado (não para se você atualizar a página ou mudar de aba).
    
- **Dashboard de Relatórios:** Visualização de progresso diário, semanal e mensal com gráficos comparativos de produtividade.
    
- **Sistema de Configurações:** (Em desenvolvimento) Personalização de tempos e preferências.
    
- **Persistência de Dados:** Histórico de sessões salvo para análise de longo prazo.
    

## 🛠️ Tecnologias Utilizadas

O projeto utiliza uma stack moderna e robusta:

- **Backend:** FastAPI (Python) - Alta performance e documentação automática.
    
- **Frontend:** HTML5, CSS3 (Flexbox/Grid) e JavaScript puro (Vanilla JS).
    
- **Template Engine:** Jinja2 para renderização dinâmica no servidor.
    
- **Banco de Dados:** PostgreSQL rodando em ambiente isolado via **Docker**.
    
- **Migrações:** Alembic para versionamento controlado do esquema do banco de dados.
    

## 📦 Arquitetura e Infraestrutura

O projeto foi desenhado para ser escalável e fácil de configurar:

>  **Docker & Banco de Dados:** O PostgreSQL é orquestrado via container, garantindo que o ambiente de desenvolvimento seja idêntico ao de produção. **Alembic:** Utilizamos o Alembic para garantir que todas as alterações na estrutura do banco (tabelas de usuários, sessões, etc.) sejam versionadas, permitindo "voltar no tempo" se necessário.

## 🔧 Como Rodar o Projeto

1. **Clone o repositório:**
    
    ```
    git clone https://github.com/TheNullP/MyPom.git
    cd mypom
    ```
    
2. **Configure o Ambiente:**
    
    - Crie um arquivo `.env` baseado no `.env.example`.
        
    - Suba o banco de dados com Docker:
        
        ```
        docker compose up -d
        ```
        
3. **Instale as Dependências (Poetry):**
    
    ```
    poetry install
    ```
    
4. **Execute as Migrações:**
    
    ```
    alembic upgrade head
    ```
    
5. **Inicie a Aplicação:**
    
    ```
    fastapi dev MyPom/app.py
    ```
    

## 🧠 O que aprendi neste projeto

- **Persistência no Cliente:** Uso de `localStorage` e lógica de _timestamps_ para manter o timer sincronizado entre páginas.
    
- **UX/UI com CSS Puro:** Construção de dashboards complexos e mapas de calor sem depender de bibliotecas externas pesadas.
    
- **Integração de Sistemas:** Comunicação fluida entre o JavaScript do frontend e as rotas assíncronas do FastAPI.

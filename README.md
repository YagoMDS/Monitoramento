# Web Scraping - Monitoramento de Preços no Mercado Livre

## Descrição
Este projeto foi desenvolvido com o objetivo de monitorar e analisar a variação de preços de produtos no Mercado Livre ao longo do tempo, utilizando a API do Mercado Livre e técnicas de **Web Scraping** com **Python**.

## Funcionalidades
- **Coleta de Dados**: Utiliza a API do Mercado Livre para buscar informações sobre os preços de produtos.
- **Armazenamento**: Dados são armazenados em um banco de dados PostgreSQL, permitindo fácil acesso e análise.
- **Visualização**: Gráficos dinâmicos são gerados para mostrar as variações de preços ao longo do tempo.
- **Envio de E-mails**: Sistema integrado para enviar alertas de mudanças significativas nos preços dos produtos monitorados.

## Tecnologias Utilizadas
- **Python**
- **API do Mercado Livre**
- **PostgreSQL**
- **pandas (para manipulação e análise de dados)**
- **requests (para fazer requisições HTTP)**
- **Matplotlib (para gráficos)**
- **yagmail (para envio de e-mails)**

## Dados Sigilosos
As credenciais e outros dados sensíveis, como a chave da API do Mercado Livre e informações de e-mail, estão armazenados em um arquivo `.env` para garantir a segurança e facilitar a configuração. Não compartilhe esse arquivo publicamente.

## Como Executar
**1. Clone o repositório:**


      git clone https://github.com/YagoMDS/Monitoramento.git
   
**2. Instale as dependências:**

      
      pip install -r requirements.txt
   
**3. Crie o arquivo .env na raiz do projeto com as seguintes variáveis:**

      API_KEY=<Sua_Chave_API_Mercado_Livre>
      EMAIL=<Seu_E-mail>
      EMAIL_PASSWORD=<Sua_Senha_De_E-mail>
   
**4. Configure seu banco de dados PostgreSQL.**

**5. Execute o script:**
      python main.py

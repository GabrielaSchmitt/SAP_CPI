<h1 align="center">
  <br>SAP CPI</h1>

**SAP_CPI** é uma aplicação web voltada à analise de dados dos fluxos de uma empresa dentro do SAP CPI ( [Integration Suite](https://help.sap.com/docs/cloud-integration?locale=en-US&version=Cloud) ) desenvolvido com Streamlit realizando consultas com a API do sistema gerando gráficos e relatórios pertinentes que hoje não são dispostas de maneira agradavel.

### Acesse o aplicativo pelo link https://sapcpi.streamlit.app/ 

## Principais Funcionalidades

- **Consumo de Mensagem**: Acessa o ambiente com o cookies do seu usuário logado e faz diversas requisições com o filtro de data desejado, afim de concatenar os retorno somando o consumo do fluxo no período.
- **Fluxos em execução**: Utiliza a API e requisições dispostas pela SAP para recuperar a lista de fluxos que estão agendadas para execução. Criado afim de prevenir que sejam agendados fluxos com baixa recorrência apenas com gráficos. 

<br>

### Como rodar o código na sua máquina

1. Baixe as bibliotecas necessárias

   ```
    pip install -r requirements.txt
   ```

2. Rode o app

   ```
    streamlit run streamlit_app.py
   ```

<br>

✨ Obrigada pela atenção! ✨

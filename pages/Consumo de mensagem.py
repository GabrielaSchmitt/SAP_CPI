import streamlit as st
from streamlit_extras.colored_header import colored_header

# Script libraries
import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# gif
import base64
import time

st.set_page_config(
    page_title="Consumo de mensagem",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="auto",
)

# Botão Dark/Light Mode 
if "theme" not in st.session_state:
    st.session_state.theme = st.config.get_option("theme.base")
    st.session_state.theme == "light"

with st.sidebar:
    
    # Get the current theme and create a button to switch themes
    if st.session_state.theme == "light":
        switch = st.button("🌙")  # Light mode button
    else:
        switch = st.button("🌞")  # Dark mode button

    # Check the button value and toggle the theme
    if switch:
        if st.session_state.theme == "light":
            st.session_state.theme = "dark"
            st.config.set_option("theme.base", "dark")
        else:
            st.session_state.theme = "light"
            st.config.set_option("theme.base", "light")
        st.rerun()

# Função iterando pelo json de resposta da chamada filtrando pelo nome da integração
def filter_integration_flows(json_data, flow_name_to_match):
    # Initialize an empty list to collect data
    filtered_data = []
    
    # Loop through the JSON data
    for item in json_data:
        source_dt = item.get('source_dt', None)

        # Check if the 'artifactDetails' key exists
        if 'artifactDetails' in item['message_details']:
            for artifact in item['message_details']['artifactDetails']:
                # Check if the 'iFlowName' matches the user-provided name
                if artifact['iFlowName'] == flow_name_to_match:
                    # Append relevant details to the list
                    filtered_data.append({
                        'Date': source_dt,
                        'Integration Flow Name': artifact['iFlowName'],
                        'Chargeable Msg': artifact['chargeableMsg'],
                        'MPL Count': artifact['mplCount']
                    })
    
    # Create a DataFrame from the collected data
    df = pd.DataFrame(filtered_data)
    
    return df

# Função para chamada da API com range de data aplicado
def fetch_data_for_date_range(start_date, end_date, flow_name_to_match):
    # Convert strings to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Initialize an empty DataFrame to collect all data
    all_data = pd.DataFrame()
    
    # Generate a date range
    current_date = start_date
    while current_date <= end_date:
        try:
            # Define parameters for the GET request
            params = {
                "date": current_date.strftime("%Y-%m-%d"),
                "download": "false",
                "runtimeLocationId": "cloudintegration"
            }

            # Make the GET request
            response = requests.get(url, headers=headers, params=params)

            # Check the status code and handle the response
            if response.status_code == 200 and response.content:
                df = filter_integration_flows(response.json(), flow_name_to_match)
                all_data = pd.concat([all_data, df], ignore_index=True)
            elif response.status_code == 200 and not response.content:
                st.warning(f"Não há dados para a data {current_date.strftime('%d-%m-%Y')}. Status code: {response.status_code}")
            elif response.status_code == 401:   
                st.warning(f"Ocorreu um erro para a requisição de {current_date.strftime('%d-%m-%Y')}. Altere os cookies informados. Status code: {response.status_code}")
            else:
                st.error(f"Falha recuperando dados para {current_date.strftime('%d-%m-%Y')}. Status code: {response.status_code}")
        
        except Exception as e:
            st.error(f"Um erro ocorreu para {current_date.strftime('%d-%m-%Y')}: {e}" , icon="🚨")
        
        # Move to the next date
        current_date += timedelta(days=1)

    
    return all_data

# Função para mostrar gif tutorial
def display_gif_tutorial():
    # Load the GIF file
    with open("/workspaces/blank-app/assets/GetCookiesTutorial.gif", "rb") as file_:
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")

    dialog = st.dialog("Como baixar cookies?")
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="Get Cookies Tutorial gif">',
        unsafe_allow_html=True,
    )

    time.sleep(42)
    st.session_state.show_dialog = False  
    st.rerun()  

# Função para plotar gráfico 
def plot_data(df, flow_name_to_match):
    # Sum the data by Date
    df['Date'] = pd.to_datetime(df['Date'])
    df_sum = df.groupby('Date').sum()

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_sum.plot(kind='bar', ax=ax)
    ax.set_title(f'Integration Flow Name: {flow_name_to_match}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sum')
    ax.set_xticks(range(len(df_sum.index)))
    ax.set_xticklabels(df_sum.index.strftime('%Y-%m-%d'), rotation=45)
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

colored_header(
    label="Consumo de mensagem 💡",
    description="Consumo de mensagens para um determinado fluxo de integração em um ambiente SAP CPI",
    color_name="light-blue-70",)


# Define the API endpoint 
#environment = "https://gfn-qas-cw2itya8.integrationsuite.cfapps.br10.hana.ondemand.com"

option = st.selectbox('Por gentileza selecione o ambiente:',
('DEV - desenvolvimento', 'QAS - qualidade', 'PRD - producao'))
st.caption(f"Ambiente selecionado: {option}")

if option=='DEV - desenvolvimento':
    environment = "https://gfn-dev-hkto43i5.integrationsuite.cfapps.br10.hana.ondemand.com"
if option=='QAS - qualidade':
    environment = "https://gfn-qas-cw2itya8.integrationsuite.cfapps.br10.hana.ondemand.com"
if option=='PRD - producao':
    environment = "https://gfn-prd-9n1xwzyx.integrationsuite.cfapps.br10.hana.ondemand.com"
        
endpoint = "/rest/api/v1/metering/usage/specific-date"
url = environment+endpoint


col1, col2 = st.columns([4, 1])

# Coluna 1 (Campo de entrada para Cookies)
with col1:
    cookies = st.text_input('Cookies da página:', '')

# Coluna 2 (Botão com explicação de como baixar os cookies)
with col2:
    st.markdown("""
        <style>
         /* Ajustar para a altura do campo de input */
        div.stButton > button {
            margin-top: 10px;
            height: 40px;
        }
        </style>  """, unsafe_allow_html=True)
    if st.button('🍪'):
        if st.session_state.show_dialog == False:
            st.session_state.show_dialog = True
        else:
            st.session_state.show_dialog = False
        #st.session_state.show_dialog = True


# Initialize session state for dialog tracking
if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = False

# Show the dialog if the state is true
if st.session_state.show_dialog:
    display_gif_tutorial()

# Define the headers to mimic the browser request
# In case the status return unauthorized, inspect your browser's network, retrieve the content of the tag Cookie and rerun
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Cookie": cookies,
    "Host": environment[8:],
    "Referer": environment+"/shell/monitoring/MessageUsage",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

# flow_name_to_match = 'LO_Transpofrete_GetInvoices'
flow_name_to_match = st.text_input('Nome da Integração:')

# start_date = "2024-09-01"
# end_date = "2024-09-05"

cl1, cl2 = st.columns(2)

with cl1:
    start_date = st.date_input("Data Inicial:", format="YYYY-MM-DD", value=None)

with cl2:
    end_date = st.date_input("Data final:", format="YYYY-MM-DD", value=None)
    if end_date == None:
        end_date = start_date
    else:
        delta = (end_date - start_date).days / 30
        if delta > 6: st.error("O intervalo entre a data inicial e a data final não pode ser maior que 6 meses.")
        if start_date > end_date: st.error("A data inicial não pode ser posterior à data final.")

if st.button("Run"):
    if start_date == None : st.error(f"Preencha o campo de Data.")
    if flow_name_to_match == "" : st.error(f"Preencha o campo de Integração.")
    if cookies == "" : st.error(f"Preencha o campo de Cookies.")

    if start_date != None and flow_name_to_match != "" and cookies != "":
        df = fetch_data_for_date_range(str(start_date), str(end_date), flow_name_to_match)
        if not df.empty: 
            st.dataframe(df)

            plot_data(df, flow_name_to_match)


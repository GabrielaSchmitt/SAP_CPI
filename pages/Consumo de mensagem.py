import streamlit as st
from streamlit_extras.colored_header import colored_header

# Script libraries
import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

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
        switch = st.button("🌞")  # Light mode button
    else:
        switch = st.button("🌙")  # Dark mode button

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
        # Define parameters for the GET request
        params = {
            "date": current_date.strftime("%Y-%m-%d"),
            "download": "false",
            "runtimeLocationId": "cloudintegration"
        }
        
        # Make the GET request
        response = requests.get(url, headers=headers, params=params)
        
        # Check the status code and handle the response
        if response.status_code == 200:
            df = filter_integration_flows(response.json(), flow_name_to_match)
            all_data = pd.concat([all_data, df], ignore_index=True)
        else:
            print(f"Failed to get data for {current_date.strftime('%Y-%m-%d')}. Status code: {response.status_code}")
        
        # Move to the next date
        current_date += timedelta(days=1)
    
    return all_data

#st.title("Consumo de mensagem")

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

cookies = "notice_preferences=1:; notice_gdpr_prefs=0,1::implied,eu; cmapi_gtm_bl=ta-asp-bzi-sp-awct-cts-csm-img-flc-fls-mpm-mpr-m6d-tc-tdc; cmapi_cookie_privacy=permit 1,2 functional; __VCAP_ID__=540dffba-2264-4e92-5545-09e9; JSESSIONID=s%3AVK750xu8Jq4WXeQaYm5qykULVWkfo3Il.B1R954Xy2ddyG5%2FDCQsrxUCmenkopPMMBi6s50dcXws"
cookies = st.text_input('Insira aqui os Cookies da página:')

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
flow_name_to_match = st.text_input('Insira aqui o nome da Integração:')

# start_date = "2024-09-01"
# end_date = "2024-09-05"

cl1, cl2 = st.columns(2)

with cl1:
    start_date = st.date_input("Data Inicial:", format="YYYY-MM-DD", value=None)

with cl2:
    end_date = st.date_input("Data final:", format="YYYY-MM-DD", value=None)
    if end_date == "":
        end_date = start_date

if st.button("Run"):
    df = fetch_data_for_date_range(str(start_date), str(end_date), flow_name_to_match)

    st.dataframe(df)

import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Função para carregar os dados de um arquivo CSV
def carregar_dados():
    if os.path.exists("disponibilidade.csv"):
        return pd.read_csv("disponibilidade.csv")
    else:
        return pd.DataFrame(columns=['Professor', 'Unidades', 'Carro', 'Máquinas', 'Disponibilidade', 'Módulo', 'Observações', 'Nome do Preenchendor', 'Data'])

# Função para salvar dados em um arquivo CSV
def salvar_dados(df):
    df.to_csv("disponibilidade.csv", index=False)

# Função para deletar uma linha específica
def deletar_linha(index):
    st.session_state.df_disponibilidade = st.session_state.df_disponibilidade.drop(index).reset_index(drop=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success(f"Linha {index} deletada com sucesso!")

# Função para autenticar e criar um serviço do Google Sheets
def autenticar_google_sheets():
    credentials = service_account.Credentials.from_service_account_info({
        "type": "service_account",
        "project_id": "projeto-teste-435314",
        "private_key_id": "7235b9adddc1a5421ecbad17905a25bc5c8d4e66",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDtv7nwTpjAwpcU\n5ectM1wcje5AWUTaQr9uR3Gw/D/Az9pzROyUdfbNxEIvTtWuKZfFvi3pFDuc/PBt\nO9ynf74ohRFl+gpgz1KXyc0EJdAqbIm3ZORHRBkq3OEDRnCM4WbjGVT9TldEziYq\nlzPojzDWsu2ESspV7E2u9/h3br5NlVUmevM1a7xy7oZyqquAir11dCGQM056VqVW\naevu+NHZXmsDadNM2BmZ5FKBBhgSvVVW6pNlqFPWPGDszQcGcc+mLfCr2TjLqOq3\nh46f0i0qnarr+C5gMQaun6Hdhy2hkUUTNCZnnN0710PcFRXAw/04FIw/nfUZWZ8A\n+RgqI75xAgMBAAECggEAC7dKRNjsBvm/42WAoCtbA27iGgqGzautjn7CT/AKUz3a\n8cRof9jAALwGbUQ5BvlhPjsk54rEn56eWX+yRrsmkOLH10rnBoYeTOvCqOI/0SC3\n+PvlkkvSjVhvqo88KNEga8S55GFfLxKVR72GRGmur4cx6bZGz3eoN10HF0RI5/6W\n2n+PIPSKS/K97JL3R8BdO0NqAKgv6EL+gHZ0lH4/c/gLT3Mh6l+ajtGHXYb6lR5A\nSe3QfaSScowRs1vi5mCbmiTXlXVFzGTN7K8dgsLf5vp9UfYhwanFw6j41MItkkrV\n52IoXHOK20SrL57TaT37UIa6gf297S1F1rDJpUn9XQKBgQD5d6zjn5y6OQP7uAHf\nG/ZCDrsWINckK2XMgHdtkvF3RAzB1otbq9DqWu++sL7KGqXmObI00kMtrhso4L0P\n9LT7yfgebS6NARM3CImLcPk8DOW+jS9hyFELK8t0UzZMmY3Ql6kP8RNj1Q4ctQ3b\n2UoST2J5ThpV9JHjj9ztuX70dQKBgQDz+X6oei1emY/sV2mPtAb9z+YbV54fqgiB\n1+mZXFOPb/OKvLXhRZrkJXvimBjYZRw+YjG8ty3khUs3rtL0gVauIq7lpedc39BJ\nw4GN2dX56BU8nMMMWoGxexhBgrSftEt+S1txJjbGLiCl0X3LUIHVTtq43zJkfFx7\nglczJY9yjQKBgEA8I4Vc9PMyeScYo0q6nXc26c9x11PV5Nl6fsX1Hz3RhONoheut\n2xZtIexdAFNz9yHH224kce3SNeYZsDTqkqt+vue+v0zJaRQzm48PIO3oeEPPgNLR\nzKRuu22Re5rPsydx1bNoJNEA7ChSKmZgleUPEdEgXkGhvur0gTOpHtp9AoGBAKP+\nDJkKpvxzlD5080vY4uowmKfAWVVHYbiFfUvMt44u3jFfb5Igy2CXoZJKUkkCjd2Q\n+4WyS3LT9h9TsBER70XVomJTBhVzi/pJJAhJaH829S9s396p54t5BnDifq7q7ePS\nm4CPAzprPx62livXza2n93VU8faBcVjD4AFNOgLxAoGAIhtjjRY9/pqXIYhDIVyS\nA0WkCT83FR02/VhnDFYC3HohSnYp/5q3U9QagzMhHiJSCsyFiGKBevaIPZvdXKUd\ngjZBtyeTEAX1bColxYEEoiad/WX0GpuIGQga6iUwUyGA32sIe2iVPl+6TMsWbcfj\nQn5zB+tzp169E1gkEhu4Rhw=\n-----END PRIVATE KEY-----\n",
        "client_email": "carlos-teste@projeto-teste-435314.iam.gserviceaccount.com",
        "client_id": "113052231256616111730",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/carlos-teste%40projeto-teste-435314.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    })
    
    service = build('sheets', 'v4', credentials=credentials)
    return service

# Função para salvar os dados no Google Sheets
def salvar_no_google_sheets(df):
    service = autenticar_google_sheets()
    spreadsheet_id = '1KqpZSsnNsDzcb-I75ys0-RmByKSiMtLv6r41-GHk8bE'
    range_name = 'Sheet1!A1'  # Altere para o nome da aba e intervalo onde os dados serão inseridos
    
    # Converte o DataFrame para uma lista de listas
    values = [df.columns.tolist()] + df.values.tolist()
    
    body = {
        'values': values
    }
    
    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name,
                                                     valueInputOption='RAW', body=body)
    response = request.execute()
    st.success("Dados salvos com sucesso no Google Sheets!")

# Carregar os dados salvos (se houver) ao iniciar a aplicação
if 'df_disponibilidade' not in st.session_state:
    st.session_state.df_disponibilidade = carregar_dados()

# Título do dashboard
st.title("Dashboard de Disponibilidade")

# Coletando o nome de quem preencheu o formulário
nome_preenchedor = st.text_input("Digite seu nome:")

# Coleta a data da modificação
data_modificacao = st.date_input("Data da modificação", value=datetime.today())

# Formata a data para DD/MM/YYYY
data_modificada_formatada = data_modificacao.strftime("%d/%m/%Y")

st.write(f"Data selecionada: {data_modificada_formatada}")

# Nomes iniciais dos professores
nomes_iniciais = ['Pessoa A']

# Lista de unidades
unidades = ['Satélite', 'Vicentina', 'Jardim', 'Online']

# Inicializa o session state se não estiver definido
if 'disponibilidade' not in st.session_state:
    st.session_state.disponibilidade = {nome: {} for nome in nomes_iniciais}

# Tabela de disponibilidade e checkboxes por unidade
st.subheader("Tabela de Disponibilidade:")

# Define a largura das colunas
col_widths = [1, 1, 1, 1, 1, 1, 1]

# Adicionando CSS para melhorar a visualização
st.markdown(
    """
    <style>
    .checkbox-no-wrap {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .dataframe {
        border-collapse: collapse;
        width: 100%;
    }
    .dataframe th, .dataframe td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    .dataframe tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .dataframe th {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

for i, nome_inicial in enumerate(nomes_iniciais):
    cols = st.columns(col_widths)

    with cols[0]:
        nome_professor = st.text_input(f"Nome do professor", nome_inicial, key=f"nome_{i}")

    # Atualiza o nome do professor no session state
    if nome_professor != nome_inicial:
        st.session_state.disponibilidade[nome_professor] = st.session_state.disponibilidade.pop(nome_inicial, {})

    # Atualiza o dicionário com base no session state
    if nome_professor not in st.session_state.disponibilidade:
        st.session_state.disponibilidade[nome_professor] = {}

    with cols[1]:
        st.write("Unidades")
        for unidade in unidades:
            st.session_state.disponibilidade[nome_professor][unidade] = st.checkbox(f"{unidade}", 
                value=st.session_state.disponibilidade[nome_professor].get(unidade, False), 
                key=f"{nome_professor}_{unidade}")

    with cols[2]:
        st.write("Carro")
        st.session_state.disponibilidade[nome_professor]['Carro'] = st.checkbox("Tem carro", 
            value=st.session_state.disponibilidade[nome_professor].get('Carro', False), 
            key=f"{nome_professor}_carro")

    with cols[3]:
        st.write("Máquina")
        maquinas = {}
        with st.container():
            st.markdown('<div class="checkbox-no-wrap">', unsafe_allow_html=True)
            maquinas['Notebook'] = st.checkbox("Notebook", 
                value='Notebook' in st.session_state.disponibilidade[nome_professor].get('Máquina', []), 
                key=f"{nome_professor}_notebook")
            maquinas['Computador'] = st.checkbox("Computador", 
                value='Computador' in st.session_state.disponibilidade[nome_professor].get('Máquina', []), 
                key=f"{nome_professor}_computador")
            maquinas['NDA'] = st.checkbox("NDA", 
                value='NDA' in st.session_state.disponibilidade[nome_professor].get('Máquina', []), 
                key=f"{nome_professor}_nda")
            st.markdown('</div>', unsafe_allow_html=True)
        st.session_state.disponibilidade[nome_professor]['Máquina'] = [key for key, value in maquinas.items() if value]

    with cols[4]:
        st.write("Disponibilidade")
        periodos = ['Manhã', 'Tarde', 'Noite', 'Sábado']
        disponibilidade_horarios = {}
        with st.container():
            st.markdown('<div class="checkbox-no-wrap">', unsafe_allow_html=True)
            for periodo in periodos:
                disponibilidade_horarios[periodo] = st.checkbox(periodo, 
                    value=periodo in st.session_state.disponibilidade[nome_professor].get('Disponibilidade', []), 
                    key=f"{nome_professor}_{periodo}")
            st.markdown('</div>', unsafe_allow_html=True)
        st.session_state.disponibilidade[nome_professor]['Disponibilidade'] = [key for key, value in disponibilidade_horarios.items() if value]

    with cols[5]:
        st.write("Módulo")
        modulo_opcoes = {}
        with st.container():
            st.markdown('<div class="checkbox-no-wrap">', unsafe_allow_html=True)
            modulo_opcoes['Stage 1'] = st.checkbox("Stage 1", 
                value='Stage 1' in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                key=f"{nome_professor}_stage1")
            modulo_opcoes['VIP'] = st.checkbox("VIP", 
                value='VIP' in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                key=f"{nome_professor}_vip")
            modulo_opcoes['CONVERSATION'] = st.checkbox("CONVERSATION", 
                value='CONVERSATION' in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                key=f"{nome_professor}_conversation")
            modulo_opcoes['MBA'] = st.checkbox("MBA", 
                value='MBA' in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                key=f"{nome_professor}_mba")
            st.markdown('</div>', unsafe_allow_html=True)
        st.session_state.disponibilidade[nome_professor]['Modulo'] = [key for key, value in modulo_opcoes.items() if value]

    with cols[6]:
        st.write("Observações")
        observacoes = st.text_area("Observações", 
            value=st.session_state.disponibilidade[nome_professor].get('Observações', ''), 
            key=f"{nome_professor}_observacoes")
        st.session_state.disponibilidade[nome_professor]['Observações'] = observacoes

# Função para converter os dados para DataFrame
def converter_para_dataframe(dados, nome_usuario, data):
    registros = []
    for professor, detalhes in dados.items():
        registro = {
            'Professor': professor,
            'Unidades': ', '.join([unidade for unidade, selecionado in detalhes.items() if unidade in unidades and selecionado]),
            'Carro': 'Sim' if detalhes.get('Carro', False) else 'Não',
            'Máquinas': ', '.join(detalhes['Máquina']),
            'Disponibilidade': ', '.join(detalhes['Disponibilidade']),
            'Módulo': ', '.join(detalhes['Modulo']),
            'Observações': detalhes.get('Observações', ''),
            'Nome do Preenchendor': nome_usuario,
            'Data': data.strftime('%Y-%m-%d')  # Garantindo que a data seja formatada sem hora
        }
        registros.append(registro)
    return pd.DataFrame(registros)

# Converter os dados coletados para um DataFrame
df_novo = converter_para_dataframe(st.session_state.disponibilidade, nome_preenchedor, data_modificacao)

# Botão para salvar os dados na tabela em tempo real
if st.button("Salvar dados"):
    st.session_state.df_disponibilidade = pd.concat([st.session_state.df_disponibilidade, df_novo], ignore_index=True)
    salvar_dados(st.session_state.df_disponibilidade)
    salvar_no_google_sheets(df_novo)  # Salva no Google Sheets também
    st.success("Dados salvos com sucesso!")

# Definir uma lista de usuários com permissões especiais
usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]

# Verificar se o nome do preenchedor está na lista de usuários com permissões especiais
if nome_preenchedor in usuarios_superadmin:
    st.subheader("Tabela Atualizada de Disponibilidade")

    # Iterar sobre as linhas do DataFrame e exibir as informações com botões de deletar
    for i, row in st.session_state.df_disponibilidade.iterrows():
        cols = st.columns(len(row) + 1)  # +1 para o botão de deletar
        for j, value in enumerate(row):
            cols[j].write(value)
        
        # Exibir o botão de deletar apenas se o nome do preenchedor estiver na lista de permissões
        if cols[len(row)].button("Deletar", key=f"delete_{i}"):
            deletar_linha(i)

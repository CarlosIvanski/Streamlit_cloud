import streamlit as st
import pandas as pd
import os
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
    credentials_info = {
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
    }
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
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
    
    try:
        request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name,
                                                         valueInputOption='RAW', body=body)
        response = request.execute()
        st.success("Dados salvos com sucesso no Google Sheets!")
    except Exception as e:
        st.error(f"Erro ao salvar no Google Sheets: {e}")

# Função principal do Streamlit
def main():
    st.title("Gerenciamento de Disponibilidade")
    
    if 'df_disponibilidade' not in st.session_state:
        st.session_state.df_disponibilidade = carregar_dados()
    
    menu = st.sidebar.selectbox("Escolha uma opção", ["Adicionar Dados", "Deletar Dados", "Visualizar Dados"])
    
    if menu == "Adicionar Dados":
        st.header("Adicionar Dados")
        professor = st.text_input("Professor")
        unidades = st.text_input("Unidades")
        carro = st.checkbox("Tem carro")
        maquinas = st.checkbox("Tem máquinas")
        disponibilidade = st.text_input("Disponibilidade")
        modulo = st.text_input("Módulo")
        observacoes = st.text_area("Observações")
        nome_preenchendor = st.text_input("Nome do Preenchendor")
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if st.button("Salvar"):
            nova_linha = pd.DataFrame([[professor, unidades, carro, maquinas, disponibilidade, modulo, observacoes, nome_preenchendor, data]],
                                      columns=['Professor', 'Unidades', 'Carro', 'Máquinas', 'Disponibilidade', 'Módulo', 'Observações', 'Nome do Preenchendor', 'Data'])
            st.session_state.df_disponibilidade = pd.concat([st.session_state.df_disponibilidade, nova_linha], ignore_index=True)
            salvar_dados(st.session_state.df_disponibilidade)
            salvar_no_google_sheets(st.session_state.df_disponibilidade)
    
    elif menu == "Deletar Dados":
        st.header("Deletar Dados")
        if not st.session_state.df_disponibilidade.empty:
            index = st.number_input("Índice da linha a ser deletada", min_value=0, max_value=len(st.session_state.df_disponibilidade) - 1)
            if st.button("Deletar"):
                deletar_linha(index)
        else:
            st.write("Nenhum dado disponível para deletar.")
    
    elif menu == "Visualizar Dados":
        st.header("Visualizar Dados")
        st.write(st.session_state.df_disponibilidade)

if __name__ == "__main__":
    main()

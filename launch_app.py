import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import BytesIO
from datetime import datetime

# Configuração das credenciais e conexão com o Google Sheets
def conectar_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("caminho/para/seu/arquivo-credenciais.json", scope)
    client = gspread.authorize(creds)
    return client

# Função para carregar dados do Google Sheets
def carregar_dados_google_sheets(sheet_id):
    client = conectar_google_sheets()
    sheet = client.open_by_key(sheet_id).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Função para salvar dados no Google Sheets
def salvar_dados_google_sheets(df, sheet_id):
    client = conectar_google_sheets()
    sheet = client.open_by_key(sheet_id).sheet1
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# ID da planilha do Google Sheets
sheet_id = "1KqpZSsnNsDzcb-I75ys0-RmByKSiMtLv6r41-GHk8bE"

# Carregar dados do Google Sheets ao iniciar a aplicação
if 'df_disponibilidade' not in st.session_state:
    st.session_state.df_disponibilidade = carregar_dados_google_sheets(sheet_id)

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
            'Unidades': ', '.join([unidade for unidade, valor in detalhes.items() if valor and unidade in unidades]),
            'Carro': 'Sim' if detalhes.get('Carro') else 'Não',
            'Máquinas': ', '.join(detalhes.get('Máquina', [])),
            'Disponibilidade': ', '.join(detalhes.get('Disponibilidade', [])),
            'Módulo': ', '.join(detalhes.get('Modulo', [])),
            'Observações': detalhes.get('Observações', ''),
            'Nome do Preenchendor': nome_usuario,
            'Data': data
        }
        registros.append(registro)
    return pd.DataFrame(registros)

# Exibir a tabela de dados atualizada
st.subheader("Tabela Atualizada de Disponibilidade:")
df_disponibilidade = converter_para_dataframe(st.session_state.disponibilidade, nome_preenchedor, data_modificada_formatada)

# Exibir a tabela
st.dataframe(df_disponibilidade)

# Verifica se há dados novos para salvar
if st.button("Salvar Dados"):
    st.session_state.df_disponibilidade = df_disponibilidade
    salvar_dados_google_sheets(st.session_state.df_disponibilidade, sheet_id)
    st.success("Dados salvos no Google Sheets com sucesso!")

# Função para deletar linha, só disponível para Bruno
if nome_preenchedor == "Bruno":
    linha_para_deletar = st.number_input("Insira o índice da linha para deletar:", min_value=0, max_value=len(st.session_state.df_disponibilidade)-1, step=1)
    if st.button("Deletar Linha"):
        deletar_linha(linha_para_deletar)
else:
    st.warning("Você não tem permissão para deletar dados.")

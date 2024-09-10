import streamlit as st
import pandas as pd
import os
import io  # Importar o módulo io
from datetime import datetime

# Função para carregar os dados de um arquivo CSV
def carregar_dados():
    if os.path.exists("disponibilidade.csv"):
        return pd.read_csv("disponibilidade.csv")
    else:
        return pd.DataFrame(columns=['Professor', 'Unidades', 'Carro', 'Máquinas', 'Disponibilidade', 'Módulo', 'Observações', 'Nome do Preenchendor', 'Data', 'Hora'])

# Função para salvar dados em um arquivo CSV
def salvar_dados(df):
    df.to_csv("disponibilidade.csv", index=False)

# Função para deletar uma linha específica
def deletar_linha(index):
    st.session_state.df_disponibilidade = st.session_state.df_disponibilidade.drop(index).reset_index(drop=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success(f"Linha {index} deletada com sucesso!")

# Carregar os dados salvos (se houver) ao iniciar a aplicação
st.session_state.df_disponibilidade = carregar_dados()

# Título do dashboard
st.title("Dashboard de Disponibilidade")

# Coletando o nome de quem preencheu o formulário
nome_preenchedor = st.text_input("Digite seu nome:")

# Coletando a data e hora da modificação
if 'data_modificacao' not in st.session_state:
    st.session_state.data_modificacao = datetime.today().date()
if 'hora_modificacao' not in st.session_state:
    st.session_state.hora_modificacao = datetime.now().time()

data_modificacao = st.date_input("Data da modificação", value=st.session_state.data_modificacao)
hora_modificacao = st.time_input("Hora da modificação", value=st.session_state.hora_modificacao)

# Atualizar o session state com os novos valores
st.session_state.data_modificacao = data_modificacao
st.session_state.hora_modificacao = hora_modificacao

# Garantir que um nome seja fornecido
if nome_preenchedor:
    st.write(f"Obrigado, {nome_preenchedor}, suas respostas foram registradas!")
else:
    st.warning("Por favor, preencha seu nome para continuar.")

# Nome do único professor (não será exibido diretamente, será usado internamente)
nome_professor_unico = "Professor Único"

# Lista de unidades
unidades = ['Satélite', 'Vicentina', 'Jardim', 'Online']

# Inicializa o session state se não estiver definido
if 'disponibilidade' not in st.session_state:
    st.session_state.disponibilidade = {nome_professor_unico: {}}

# Tabela de disponibilidade e checkboxes por unidade
st.subheader("Tabela de Disponibilidade:")

# Define a largura das colunas
col_widths = [1, 1.5, 1, 1.5, 1, 1.5, 2]  # Reduzindo o tamanho das colunas para ajustar o layout

# Adicionando CSS para melhorar a visualização
st.markdown(
    """
    <style>
    .checkbox-no-wrap {
        display: flex;
        flex-direction: column;  /* Mantém os checkboxes organizados em coluna */
        gap: 2px;  /* Reduzindo o espaçamento entre os checkboxes */
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

cols = st.columns(col_widths)

# Atualiza o dicionário com base no session state
if nome_professor_unico not in st.session_state.disponibilidade:
    st.session_state.disponibilidade[nome_professor_unico] = {}

with cols[0]:
    st.write("Unidades")
    # Adicionar checkboxes para cada unidade
    for unidade in unidades:
        st.session_state.disponibilidade[nome_professor_unico][unidade] = st.checkbox(f"{unidade}", 
            value=st.session_state.disponibilidade[nome_professor_unico].get(unidade, False), 
            key=f"{nome_professor_unico}_{unidade}")

with cols[1]:
    st.write("Carro")
    # Adicionar checkbox para o carro
    st.session_state.disponibilidade[nome_professor_unico]['Carro'] = st.checkbox("Tem carro", 
        value=st.session_state.disponibilidade[nome_professor_unico].get('Carro', False), 
        key=f"{nome_professor_unico}_carro")

with cols[2]:
    st.write("Máquina")
    # Adicionar checkboxes para selecionar múltiplas máquinas
    maquinas = {}
    with st.container():
        st.markdown('<div class="checkbox-no-wrap">', unsafe_allow_html=True)
        maquinas['Notebook'] = st.checkbox("Notebook", 
            value='Notebook' in st.session_state.disponibilidade[nome_professor_unico].get('Máquina', []), 
            key=f"{nome_professor_unico}_notebook")
        maquinas['Computador'] = st.checkbox("Computador", 
            value='Computador' in st.session_state.disponibilidade[nome_professor_unico].get('Máquina', []), 
            key=f"{nome_professor_unico}_computador")
        maquinas['NDA'] = st.checkbox("NDA", 
            value='NDA' in st.session_state.disponibilidade[nome_professor_unico].get('Máquina', []), 
            key=f"{nome_professor_unico}_nda")
        st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.disponibilidade[nome_professor_unico]['Máquina'] = [key for key, value in maquinas.items() if value]

with cols[3]:
    st.write("Disponibilidade")
    # Adicionar checkboxes para cada período
    periodos = ['Manhã', 'Tarde', 'Noite', 'Sábado']
    disponibilidade_horarios = {}
    with st.container():
        st.markdown('<div class="checkbox-no-wrap">', unsafe_allow_html=True)
        for periodo in periodos:
            disponibilidade_horarios[periodo] = st.checkbox(periodo, 
                value=periodo in st.session_state.disponibilidade[nome_professor_unico].get('Disponibilidade', []), 
                key=f"{nome_professor_unico}_{periodo}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.disponibilidade[nome_professor_unico]['Disponibilidade'] = [key for key, value in disponibilidade_horarios.items() if value]

with cols[4]:
    st.write("Módulo")
    # Adicionar checkboxes para as novas opções: Stage 1, VIP, CONVERSATION e MBA
    modulo_opcoes = {}
    with st.container():
        st.markdown('<div class="checkbox-no-wrap">', unsafe_allow_html=True)
        modulo_opcoes['Stage 1'] = st.checkbox("Stage 1", 
            value='Stage 1' in st.session_state.disponibilidade[nome_professor_unico].get('Modulo', []), 
            key=f"{nome_professor_unico}_stage1")
        modulo_opcoes['VIP'] = st.checkbox("VIP", 
            value='VIP' in st.session_state.disponibilidade[nome_professor_unico].get('Modulo', []), 
            key=f"{nome_professor_unico}_vip")
        modulo_opcoes['CONVERSATION'] = st.checkbox("CONVERSATION", 
            value='CONVERSATION' in st.session_state.disponibilidade[nome_professor_unico].get('Modulo', []), 
            key=f"{nome_professor_unico}_conversation")
        modulo_opcoes['MBA'] = st.checkbox("MBA", 
            value='MBA' in st.session_state.disponibilidade[nome_professor_unico].get('Modulo', []), 
            key=f"{nome_professor_unico}_mba")
        st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.disponibilidade[nome_professor_unico]['Modulo'] = [key for key, value in modulo_opcoes.items() if value]

with cols[5]:
    st.write("Observações")
    # Adicionar uma caixa de texto para observações
    observacoes = st.text_area("Observações", 
        value=st.session_state.disponibilidade[nome_professor_unico].get('Observações', ''), 
        key=f"{nome_professor_unico}_observacoes")
    st.session_state.disponibilidade[nome_professor_unico]['Observações'] = observacoes

# Função para converter os dados para DataFrame
def converter_para_dataframe(dados, nome_usuario, data, hora):
    registros = []
    for professor, detalhes in dados.items():
        registro = {
            'Professor': professor,
            'Unidades': ', '.join([unidade for unidade, selecionado in detalhes.items() if unidade in unidades and selecionado]),
            'Carro': 'Sim' if detalhes.get('Carro', False) else 'Não',
            'Máquinas': ', '.join(detalhes['Máquina']),
            'Disponibilidade': ', '.join(detalhes['Disponibilidade']),
            'Módulo': ', '.join(detalhes['Modulo']),
            'Observações': detalhes.get('Observações', ''),  # Incluindo observações
            'Nome do Preenchendor': nome_usuario,
            'Data': data.strftime('%Y-%m-%d'),
            'Hora': hora.strftime('%H:%M')  # Hora da modificação
        }
        registros.append(registro)
    return pd.DataFrame(registros)

# Converter os dados coletados para um DataFrame
df_novo = converter_para_dataframe(st.session_state.disponibilidade, nome_preenchedor, data_modificacao, hora_modificacao)

# Botão para salvar os dados na tabela em tempo real
if st.button("Salvar dados"):
    st.session_state.df_disponibilidade = pd.concat([st.session_state.df_disponibilidade, df_novo]).drop_duplicates().reset_index(drop=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success("Dados salvos com sucesso!")

# Exibir a tabela atualizada no site com bordas e botão de deletar
st.subheader("Tabela Atualizada de Disponibilidade")

# Exibir a tabela com os botões de deletar
for i, row in st.session_state.df_disponibilidade.iterrows():
    cols = st.columns(len(row) + 1)  # +1 para o botão de deletar
    for j, value in enumerate(row):
        cols[j].write(value)
    # Adicionar botão de deletar
    if cols[len(row)].button("Deletar", key=f"delete_{i}"):
        deletar_linha(i)

# Botão para exportar os dados para Excel
st.subheader("Exportar Dados para Excel")
if st.button("Exportar para Excel"):
    # Usar um BytesIO buffer para evitar problemas com diretórios
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        st.session_state.df_disponibilidade.to_excel(writer, index=False, sheet_name='Disponibilidade')
    buffer.seek(0)
    
    # Streamlit download button
    st.download_button(
        label="Baixar Excel",
        data=buffer,
        file_name="disponibilidade_professores.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

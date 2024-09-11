import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# Função para carregar os dados do CSV
def carregar_dados():
    try:
        return pd.read_csv('disponibilidade.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Dia', 'Período', 'Disponibilidade'])

# Função para salvar os dados no CSV
def salvar_dados(df):
    df.to_csv('disponibilidade.csv', index=False)

# Função para deletar uma linha pelo índice
def deletar_linha(index):
    # Remover a linha do DataFrame
    st.session_state.df_disponibilidade = st.session_state.df_disponibilidade.drop(index).reset_index(drop=True)
    
    # Salvar o DataFrame atualizado no CSV
    salvar_dados(st.session_state.df_disponibilidade)
    
    # Mostrar mensagem de sucesso
    st.success(f"Linha {index} deletada com sucesso!")
    
    # Recarregar os dados para refletir as alterações imediatamente
    st.session_state.df_disponibilidade = carregar_dados()

# Verifica se já existe um DataFrame carregado no estado da sessão
if 'df_disponibilidade' not in st.session_state:
    st.session_state.df_disponibilidade = carregar_dados()

# Interface de input para adicionar nova disponibilidade
st.title('Gestão de Disponibilidade')
dia = st.selectbox('Selecione o dia', ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'])
periodo = st.selectbox('Selecione o período', ['Manhã', 'Tarde', 'Noite'])
disponibilidade = st.selectbox('Disponível?', ['Sim', 'Não'])

# Botão para adicionar nova disponibilidade
if st.button('Adicionar Disponibilidade'):
    novo_dado = {'Dia': dia, 'Período': periodo, 'Disponibilidade': disponibilidade}
    st.session_state.df_disponibilidade = st.session_state.df_disponibilidade.append(novo_dado, ignore_index=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success('Disponibilidade adicionada com sucesso!')

# Exibe a tabela atualizada de disponibilidade
st.subheader('Tabela Atualizada de Disponibilidade')

# Exibe a tabela de forma interativa
st.dataframe(st.session_state.df_disponibilidade)

# Permite deletar uma entrada específica
st.subheader('Deletar uma Entrada')

# Exibe a tabela com botões para deletar cada linha
for i, row in st.session_state.df_disponibilidade.iterrows():
    cols = st.columns(len(row) + 1)  # +1 para o botão de deletar
    for j, value in enumerate(row):
        cols[j].write(value)

    # Exibir o botão de deletar
    if cols[len(row)].button("Deletar", key=f"delete_{i}"):
        deletar_linha(i)

# Botão para exportar os dados como Excel
st.markdown('### Exportar para Excel')
if st.button('Exportar'):
    st.session_state.df_disponibilidade.to_excel('disponibilidade.xlsx', index=False)
    st.success('Dados exportados com sucesso para Excel!')

    # Botão para exportar os dados para Excel, visível para todos os usuários na lista de permissões especiais
    st.subheader("Exportar Dados para Excel")
    if st.button("Exportar para Excel"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.df_disponibilidade.to_excel(writer, index=False, sheet_name='Disponibilidade')
        buffer.seek(0)
        
        st.download_button(
            label="Baixar Excel",
            data=buffer,
            file_name="disponibilidade_professores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

import streamlit as st
import pandas as pd
import io
import os

# Função para carregar os dados
def carregar_dados():
    if os.path.exists("disponibilidade.csv"):
        return pd.read_csv("disponibilidade.csv")
    else:
        return pd.DataFrame(columns=['Professor', 'Unidades', 'Carro', 'Máquinas', 'Disponibilidade', 'Módulo', 'Observações'])

# Função para salvar os dados
def salvar_dados(df):
    df.to_csv("disponibilidade.csv", index=False)

# Carregar os dados do CSV
st.session_state.df_disponibilidade = carregar_dados()

# Adicionar um botão para deletar uma linha específica
st.subheader("Tabela Atualizada de Disponibilidade")

# Função para deletar uma linha específica
def deletar_linha(index):
    st.session_state.df_disponibilidade = st.session_state.df_disponibilidade.drop(index).reset_index(drop=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success(f"Linha {index} deletada com sucesso!")

# Exibir a tabela com os botões de deletar
for i, row in st.session_state.df_disponibilidade.iterrows():
    cols = st.columns(len(row) + 1)  # +1 para o botão de deletar
    for j, value in enumerate(row):
        cols[j].write(value)
    # Adicionar botão de deletar
    if cols[len(row)].button("Deletar", key=f"delete_{i}"):
        deletar_linha(i)

# Botão para exportar os dados para CSV
st.subheader("Exportar Dados para CSV")
csv = st.session_state.df_disponibilidade.to_csv(index=False).encode('utf-8')
st.download_button("Baixar CSV", data=csv, file_name="disponibilidade.csv", mime='text/csv')

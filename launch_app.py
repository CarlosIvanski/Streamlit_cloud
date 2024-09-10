import streamlit as st
import pandas as pd
import os

# Função para carregar dados de um arquivo CSV
def carregar_dados():
    if os.path.exists("disponibilidade.csv"):
        return pd.read_csv("disponibilidade.csv")
    else:
        return pd.DataFrame(columns=['Professor', 'Unidades', 'Carro', 'Máquinas', 'Disponibilidade', 'Módulo', 'Observações'])

# Função para salvar dados em um arquivo CSV
def salvar_dados(df):
    df.to_csv("disponibilidade.csv", index=False)

# Carregar os dados salvos (se houver) ao iniciar a aplicação
st.session_state.df_disponibilidade = carregar_dados()

# Título do dashboard
st.title("Dashboard de Disponibilidade")

# Coletando o nome de quem preencheu o formulário
nome_preenchedor = st.text_input("Digite seu nome:")

# Garantir que um nome seja fornecido
if nome_preenchedor:
    st.write(f"Obrigado, {nome_preenchedor}, suas respostas foram registradas!")
else:
    st.warning("Por favor, preencha seu nome para continuar.")

# Nomes iniciais dos professores
nomes_iniciais = ['Pessoa A', 'Pessoa B', 'Pessoa C', 'Pessoa D']

# Lista de unidades
unidades = ['Satélite', 'Vicentina', 'Jardim', 'Online']

# Inicializa o session state se não estiver definido
if 'disponibilidade' not in st.session_state:
    st.session_state.disponibilidade = {nome: {} for nome in nomes_iniciais}

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
    </style>
    """,
    unsafe_allow_html=True
)

for i, nome_inicial in enumerate(nomes_iniciais):
    cols = st.columns(col_widths)

    with cols[0]:
        nome_professor = st.text_input(f"Nome do professor {i + 1}:", nome_inicial, key=f"nome_{i}")

    # Atualiza o nome do professor no session state
    if nome_professor != nome_inicial:
        st.session_state.disponibilidade[nome_professor] = st.session_state.disponibilidade.pop(nome_inicial, {})

    # Atualiza o dicionário com base no session state
    if nome_professor not in st.session_state.disponibilidade:
        st.session_state.disponibilidade[nome_professor] = {}

    with cols[1]:
        st.write("Unidades")
        # Adicionar checkboxes para cada unidade
        for unidade in unidades:
            st.session_state.disponibilidade[nome_professor][unidade] = st.checkbox(f"{unidade}", 
                value=st.session_state.disponibilidade[nome_professor].get(unidade, False), 
                key=f"{nome_professor}_{unidade}")

    with cols[2]:
        st.write("Carro")
        # Adicionar checkbox para o carro
        st.session_state.disponibilidade[nome_professor]['Carro'] = st.checkbox("Tem carro", 
            value=st.session_state.disponibilidade[nome_professor].get('Carro', False), 
            key=f"{nome_professor}_carro")

    with cols[3]:
        st.write("Máquina")
        # Adicionar checkboxes para selecionar múltiplas máquinas
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
        # Adicionar checkboxes para cada período
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
        # Adicionar checkboxes para as novas opções: Stage 1, VIP, CONVERSATION e MBA
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
        # Adicionar uma caixa de texto para observações
        observacoes = st.text_area("Observações", 
            value=st.session_state.disponibilidade[nome_professor].get('Observações', ''), 
            key=f"{nome_professor}_observacoes")
        st.session_state.disponibilidade[nome_professor]['Observações'] = observacoes

# Função para converter os dados para DataFrame
def converter_para_dataframe(dados):
    registros = []
    for professor, detalhes in dados.items():
        registro = {
            'Professor': professor,
            'Unidades': ', '.join([unidade for unidade, selecionado in detalhes.items() if unidade in unidades and selecionado]),
            'Carro': 'Sim' if detalhes.get('Carro', False) else 'Não',
            'Máquinas': ', '.join(detalhes['Máquina']),
            'Disponibilidade': ', '.join(detalhes['Disponibilidade']),
            'Módulo': ', '.join(detalhes['Modulo']),
            'Observações': detalhes.get('Observações', '')  # Incluindo observações
        }
        registros.append(registro)
    return pd.DataFrame(registros)

# Converter os dados coletados para um DataFrame
df_novo = converter_para_dataframe(st.session_state.disponibilidade)

# Botão para salvar os dados na tabela em tempo real
if st.button("Salvar dados"):
    st.session_state.df_disponibilidade = pd.concat([st.session_state.df_disponibilidade, df_novo]).drop_duplicates().reset_index(drop=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success("Dados salvos com sucesso!")

# Exibir a tabela atualizada no site
st.subheader("Tabela Atualizada de Disponibilidade")
st.dataframe(st.session_state.df_disponibilidade)

# Botão para exportar os dados para CSV
st.subheader("Exportar Dados para CSV")
csv = st.session_state.df_disponibilidade.to_csv(index=False).encode('utf-8')
st.download_button("Baixar CSV", data=csv, file_name="disponibilidade.csv", mime='text/csv')

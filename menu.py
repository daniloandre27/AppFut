import streamlit as st
import pandas as pd
import csv
from tela1 import show_tela1
from tela2 import show_tela2
from tela3 import show_tela3
from tela6 import show_tela6

# Função para verificar o login do usuário
def verificar_login(usuario, senha):
    # Lê o arquivo CSV com os usuários e senhas
    with open('usuarios.csv', mode='r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        for linha in leitor_csv:
            if usuario == linha[0] and senha == linha[1]:
                return True
    return False
# Função para verificar se o usuário é um administrador
def verificar_admin(usuario):
    with open('usuarios.csv', mode='r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        for linha in leitor_csv:
            if len(linha) >= 3 and usuario == linha[0] and linha[2] == '1':
                return True
    return False
# Função para verificar se o usuário já existe
def usuario_existe(usuario):
    with open('usuarios.csv', mode='r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        for linha in leitor_csv:
            if usuario == linha[0]:
                return True
    return False

def adicionar_usuario(usuario, senha, usuario_atual):
    # Verifica se o usuário e a senha foram preenchidos
    if usuario == "" or senha == "":
        st.error("Por favor, preencha o usuário e a senha.")
        return
    # Verifica se o usuário já existe
    if usuario_existe(usuario):
        st.error("O usuário já existe.")
        return
    # Verifica se o usuário atual é um administrador
    if not verificar_admin(usuario_atual):
        st.error("Apenas administradores podem adicionar novos usuários.")
        return
    # Adiciona um novo usuário e senha ao arquivo CSV
    with open('usuarios.csv', mode='a', newline='') as arquivo:
        escritor_csv = csv.writer(arquivo, delimiter=';')
        escritor_csv.writerow([usuario, senha])
        st.success("Usuário registrado com sucesso!")

def alterar_senha(usuario, senha_atual, nova_senha):
    if not verificar_login(usuario, senha_atual):
        st.error("Senha atual incorreta. Tente novamente.")
        return
    # Atualize a senha no arquivo CSV (ou onde você armazena as informações dos usuários)
    # Implemente a lógica para atualizar a senha aqui
    # Por exemplo, você pode procurar o usuário pelo nome e atualizar a senha
    # Certifique-se de armazenar a senha de forma segura (hash e sal)
    with open('usuarios.csv', mode='r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        linhas = list(leitor_csv)

    with open('usuarios.csv', mode='w', newline='') as arquivo:
        escritor_csv = csv.writer(arquivo, delimiter=';')
        for linha in linhas:
            if linha[0] == usuario:
                linha[1] = nova_senha
            escritor_csv.writerow(linha)

    st.success("Senha alterada com sucesso!")

# Configuração da página
st.set_page_config(page_title="Meu Dashboard", layout="centered")

# Função principal que controla o fluxo do aplicativo
def main():
    # Verifica se o usuário já está logado
    if 'logado' not in st.session_state or not st.session_state['logado']:
        # Centraliza a tela de login
        st.write("<h1 style='text-align: center;'>Bem-Vindo</h1>", unsafe_allow_html=True)
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        # Botão para fazer login
        if st.button("Login"):
            if verificar_login(usuario, senha):
                st.session_state['logado'] = True
                st.session_state['usuario_atual'] = usuario
            else:
                st.error("Usuário ou senha incorretos.")
    else:
        # Menu de navegação
        st.title("Monstro dos Greens")
        paginas = ['Lay Home', 'Lay Away', 'Lay 0 x 1', 'Resultados']
        escolha = st.radio('', paginas)
        if escolha == 'Lay Home':
            show_tela1()
        elif escolha == 'Lay Away':
            show_tela2()
        elif escolha == 'Lay 0 x 1':
            show_tela3()
        elif escolha == 'Resultados':
            show_tela6()     

        # Opções para o administrador
        # Dentro da função main()

        # Botão para mostrar/ocultar o subheader de cadastro de usuários
        mostrar_subheader_cadastro = st.button("Cadastro de usuários")

        # Verifica se o botão foi clicado e altera a visibilidade do subheader de cadastro de usuários
        if mostrar_subheader_cadastro:
            if 'exibir_subheader_cadastro' not in st.session_state:
                st.session_state['exibir_subheader_cadastro'] = True
            else:
                st.session_state['exibir_subheader_cadastro'] = not st.session_state['exibir_subheader_cadastro']

        # Verifica se o subheader de cadastro de usuários deve ser exibido
        if st.session_state.get('exibir_subheader_cadastro', False):
            # Subheader para a seção de cadastro de usuários
            st.subheader("Cadastro de Usuários")

            # Aqui você pode adicionar o código para o cadastro de usuários
            # Por exemplo:
            novo_usuario = st.text_input("Novo usuário", key="novo_usuario")
            nova_senha_cadastro = st.text_input("Nova senha", key="nova_senha_cadastro", type="password")
            # Botão para cadastrar o usuário
            if st.button("Cadastrar"):
                adicionar_usuario(novo_usuario, nova_senha_cadastro, st.session_state['usuario_atual'])

        else:
            pass

        
        # Opção para alterar a senha

        # Botão para mostrar/ocultar o subheader de alteração de senha
        mostrar_subheader = st.button("Alteração de senha")

        # Verifica se o botão foi clicado e altera a visibilidade do subheader
        if mostrar_subheader:
            if 'exibir_subheader' not in st.session_state:
                st.session_state['exibir_subheader'] = True
            else:
                st.session_state['exibir_subheader'] = not st.session_state['exibir_subheader']

        # Verifica se o subheader deve ser exibido
        if st.session_state.get('exibir_subheader', False):
            # Subheader para a seção de alteração de senha
            st.subheader("Alterar Senha")

            # Opção para alterar a senha
            senha_atual = st.text_input("Senha atual", key="senha_atual")
            nova_senha_input = st.text_input("Nova senha", key="nova_senha_input")
            # Botão para alterar a senha
            if st.button("Alterar"):
                if verificar_login(st.session_state['usuario_atual'], senha_atual):
                    nova_senha = nova_senha_input
                    alterar_senha(st.session_state['usuario_atual'], senha_atual, nova_senha)
                    # Atualize o valor da nova senha na sessão após a confirmação
                    st.session_state['nova_senha'] = nova_senha
                else:
                    st.error("Senha atual incorreta. Tente novamente.")
        else:
            # Se o subheader não deve ser exibido, exibe apenas o botão para mostrar/ocultar
            pass



        # Botão para sair da aplicação
        if st.button("Sair"):
            st.session_state['logado'] = False

if __name__ == "__main__":
    main()


st.write("<h1 style='text-align: center; font-size: 15px;'>Quer participar? Chama o Altair<br>Zap: (22)98802-4908</h1>", unsafe_allow_html=True)   

import streamlit as st
import pandas as pd
import csv
from tela1 import show_tela1
from tela2 import show_tela2
from tela3 import show_tela3

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
        paginas = ['Lay Home', 'Lay Away', 'Lay 0 x 1']
        escolha = st.radio('', paginas)
        if escolha == 'Lay Home':
            show_tela1()
        elif escolha == 'Lay Away':
            show_tela2()
        elif escolha == 'Lay 0 x 1':
            show_tela3()

        # Opções para o administrador
        if verificar_admin(st.session_state['usuario_atual']):
            if st.button("Registrar novo usuário"):
                usuario = st.text_input("Novo usuário")
                senha = st.text_input("Nova senha", type="password")
                if st.button("Confirmar registro"):
                    adicionar_usuario(usuario, senha, st.session_state['usuario_atual'])
        
        # Opção para alterar a senha
        if st.button("Alterar senha"):
            senha_atual = st.text_input("Senha atual", type="password")
            nova_senha = st.text_input("Nova senha", type="password")
            if st.button("Confirmar alteração"):
                pass# Adicione aqui o código para alterar a senha do usuário logado

        # Botão para sair da aplicação
        if st.button("Sair"):
            st.session_state['logado'] = False

if __name__ == "__main__":
    main()




# Importand as Bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

def drop_reset_index(df):
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.index += 1
    return df

# Importando as Funções
def ajustar_id_mercado(id_mercado, comprimento_decimal_desejado=9):
    id_mercado_str = str(id_mercado)
    partes = id_mercado_str.split('.')
    if len(partes) == 1:
        return id_mercado_str + '.' + '0' * comprimento_decimal_desejado
    parte_inteira, parte_decimal = partes
    zeros_para_adicionar = comprimento_decimal_desejado - len(parte_decimal)
    if zeros_para_adicionar > 0:
        parte_decimal += '0' * zeros_para_adicionar
    id_mercado_ajustado = parte_inteira + '.' + parte_decimal
    return id_mercado_ajustado

# Iniciando a Tela 2
def show_tela2():
    st.header("Lay Away")

    dia = st.date_input("Data de Análise", date.today())

    Jogos_do_Dia = pd.read_csv(f'https://raw.githubusercontent.com/futpythontrader/YouTube/main/Jogos_do_Dia/Betfair/Jogos_do_Dia_Betfair_Back_Lay_{dia}.csv')
    
    Jogos_do_Dia['VAR1'] = np.sqrt((Jogos_do_Dia['Odd_H_Back'] - Jogos_do_Dia['Odd_A_Back'])**2)
    Jogos_do_Dia['VAR2'] = np.degrees(np.arctan((Jogos_do_Dia['Odd_A_Back'] - Jogos_do_Dia['Odd_H_Back']) / 2))
    Jogos_do_Dia['VAR3'] = np.degrees(np.arctan((Jogos_do_Dia['Odd_D_Back'] - Jogos_do_Dia['Odd_A_Back']) / 2))
    
    flt = (Jogos_do_Dia.VAR1 >= 5) & (Jogos_do_Dia.VAR2 >= 60) & (Jogos_do_Dia.VAR3 <= -60)
    Entradas = Jogos_do_Dia[flt]
    Entradas = drop_reset_index(Entradas)
    
    st.dataframe(Entradas)

    st.subheader("Entradas")
    st.text('')

    for a,b,c,d,e,f in zip(Entradas.League,
                           Entradas.Time,
                           Entradas.Home,
                           Entradas.Away,
                           Entradas.Odd_A_Lay,
                           Entradas.IDMercado_Match_Odds):
        liga = a
        horario = b
        home = c
        away = d
        odd = e
        id_mercado = ajustar_id_mercado(f)

    
        st.markdown(f"<span style='color:green'><b>{liga}</b></span>", unsafe_allow_html=True)
        st.markdown(f"{home} x {away} - {horario} | Odd: {odd}")
        link = f'<div style="text-align:left"><a href="https://greenwin.bet/exchange/sport/1/market/{id_mercado}?affBetId=115748">{"Aposte Aqui"}</a></div>'
        st.markdown(link, unsafe_allow_html=True)
        st.write('______________________________________________')
        st.write('')

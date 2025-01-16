import pandas as pd
import streamlit as st
import joblib

# modelo = joblib.load('modelo.joblib') # para ler o modelo

# colunas de numeros
x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

# colunas de verdadeiro e falso
x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

# colunas de colunas de listas de escolhas
x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }

# juntar cada item dos x_listas com cada valor dentro de suas respectivas listas dando o valor 0 a cada uma para poder indicalos nas contas
dicionario = {}
for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0 

for item in x_numericos:
    if item == 'latitude' or item == 'longitude':
        valor = st.number_input(f'{item}', step=0.00001, value=0.0, format='%.5f') # para ter varias casas decimais e ser considerado float
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step=0.01, value=0.0) # padrao do format em float é duas casas decimais
    else:
        valor = st.number_input(f'{item}', step=1, value=0) # cria campos numerico para colocar o valor a ser calculado default
    x_numericos[item] = valor # altera o campo
    
for item in x_tf:
    valor = st.selectbox(f'{item}', ('Sim', 'Não')) # cria campos de selecao 'sim' ou 'nao' para colocar o valor a ser calculado
    if valor == 'Sim':
        x_tf[item] = 1
    else:
        x_tf[item] = 0
    
for item in x_listas:
    valor = st.selectbox(f'{item}', x_listas[item]) # cria campos de selecao de listas para colocar o valor a ser calculado
    dicionario[f'{item}_{valor}'] = 1
    
botao = st.button('Prever Valor do Imóvel') # cria botao para executar o calculo com o modelo

if botao: # verificar se o botao foi clicado
    dicionario.update(x_numericos) # junta os dicionarios
    dicionario.update(x_tf)
    valores_x = pd.DataFrame(dicionario, index=[0]) # index = [0] pq sem ele n teria indice ai daria erro
    
    dados = pd.read_csv('dados.csv')
    # deixar tabela com a mesma ordem e numero de colunas
    # retirar a coluna de unnamed e a coluna price
    colunas = list(dados.columns)[1:-1]
    valores_x = valores_x[colunas] # colunas reordenadas (lista de colunas existentes na ordem q voce quiser)
    
    modelo = joblib.load('modelo.joblib')
    preco = modelo.predict(valores_x)
    st.write(preco[0]) # só para n vir em tabela e apenas o valor



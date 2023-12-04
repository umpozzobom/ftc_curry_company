#Libraries/ pacotes


import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Empresa', layout='wide')
                   
                   
                   
                   
#--------------------------------------------------------------------
# FUNÇÕES                                                           #
#---------------------------------------------------------------------
def country_maps(df1):
        
        df1_aux = ( df1.loc[ : , ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                     .groupby(['City', 'Road_traffic_density'])
                     .median()
                     .reset_index() )
    
        map = folium.Map()
        for index, location_info in df1_aux.iterrows():
            folium.Marker([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']]).add_to(map)
        folium_static(map, width =1024, height = 600)
            
        

def order_by_week( df1 ):
    #criar a coluna da semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df1_aux1 = ( df1.loc[ : , ['ID' , 'week_of_year']]
                     .groupby('week_of_year')
                     .count()
                     .reset_index() )
    fig = px.line(df1_aux1, x ='week_of_year' , y = 'ID')
    
    return fig



def traffic_order_city(df1) :
        df1_aux = ( df1.loc[ : , ['ID', 'City','Road_traffic_density']]
                        .groupby(['City','Road_traffic_density'])
                        .count()
                        .reset_index() )
                
        fig = px.scatter(df1_aux, x ='City' , y ='Road_traffic_density' , color = 'City' , size = 'ID' )
                
        return fig
            

def traffic_order_share(df1):
    df1_aux2 = ( df1.loc[ : , ['Road_traffic_density', 'ID']]
                    .groupby('Road_traffic_density')
                    .count().reset_index() )
    df1_aux2.head()
    df1_aux2['perc_ID'] = 100 * ( df1_aux2['ID'] / df1_aux2['ID'].sum() )
    fig = px.pie(df1_aux2, names = 'Road_traffic_density', values = 'perc_ID' )
            
    return fig


def order_metric(df1):             
    cols = ['ID', 'Order_Date']
    #seleção de linhas
    df1_aux = df1.loc[ : , ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    #Desenhar o gráfico
    fig = px.bar(df1_aux, x = 'Order_Date', y = 'ID')
           
    return fig
        

def clean_code( df1 ):
    
    """esta funcao tem a responsabilidade de limpar o dataframe
    
        tipos de limpeza:

        1 - remoção dos dados NaN
        2 - mudança do tipo da coluna de dados
        3 - remocao das variaveis de texto
        4 - formatacao da data 
        5 - limpeza da coluna de tempo (remoção do texto da variavel numerica)

        Input: dataframe
        Output: dataframe
    """

    # 1 - Convertendo Object para inteiro = Delivery_person_Age / / Removendo os NaN

    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()
    df1['Delivery_person_Age'] = df1["Delivery_person_Age"].astype(int)

    # 1.1 - retirando NAN

    linhas_selecionadas = df1['Weatherconditions'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()

    # 1.1 - retirando NAN

    linhas_selecionadas = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()

    linhas_selecionadas = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()

    linhas_selecionadas = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()


    # 2- Convertendo order_date usaod pd.to_datetime

    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')


    # 3 - convertendo Delivery_person_Ratings  - objetc par float

    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 4 - Convertendo deliveris_ Objetc = int

    linhas_selecionadas_mult = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas_mult, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    #Retirando os espaços entre strings usando a função str.strip()

    df1.loc[:, 'Delivery_person_ID'] = df1.loc[: , 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'ID'] = df1.loc[: , 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[: , 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[: , 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[: , 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[: , 'City'].str.strip()

    #retirando o min

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split( '(min)' ) [1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )
    
    return df1

#---------------------------INICIO DA ESTRUTURA LÓGICA DO CÓDIGO

#IMPORT DATASET

df1 = pd.read_csv('train.csv')

#----------------------------------------------#
# LIMPANDO OS DADOS                            #
#----------------------------------------------#
df1 = clean_code(df1)

#---------------------------------------------
# lAYOYT DO STREAMLIT
#--------------------------------------------


st.header('Marketplace - Visão Cliente')

#image_path = 'log.png'
image = Image.open('log.png')
st.sidebar.image(image, width=120)


st.sidebar.markdown('### Curry Company')
st.sidebar.markdown('## Fastest delivery in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown(' ## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime(2022,4,13),
    min_value=pd.datetime(2022,2,11),
    max_value=pd.datetime(2022,4,6),
    format='DD-MM-YYYY')
#st.header(date_slider)
st.sidebar.markdown("""___""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low','Medium','High','Jam'],
    default = ['Low','Medium','High', 'Jam'])

st.sidebar.markdown("""___""")
st.sidebar.markdown(' ### Powered by UMP')

 
#'DD-MM-YYYY'
#Filtro de data

linhas_selecionadas = df1['Order_Date']< date_slider
df1 = df1.loc[linhas_selecionadas, : ]
#st.dataframe(df1.head() )

#Filtro de transito
#isin = filtra as info pelo que o usuario passa

linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]


#Criação de abas com informações

tab1,tab2,tab3 = st.tabs(['Visão Gerencial', 'Visão Tática','Visão Geográfica'])

#tudo que estiver dentro do with vai aparecer na primeira aba
#container (divisões )

with tab1:
    with st.container(): 
        fig = order_metric(df1)
        st.markdown('# Orders by Day')
        st.plotly_chart(fig, use_container_width = True) 
              
        
    with st.container():
        col1,col2 = st.columns (2)

        with col1:
            fig = traffic_order_share( df1 )
            st.header('Traffic Order Share')
            st.plotly_chart(fig, use_container_width = True)

        with col2:
            fig = traffic_order_city( df1 )
            st.header('Traffic Order City')
            st.plotly_chart(fig, use_container_width = True)
                  
with tab2:
        with st.container():
            st.markdown('# Order by Week')
            fig = order_by_week(df1)
            st.plotly_chart(fig, use_container_width = True)  

with tab3:
        st.markdown('# \Country Maps')
        country_maps(df1)

    
 

    


















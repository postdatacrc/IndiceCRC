import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import glob
import os
from urllib.request import urlopen
import json
from streamlit_folium import folium_static
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import geopandas as gpd
import folium
from functools import reduce
from folium.plugins import FloatImage
import urllib
import unidecode,datetime
import requests



LogoComision="data:image/png;base64,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"
LogoComision2="https://www.postdata.gov.co/sites/all/themes/nuboot_radix/logo-crc-blanco.png"

st.set_page_config(
    page_title="ICE", page_icon=LogoComision,layout="wide",initial_sidebar_state="expanded")
    
Estilo_css="""<style type="text/css">
    @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap'); 

    html, body, [class*="css"] ,[class*="st-ae"]{
        font-family: 'Poppins', serif; 
    }  
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 300px;background-color:#2A3144;color=white;}
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 300px;
        top:100px;
        background-color:#2A3144;
        color=white;
        margin-left: -300px;}
    h1{ background: #EEF3F4;
        text-align: center;
        padding: 15px;
        font-family: Poppins;
        font-size:1.60rem;
        color: black;
        width:100%;
        z-index:9999999;
        left:0;
    }
    h2{
        background: #fffdf7;
        text-align: center;
        padding: 10px;
        color: #FE9D82;
        font-weight: bold;
    }    
    h6{
        background: #fffdf7;
        color: #7a44f2;
        font-weight: bold;
    }        
    .css-1kyxreq {
        display: unset;
    }
    .css-1v0mbdj {
        display: unset;
    }
    .e16nr0p31 {display:none}
    .css-y3whyl, .css-xqnn38 {background-color:#ccc}
    .e8zbici0 {display:none}
    .e8zbici2 {display:none}
    .e19lei0e1 {display:none}
    .css-1uvyptr:hover,.css-1uvyptr {background: #ccc}
    .e1tzin5v2 {
        display:flex;
        align-items:center;
    }
    .css-52bwht{
        gap:0.01rem;
    }
    .block-container {
        padding-top:0;
        } 
    .main > div {
        padding-left:30px;
        padding-right:30px;
    }            
    .titulo {
      background: #fffdf7;
      display: flex;
      color: #7a44f2;
      font-size:25px;
      padding:10px;
      text-align:center;
    }
    .titulo:before,
    .titulo:after {
      content: '';
      margin: auto 1em;
      border-bottom: solid 3px;
      flex: 1;
    }   
    .stButton{
        text-align:center;
    }
    .edgvbvh9:hover {
      color:rgb(255,255,255);
      border-color:rgb(255,75,75);
    }
    .edgvbvh9 {
      font-weight: 600;
      background-color: rgb(215,235,252);
      border: 0px solid rgba(0, 0, 0, 1); 
      color:black;
      padding: 0.6rem 0.6rem;
      font-size: 16px;
    }
    .imagen-flotar{float:left;}      
    .IconoTitulo img {
        margin-right:10px;
    }
    .IconoTitulo{
        text-align:center;
    }
    .IconoTitulo h4, .IconoTitulo img {
        display:inline-block;
        vertical-align:middle;
    }    
    .css-17m3m1o{text-align:left}
    .st-b4 {display: inline-flex}
    .stRadio{text-align:center}
    ul {
        list-style-type: square;
        text-align:left;
    }      
    mark.title {
        color:#7a44f2;
        background:none;
    }
    .e1tzin5v3{
        text-align:center}
        
    .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        margin-left: auto;
        margin-right: auto;        
        border-collapse: collapse;
    }    
    .styled-table thead tr {
        background-color: #009879;
        color: #ffffff;
        text-align: left;
    }    
    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
        border:0;
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }

    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #FE9D82;
    }    
    .styled-table tbody tr:first-of-type {
        border-top: 2px solid #FE9D82;
    }        
    .styled-table tbody tr.active-row {
        font-weight: bold;
        color: #009879;
    }    
    hr{
        margin:0;
        border-bottom:none;
    }
    .css-ocqkz7{
        gap:20px;
    }
    .css-keje6w {
        display: unset;
    }
    </style>"""
Barra_superior="""
<div class="barra-superior">
    <div class="imagen-flotar" style="height: 0px; left: 10px; padding:15px">
        <a class="imagen-flotar" style="float:left;" href="https://www.crcom.gov.co" title="CRC">
            <img src="https://www.postdata.gov.co/sites/all/themes/nuboot_radix/logo-crc-blanco.png" alt="CRC" style="height:40px">
        </a>
    </div>  
</div>"""

def convert_df(df):
     return df.to_csv().encode('utf-8')
def standardize_date(date):
    date=date.replace(' ','-').lower()
    month,year=date.split('-')
    if len(year)==2:
        year='20'+year
    else:
        pass
    date=month+'-'+year
    return date
## Definiciones Fijos

def DownloadFIJO(x):
    min_down=25;max_down=500;weight_down=0.40
    if x>max_down:
        y=100*weight_down
    elif x<min_down:
        y=0
    else:    
        y= y=(x/max_down)*100*weight_down
    return y
def UploadFIJO(x):
    min_up=5;max_up=500;weight_up=0.25
    if x>max_up:
        y=100*weight_up
    elif x<min_up:
        y=0
    else:    
        y= y=(x/max_up)*100*weight_up
    return y
def LatencyFIJO(x):
    min_Lat=25;max_Lat=100;weight_Lat=0.25
    if x>=max_Lat:
        y=0
    elif x<=min_Lat:
        y=100*weight_Lat
    else:
        y=100*(max_Lat-x)*weight_Lat/(max_Lat-min_Lat)
    return y
def JitterFIJO(x):
    min_Jit=0;max_Jit=50;weight_Jit=0.10
    if x>=max_Jit:
        y=0
    elif x<=min_Jit:
        y=100*weight_Jit
    else:
        y=100*(max_Jit-x)*weight_Jit/(max_Jit-min_Jit)
    return y

def lineatiempoMuni(df,yvalue):
    fig = make_subplots(rows=1, cols=1)
    for proveedor in df['provider'].unique().tolist():
        df2=df[df['provider']==proveedor]
        fig.add_trace(go.Scatter(x=df2['periodo'],y=df2[yvalue],name=proveedor,marker=dict(size=7,color=Colores_proveedores[proveedor]),line=dict(color=Colores_proveedores[proveedor]),
        hovertemplate =
            '<br><b>Operador</b>:<br><extra></extra>'+proveedor+
            '<br><b>Periodo</b>: %{x}<br>'+                         
            ParametroFijo+'-'+dict_parametros_unidad[ParametroFijo]+': %{y:.3f}<br>'))
    fig.update_yaxes(tickfont=dict(family='Poppins', color='black', size=16),titlefont_size=16, title_text=ParametroFijo+' '+dict_parametros_unidad[ParametroFijo], row=1, col=1)
    fig.update_xaxes(tickangle=0, tickfont=dict(family='Poppins', color='black', size=14),title_text='Fecha (mes/año)',row=1, col=1
    ,zeroline=True,linecolor = 'rgba(192, 192, 192, 0.8)',zerolinewidth=2)
    fig.update_layout(height=550,legend_title=None)
    fig.update_layout(font_color="Black",font_family="Poppins",title_font_color="Black",titlefont_size=16,
    title={
    'text':'Evolución '+ParametroFijo+' por operador',
    'y':0.96,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})        
    fig.update_layout(legend=dict(orientation="h",xanchor='center',y=1.05,x=0.5,font_size=11),showlegend=True)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(192, 192, 192, 0.8)')
    fig.update_layout(yaxis_tickformat ='d')
    fig.update_layout(xaxis_tickformat ='%m/%y')
    fig.add_annotation(
    showarrow=False,
    text='',
    font=dict(size=11), xref='x domain',x=0.5,yref='y domain',y=-0.2)    
    return fig

def lineatiempoMuniMovil(df,yvalue):
    fig = make_subplots(rows=1, cols=1)
    for proveedor in df['provider'].unique().tolist():
        df2=df[df['provider']==proveedor]
        fig.add_trace(go.Scatter(x=df2['periodo'],y=df2[yvalue],name=proveedor,marker=dict(color=Colores_proveedores[proveedor]),line=dict(color=Colores_proveedores[proveedor]),
        hovertemplate =
            '<br><b>Operador</b>:<br><extra></extra>'+proveedor+
            '<br><b>Periodo</b>: %{x}<br>'+                         
            ParametroMovil+'-'+dict_parametros_unidad[ParametroMovil]+': %{y:.3f}<br>'))
    fig.update_yaxes(tickfont=dict(family='Poppins', color='black', size=16),titlefont_size=16, title_text=ParametroMovil+' '+dict_parametros_unidad[ParametroMovil], row=1, col=1)
    fig.update_xaxes(tickangle=0, tickfont=dict(family='Poppins', color='black', size=14),title_text='Fecha (mes/año)',row=1, col=1
    ,zeroline=True,linecolor = 'rgba(192, 192, 192, 0.8)',zerolinewidth=2)
    fig.update_layout(height=550,legend_title=None)
    fig.update_layout(font_color="Black",font_family="Poppins",title_font_color="Black",titlefont_size=16,
    title={
    'text':'Evolución '+ParametroMovil+' por operador',
    'y':0.96,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})        
    fig.update_layout(legend=dict(orientation="h",xanchor='center',y=1.05,x=0.5,font_size=11),showlegend=True)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(192, 192, 192, 0.8)')
    fig.update_layout(yaxis_tickformat ='d')
    fig.update_layout(xaxis_tickformat ='%m/%y')
    fig.add_annotation(
    showarrow=False,
    text='',
    font=dict(size=11), xref='x domain',x=0.5,yref='y domain',y=-0.2)    
    return fig

def cambiopos(x):
    if x<0:
        y="""<span style='color:red'>"""+str(x)+"""</span>"""
    elif x==0:
        y='-'
    else:   
        y="""<span style='color:green'>+"""+str(x)+"""</span>"""
    return y           

#@st.cache(ttl=24*3600,allow_output_mutation=True)
def ReadDataFijoMunicipios():
    FijosCapDep=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/2023/Fijo/fixed_CapDep.csv',delimiter=';')    
    FijosCapDep.rename(columns={'Provider':'provider','Location':'municipio','Minimum Latency':'latency','Multi-Server Jitter':'jitter','Download Speed Mbps':'download_speed','Upload Speed Mbps':'upload_speed'},inplace=True)
    FijosCapDep['municipio']=FijosCapDep['municipio'].str.upper()
    FijosCapDep['Aggregate Date']=FijosCapDep['Aggregate Date'].apply(standardize_date)
    FeAntigFijoTCP= sorted(FijosCapDep['Aggregate Date'].unique(),key=lambda x: datetime.datetime.strptime(x, '%b-%Y')) #Generar las fechas que tenían los datos
    FeCorreFijoTCP=pd.date_range('2022-01-01','2023-06-01', 
                  freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
    dictionFijoTCP=dict(zip(FeAntigFijoTCP, FeCorreFijoTCP))
    FijosCapDep['Aggregate Date'].replace(dictionFijoTCP, inplace=True) #Reemplazar fechas antiguas por nuevas
    FijosCapDep['Aggregate Date'] =pd.to_datetime(FijosCapDep['Aggregate Date']).dt.floor('d') 
    FijosCapDep['mes']=pd.DatetimeIndex(FijosCapDep['Aggregate Date']).month
    FijosCapDep['año']=pd.DatetimeIndex(FijosCapDep['Aggregate Date']).year
    FijosCapDep['periodo']=FijosCapDep['año'].astype('str')+'-'+FijosCapDep['mes'].astype('str').str.zfill(2)
    FijosCapDep['municipio']=FijosCapDep['municipio'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
    FijosCapDep=FijosCapDep[(FijosCapDep['periodo']>'2021-12')&(FijosCapDep['periodo']<'2023-07')&(FijosCapDep['Test Count']>=30)]    
    return FijosCapDep

BaseFijosMunicipios=ReadDataFijoMunicipios()
BaseFijosMunicipios['latency']=BaseFijosMunicipios['latency'].astype('str').str.replace(',','.').astype('float')
BaseFijosMunicipios['jitter']=BaseFijosMunicipios['jitter'].astype('str').str.replace(',','.').astype('float')
BaseFijosMunicipios['Indice_Descarga']=BaseFijosMunicipios['download_speed'].apply(DownloadFIJO)
BaseFijosMunicipios['Indice_Carga']=BaseFijosMunicipios['upload_speed'].apply(UploadFIJO)
BaseFijosMunicipios['Indice_Latencia']=BaseFijosMunicipios['latency'].apply(LatencyFIJO)
BaseFijosMunicipios['Indice_Jitter']=BaseFijosMunicipios['jitter'].apply(JitterFIJO)
BaseFijosMunicipios['Indice_CRC']=BaseFijosMunicipios['Indice_Descarga']+BaseFijosMunicipios['Indice_Carga']+BaseFijosMunicipios['Indice_Latencia']+BaseFijosMunicipios['Indice_Jitter']
BaseFijosMunicipios[['download_speed','upload_speed','latency','jitter','Indice_CRC']]=BaseFijosMunicipios[['download_speed','upload_speed','latency','jitter','Indice_CRC']]
BaseFijosMunicipios['municipio']=BaseFijosMunicipios['municipio'].apply(lambda x:unidecode.unidecode(x).upper())

#@st.cache(allow_output_mutation=True)
def data_MuniColombia():    
    with urllib.request.urlopen("https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/co_2018_MGN_MPIO_POLITICO.geojson") as url:
        Muni = json.loads(url.read().decode())
    return Muni
Colombian_MUNI=data_MuniColombia()  
Proveedores_fijo=['All Providers Combined','Claro','Tigo','Movistar','ETB','DIRECTV']    
Proveedores_moviles=['All Providers Combined','Movistar','Claro','Tigo','Avantel','WOM']
Colores_proveedores={'All Providers Combined':'black','Claro':'rgb(226,36,46)','Tigo':'rgb(57,107,80)','Movistar':'rgb(102,206,0)','ETB':'rgb(11,52,104)',
                          'DIRECTV':'rgb(0,147,209)','Avantel':'rgb(255,0,156)','WOM':'rgb(69,7,82)'}
    
st.markdown(Estilo_css,unsafe_allow_html=True)

hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

st.markdown("<center><h2>Índice de calidad de la experiencia - ICE</h2></center>",unsafe_allow_html=True)
select_seccion = st.selectbox('Escoja la sección del reporte',['Definición','Resultados'])   


reemplazo_Muni={'SANTA FE DE ANTIOQUIA':'SANTAFE DE ANTIOQUIA','BOGOTA, D.C.':'BOGOTA','CUASPUD CARLOSAMA':'CUASPUD',
                'SOTARA - PAISPAMBA':'SOTARA','EL CANTON DEL SAN PABLO':'CANTON DEL SAN PABLO'}

                
capitales_departamento={'AMAZONAS':'LETICIA','ANTIOQUIA':'MEDELLIN','ARAUCA':'ARAUCA','ATLANTICO':'BARRANQUILLA','BOGOTA, D.C.':'BOGOTA',
                        'BOLIVAR':'CARTAGENA','BOYACA':'TUNJA','CALDAS':'MANIZALES','CAQUETA':'FLORENCIA','CASANARE':'YOPAL','CAUCA':'POPAYAN',
                        'CESAR':'VALLEDUPAR','CHOCO':'QUIBDO','CORDOBA':'MONTERIA','GUAINIA':'INIRIDA','GUAVIARE':'SAN JOSE DEL GUAVIARE',
                        'HUILA':'NEIVA','LA GUAJIRA':'RIOHACHA','MAGDALENA':'SANTA MARTA','META':'VILLAVICENCIO','NARIÑO':'PASTO',
                        'NORTE DE SANTANDER':'CUCUTA','PUTUMAYO':'MOCOA','QUINDIO':'RISARALDA','SAN ANDRES':'SAN ANDRES','SANTANDER':'BUCARAMANGA',
                        'SUCRE':'SINCELEJO','TOLIMA':'IBAGUE','VALLE DEL CAUCA':'CALI','VAUPES':'MITU','VICHADA':'PUERTO CARRENO'}                
capitales_departamento_inv={v: k for k, v in capitales_departamento.items()}
def capitales_Dep(x):
    y=capitales_departamento_inv[x]
    return y    
List_capitales=list(capitales_departamento.values())

Intro_Sec1=r"""<p style='text-align:justify'> 
El índice de calidad de la experiencia -ICE- busca dar a conocer el comportamiento de las capitales de departamento del país que cuentan con las mejores 
condiciones en términos de calidad que experimenta el usuario en el servicio de Internet prestado a través de redes de acceso móvil y fijo.
</p>
"""

Intro_Sec2=r"""<p style='text-align:justify'> 
Teniendo en cuenta lo estipulado en la regulación vigente, la CRC ha estado utilizando la metodología de Crowdsourcing para capturar información de indicadores
de calidad directamente de los equipos terminales de los usuarios. En ese sentido, y con la finalidad de entregar a los usuarios información técnica de una 
manera más sencilla, nace la idea de consolidar los parámetros para la construcción de un índice, en aras de facilitar la lectura y entendimiento de la 
calidad de los servicios que prestan los operados a los usuarios, para este caso, se definirá un índice para la calidad del servicio de Internet móvil y un 
índice para Internet fijo.
</p>
"""

Intro_Sec3=r"""<p style='text-align:justify'>  
En ese contexto, el reporte técnico ETSI TR 103 559 analiza la construcción y la metodología de una evaluación comparativa en una medición nacional, 
considerando aspectos como el área y la población a cubrir, la recopilación y agregación de las mediciones, y la ponderación de los diversos aspectos 
considerados, con el principal propósito de identificar las mejores prácticas que se deben tener en cuenta a la hora de realizar una evaluación comparativa, 
de tal manera que esta refleje la verdadera experiencia del usuario.
</p>
"""

Intro_Sec4=r"""<p style='text-align:justify'> 
Considerando las recomendaciones y buenas prácticas contenidas en el mencionado reporte técnico de la ETSI, la CRC diseñó el índice de calidad de la 
experiencia con el propósito de reducir la asimetría de la información hacia el usuario, de tal manera que pueda tomar decisiones bien informado, respecto de 
la contratación de los servicios de Internet móvil e Internet fijo. 
</p>
"""

Intro_Sec5=r""" <p style='text-align:justify'>
Adicionalmente, el ICE busca también incentivar la mejora continua de la calidad de los servicios de Internet fijo y móvil que se prestan a los usuarios, 
considerando para tal efecto los cinco (5) siguientes parámetros:
<center>
<ul>
<li>Velocidad de descarga
<li>Velocidad de carga
<li>Latencia
<li>Jitter
<li>Tasa de pérdida de paquetes
</ul>
</center>
</p>
"""

Intro_Sec6=r"""<p style='text-align:justify'>
Este índice arroja un valor máximo de cien (100) puntos y se calcula de acuerdo con la evaluación de los parámetros antes descritos, definiendo unos valores 
que permiten la normalización y con la aplicación de unos ponderadores.
</p>
"""

Vel_descarga_Info=r"""<p style='text-align:justify'>
Se entiende como la rapidez con la que se pueden descargar contenidos (documentos, videos, imágenes, audio, etc.), normalmente desde una página Web. A mayor 
velocidad obtenida en la medición, mayor rapidez en la descarga, y, por lo tanto, mejor experiencia del usuario. La medición de este parámetro se normaliza a 
un valor de 0 a 100, utilizando para ello un valor mínimo de velocidad de 5 Mbps y un máximo de 25 Mbps en Internet móvil y de 25 Mbps y 500 Mbps en Internet 
fijo.
</p>
"""
Vel_carga_Info=r"""<p style='text-align:justify'>
Se entiende como qué tan rápido se envían los datos en dirección desde un dispositivo hacia Internet. Es decir, es la rapidez con la que se pueden subir 
contenidos (cargar archivos adjuntos al correo, compartir pantalla en una video conferencia, subir imágenes a redes sociales, etc.) a Internet. A mayor 
velocidad obtenida en la medición, mayor rapidez en la carga, por lo tanto, mejor es la experiencia del usuario. La medición de este parámetro se normaliza a 
un valor de 0 a 100, utilizando para ello un valor mínimo de velocidad de 2,6 Mbps y un máximo de 12,5 Mbps en Internet móvil y de 5 Mbps y 500 Mbps en Internet
fijo.
</p>
"""
Lat_Info=r"""<p style='text-align:justify'>
Sirve para medir qué tan rápido viajan los datos desde un punto de origen al destino. Por ejemplo, en los videojuegos en línea, cuando hay alta latencia se 
tarda en refrescar la pantalla con respecto a la velocidad de lo que ocurre en el juego. Por tal motivo, a latencias más bajas, la experiencia del usuario es
mejor. La latencia se mide en milisegundos (ms). La medición de este parámetro se normaliza a un valor de 0 a 100, utilizando para ello un valor mínimo de 
latencia de 25 ms y un máximo de 100 ms, tanto para Internet móvil como para el fijo.
</p>
"""
Jitter_Info=r"""<p style='text-align:justify'>
Es una medida en el tiempo de la fluctuación en la entrega y recepción de paquetes. Este comportamiento puede ser percibido cuando en las llamadas (de audio o 
video) se presentan interrupciones. Esto se traduce en que a valores bajos (en milisegundos) de este parámetro, mejor es la experiencia del usuario. La medición
de este parámetro se normaliza a un valor de 0 a 100, utilizando para ello un valor mínimo de jitter de 0 ms y un máximo de 50 ms, tanto para Internet móvil 
como para el fijo.
</p>
"""
TPerida_paquetes_Info=r"""<p style='text-align:justify'>
Los paquetes pueden verse como contenedores de información (audio, video, archivos, etc.), los cuales se envían y reciben en toda interacción en Internet. En 
este contexto, la pérdida de paquetes ocurre cuando la cantidad de paquetes recibidos no es igual a la cantidad de paquetes transmitidos. En este caso, pueden 
evidenciarse interrupciones en las llamadas (audio o video), en la reproducción de contenidos multimedia, etc. A menor tasa de pérdida de paquetes, mejor es la
experiencia del usuario. La medición de este parámetro se normaliza a un valor de 0 a 100, utilizando para ello un valor mínimo de tasa de pérdida de paquetes
de 0 % y un máximo de 100 % para Internet móvil. La información de este parámetro no se encuentra disponible para Internet fijo.
</p>
"""

dict_parametros={'Velocidad de descarga':'download_speed','Velocidad de carga':'upload_speed','Latencia':'latency','Jitter':'jitter','ICE':'Indice_CRC'}
dict_parametros_unidad={'Velocidad de descarga':'(mpbs)','Velocidad de carga':'(mbps)','Latencia':'(ms)','Jitter':'(ms)','ICE':'(%)'}

if select_seccion=='Definición':
    st.markdown("")
    st.title("Definición del ICE")       
    st.markdown(r"""<hr>""",unsafe_allow_html=True)
    st.markdown("")
    st.markdown(Intro_Sec1,unsafe_allow_html=True)
    st.markdown(Intro_Sec2,unsafe_allow_html=True)
    st.markdown(Intro_Sec3,unsafe_allow_html=True)
    st.markdown(Intro_Sec4,unsafe_allow_html=True)
    st.markdown(Intro_Sec5,unsafe_allow_html=True)
    st.markdown(Intro_Sec6,unsafe_allow_html=True)
    st.markdown("A continuación se presenta una definición detallada de cada uno de los parámetros usados para el cálculo del índice",unsafe_allow_html=True)
    
    col1,col2=st.columns(2)
    with col1:
        with st.expander('Velocidad de descarga'):
            st.markdown(Vel_descarga_Info,unsafe_allow_html=True)
    with col2:
        with st.expander('Velocidad de carga'):
            st.markdown(Vel_carga_Info,unsafe_allow_html=True)
    col1,col2=st.columns(2)        
    with col1:
        with st.expander('Latencia'):
            st.markdown(Lat_Info,unsafe_allow_html=True)       
    with col2:
        with st.expander('Jitter'):
            st.markdown(Jitter_Info,unsafe_allow_html=True)
    col1,col2=st.columns(2) 
    with col1:
        with st.expander('Tasa pérdida paquetes'):
            st.markdown(TPerida_paquetes_Info,unsafe_allow_html=True)

    st.markdown(r"""<p style='text-align:justify'>El cálculo del ICE está conformado por la sumatoria de la relación del valor de la medición y el valor de normalización y 
    el producto con el ponderador de cada uno de los indicadores. En las tablas 1 y 2 se pueden observar estos ponderadores, así como los valores de 
    normalización indicados previamente.</p>""",unsafe_allow_html=True)    
    
    col1,col2=st.columns(2)
    with col1:
        st.markdown("<p style='font-size:11px;text-align:center'><b>Tabla 1:</b> Valores de referencia para el cálculo del ICE para el servicio de Internet móvil</p>",unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/ICE%20Movil2.png")
    with col2:
        st.markdown("<p style='font-size:11px;text-align:center'><b>Tabla 2:</b> Valores de referencia para el cálculo del ICE para el servicio de Internet fijo</p>",unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/ICE%20Fijo2.png")
        
if select_seccion=='Resultados':
    st.markdown("")
    st.title("Resultados ICE") 
    st.markdown(r"""<hr style='border:1px solid #FE9D82'>""",unsafe_allow_html=True)
                    
    
    st.markdown("<h3> Comparación posiciones de ciudades por periodo</h3>",unsafe_allow_html=True) 
    st.markdown(r"""<hr>""",unsafe_allow_html=True) 

    BaseFijosMunicipios=BaseFijosMunicipios[(BaseFijosMunicipios['provider']=='All Providers Combined')]
    BaseFijosMunicipios['Indice_CRC']=round(BaseFijosMunicipios['Indice_CRC'],2)
    BaseFijosMunicipios['municipio']=BaseFijosMunicipios['municipio'].replace({'SAN JOSE DEL GUAVIARE':'SJ. GUAVIARE'})
    BaseFijosMunicipios=BaseFijosMunicipios.sort_values(by=['periodo'],ascending=False)
    Ciudades_capitales=sorted(BaseFijosMunicipios['municipio'].unique().tolist())    
    
    #
           
    periodos_posiciones=BaseFijosMunicipios['periodo'].unique().tolist()        
    
    col1b,col2b,col3b=st.columns(3)
    with col2b:
        select_periodoComp1=st.selectbox('Escoja un periodo',periodos_posiciones,0)
        if periodos_posiciones.index(select_periodoComp1)<len(periodos_posiciones)-1:
            second_period=periodos_posiciones[periodos_posiciones.index(select_periodoComp1)+1]
        else:
            second_period=select_periodoComp1
   
    st.markdown("""<p style='font-size:12px'><b>Nota</b>: El cambio en la posición se compara respecto al periodo inmediatamente anterior</p>""",unsafe_allow_html=True)
        
    prueba1=BaseFijosMunicipios[(BaseFijosMunicipios['periodo']==select_periodoComp1)&(BaseFijosMunicipios['municipio']!='COLOMBIA')].sort_values(by=['Indice_CRC'],ascending=False).reset_index()
    prueba1['posición']=prueba1.index+1
    prueba1=prueba1[['periodo','municipio','Indice_CRC','posición','download_speed','upload_speed','latency','jitter']]
    prueba1[['download_speed','upload_speed','latency','jitter']]=round(prueba1[['download_speed','upload_speed','latency','jitter']],2)
    replace_colname={'download_speed':'Vel descarga '+select_periodoComp1,'upload_speed':'Vel carga '+select_periodoComp1,'latency':'Latencia '+select_periodoComp1,'jitter':'Jitter '+select_periodoComp1}
    prueba1=prueba1.rename(columns=replace_colname)
    
    prueba2=BaseFijosMunicipios[(BaseFijosMunicipios['periodo']==second_period)&(BaseFijosMunicipios['municipio']!='COLOMBIA')].sort_values(by=['Indice_CRC'],ascending=False).reset_index()
    prueba2['posición']=prueba2.index+1
    prueba2=prueba2[['periodo','municipio','Indice_CRC','posición']]

    Compara_Ciudad=prueba1.merge(prueba2, left_on=['municipio'],right_on=['municipio'])
    Compara_Ciudad['Cambio_indice']=round((Compara_Ciudad['Indice_CRC_x']-Compara_Ciudad['Indice_CRC_y']),2)   
    Compara_Ciudad['Cambio posición']=Compara_Ciudad['posición_y']-Compara_Ciudad['posición_x']
    Compara_Ciudad['Cambio posición']=Compara_Ciudad['Cambio posición'].apply(cambiopos)
    Compara_Ciudad=Compara_Ciudad.sort_values(by=['posición_x'],ascending=True)
    
    
    BaseFijosMunicipios2=BaseFijosMunicipios.copy()[['periodo','municipio','Indice_CRC']]
            
    pruebaHTML=Compara_Ciudad[['Cambio posición','posición_x','municipio','Indice_CRC_x']]
    pruebaHTML['barra']=""
    pruebaHTML=pruebaHTML.values.tolist()
    Title="""<table class='styled-table'>
      <tr>
        <th></th>
        <th>Posición</th>
        <th style='width:200px'>Municipio</th>
        <th colspan="2" style='text-align:left'>ICE</th>
      </tr> 
      """
    def htmlcode(x,a,b):
        html=""
        maximo_Indice=max([i[3] for i in x])
        for i in x[a:b]:
            width_linea=round(i[3]*100/maximo_Indice,2)
            html+="""<tr><td>"""+i[0]+"""</td><td>"""+str(i[1])+"""</td><td style='text-align:left'>"""+i[2]+"""</td><td>"""+str(i[3])+"""</td>"""
            html+="""<td style="width:300px"><hr style='background:linear-gradient(to right,#4949E7 """+str(width_linea)+"""%, #B6B6F5 """+str(width_linea)+"""%, #B6B6F5 100%);height:15px;'></td></tr>"""
        html=html+"""</table>"""    
        return html
        
    st.markdown("<center><h2 style='color:#4949E7'>Internet fijo</h2></center>",unsafe_allow_html=True)
    st.markdown(Title+htmlcode(pruebaHTML,0,len(pruebaHTML)),unsafe_allow_html=True)  
        
    ################################################################################################################     

    
    st.markdown("<h3> Evolución temporal capitales departamentales</h3>",unsafe_allow_html=True) 
    st.markdown(r"""<hr>""",unsafe_allow_html=True)
    param_Evo=st.radio('Escoja el parámetro a visualizar',['ICE','Velocidad de descarga','Velocidad de carga','Latencia','Jitter'],horizontal=True)
    Select_ciudCapital=st.multiselect('Escoja las ciudades capitales a comparar',Ciudades_capitales,['COLOMBIA']) 

    dfFijoCiudCapi=BaseFijosMunicipios[BaseFijosMunicipios['municipio'].isin(Select_ciudCapital)]
    dfFijoCiudCapi=dfFijoCiudCapi[['periodo','municipio',dict_parametros[param_Evo]]]
    fig_ciudadesEv=make_subplots(rows=1,cols=1)
    for ciudad in Select_ciudCapital:
        dfFijoCiudCapi2=dfFijoCiudCapi[dfFijoCiudCapi['municipio']==ciudad]
        fig_ciudadesEv.add_trace(go.Scatter(x=dfFijoCiudCapi2['periodo'],y=dfFijoCiudCapi2[dict_parametros[param_Evo]],mode='lines+markers',name=ciudad,hovertemplate='<br><b>Ciudad: </b><extra></extra>'+ciudad+'<br>'+param_Evo+': %{y:.2f}'+'<br>'+'Periodo : %{x}'))
    fig_ciudadesEv.update_yaxes(tickfont=dict(family='Poppins', color='black', size=16),titlefont_size=16, title_text=param_Evo+' '+dict_parametros_unidad[param_Evo], row=1, col=1)
    fig_ciudadesEv.update_xaxes(tickangle=0, tickfont=dict(family='Poppins', color='black', size=14),title_text='Fecha (mes/año)',row=1, col=1
    ,zeroline=True,linecolor = 'rgba(192, 192, 192, 0.8)',zerolinewidth=2)
    fig_ciudadesEv.update_layout(height=550,legend_title=None)
    fig_ciudadesEv.update_layout(font_color="Black",font_family="Poppins",title_font_color="Black",titlefont_size=16,
    title={
    'text':param_Evo+' por ciudad - Internet fijo',
    'y':0.9,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})        
    fig_ciudadesEv.update_layout(legend=dict(orientation="h",y=1.07,x=0.01,font_size=11),showlegend=True)
    fig_ciudadesEv.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig_ciudadesEv.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(192, 192, 192, 0.8)')
    fig_ciudadesEv.update_layout(yaxis_tickformat ='d')
    fig_ciudadesEv.update_layout(xaxis_tickformat ='%m/%y')
    fig_ciudadesEv.add_annotation(
    showarrow=False,
    text='',
    font=dict(size=11), xref='x domain',x=0.5,yref='y domain',y=-0.2) 
    st.plotly_chart(fig_ciudadesEv,use_container_width=True)
    st.download_button(label="Descargar CSV",data=convert_df(dfFijoCiudCapi),file_name='EvolucionIntFijo.csv',mime='text/csv')
        
 


    st.markdown("<p style='font-size:12px;text-align:center'><b>Nota:</b> Resultados basados en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2023 - 2023/1S. </p>",unsafe_allow_html=True)
            

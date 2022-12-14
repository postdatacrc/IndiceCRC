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
import unidecode
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

##Definiciones M??vil

def DownloadMOVIL(x):
    min_down=5;max_down=50;weight_down=0.35
    if x>max_down:
        y=100*weight_down
    elif x<min_down:
        y=0
    else:    
        y= y=(x/max_down)*100*weight_down
    return y
def UploadMOVIL(x):
    min_up=2.6;max_up=15;weight_up=0.25
    if x>max_up:
        y=100*weight_up
    elif x<min_up:
        y=0
    else:    
        y= y=(x/max_up)*100*weight_up
    return y
def LatencyMOVIL(x):
    min_Lat=25;max_Lat=100;weight_Lat=0.20
    if x>=max_Lat:
        y=0
    elif x<=min_Lat:
        y=100*weight_Lat
    else:
        y=100*(max_Lat-x)*weight_Lat/(max_Lat-min_Lat)
    return y
def JitterMOVIL(x):
    min_Jit=0;max_Jit=50;weight_Jit=0.1
    if x>=max_Jit:
        y=0
    elif x<=min_Jit:
        y=100*weight_Jit
    else:
        y=100*(max_Jit-x)*weight_Jit/(max_Jit-min_Jit)
    return y
def AvgPacket(x):
    weight_AvgPack=0.1
    y=y=100*(100-x)*weight_AvgPack/(100)
    return y

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
    fig.update_xaxes(tickangle=0, tickfont=dict(family='Poppins', color='black', size=14),title_text='Fecha (mes/a??o)',row=1, col=1
    ,zeroline=True,linecolor = 'rgba(192, 192, 192, 0.8)',zerolinewidth=2)
    fig.update_layout(height=550,legend_title=None)
    fig.update_layout(font_color="Black",font_family="Poppins",title_font_color="Black",titlefont_size=16,
    title={
    'text':'Evoluci??n '+ParametroFijo+' por operador',
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
    fig.update_xaxes(tickangle=0, tickfont=dict(family='Poppins', color='black', size=14),title_text='Fecha (mes/a??o)',row=1, col=1
    ,zeroline=True,linecolor = 'rgba(192, 192, 192, 0.8)',zerolinewidth=2)
    fig.update_layout(height=550,legend_title=None)
    fig.update_layout(font_color="Black",font_family="Poppins",title_font_color="Black",titlefont_size=16,
    title={
    'text':'Evoluci??n '+ParametroMovil+' por operador',
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
    FijosMuni=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/Bases/BaseFijosMunicipios.csv')
    return FijosMuni
BaseFijosMunicipios=ReadDataFijoMunicipios()
BaseFijosMunicipios['Indice_Descarga']=BaseFijosMunicipios['download_speed'].apply(DownloadFIJO)
BaseFijosMunicipios['Indice_Carga']=BaseFijosMunicipios['upload_speed'].apply(UploadFIJO)
BaseFijosMunicipios['Indice_Latencia']=BaseFijosMunicipios['latency'].apply(LatencyFIJO)
BaseFijosMunicipios['Indice_Jitter']=BaseFijosMunicipios['jitter'].apply(JitterFIJO)
BaseFijosMunicipios['Indice_CRC']=BaseFijosMunicipios['Indice_Descarga']+BaseFijosMunicipios['Indice_Carga']+BaseFijosMunicipios['Indice_Latencia']+BaseFijosMunicipios['Indice_Jitter']
BaseFijosMunicipios[['download_speed','upload_speed','latency','jitter','Indice_CRC']]=BaseFijosMunicipios[['download_speed','upload_speed','latency','jitter','Indice_CRC']]
BaseFijosMunicipios['municipio']=BaseFijosMunicipios['municipio'].apply(lambda x:unidecode.unidecode(x).upper())
BaseFijosMunicipios['departamento']=BaseFijosMunicipios['departamento'].apply(lambda x:unidecode.unidecode(x).upper())
BaseFijosMunicipios['departamento']=BaseFijosMunicipios['departamento'].replace({'CAUCA DEPARTMENT':'CAUCA','NORTH SANTANDER':'NORTE DE SANTANDER',
                                                                        'SAN ANDRES AND PROVIDENCIA':'SAN ANDRES','SANTANDER DEPARTMENT':'SANTANDER',
                                                                        'BOGOTA':'BOGOTA, D.C.','NARINO':'NARI??O'})

#@st.cache(ttl=24*3600,allow_output_mutation=True)
def ReadDataMovilesMunicipios():
    MovilesMuni=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/Bases/BaseMovilesMunicipio.csv')
    return MovilesMuni
BaseMovilesMunicipio=ReadDataMovilesMunicipios()
BaseMovilesMunicipio[['download_speed','upload_speed','latency','jitter']]=round(BaseMovilesMunicipio[['download_speed','upload_speed','latency','jitter']],3)
BaseMovilesMunicipio['Indice_Descarga']=BaseMovilesMunicipio['download_speed'].apply(DownloadMOVIL)
BaseMovilesMunicipio['Indice_Carga']=BaseMovilesMunicipio['upload_speed'].apply(UploadMOVIL)
BaseMovilesMunicipio['Indice_Latencia']=BaseMovilesMunicipio['latency'].apply(LatencyMOVIL)
BaseMovilesMunicipio['Indice_Jitter']=BaseMovilesMunicipio['jitter'].apply(JitterMOVIL)
BaseMovilesMunicipio['Indice_AvgPack']=BaseMovilesMunicipio['AvgPack'].apply(AvgPacket)
BaseMovilesMunicipio['Indice_CRC']=BaseMovilesMunicipio['Indice_Descarga']+BaseMovilesMunicipio['Indice_Carga']+BaseMovilesMunicipio['Indice_Latencia']+BaseMovilesMunicipio['Indice_Jitter']+BaseMovilesMunicipio['Indice_AvgPack']
BaseMovilesMunicipio['municipio']=BaseMovilesMunicipio['municipio'].apply(lambda x:unidecode.unidecode(x).upper())
BaseMovilesMunicipio['departamento']=BaseMovilesMunicipio['departamento'].apply(lambda x:unidecode.unidecode(x).upper())
BaseMovilesMunicipio['departamento']=BaseMovilesMunicipio['departamento'].replace({'CAUCA DEPARTMENT':'CAUCA','NORTH SANTANDER':'NORTE DE SANTANDER',
                                                                        'SAN ANDRES AND PROVIDENCIA':'SAN ANDRES','SANTANDER DEPARTMENT':'SANTANDER',
                                                                        'BOGOTA':'BOGOTA, D.C.','NARINO':'NARI??O'})

#@st.cache(allow_output_mutation=True)
def MunicipiosColombia():
    gdf= gpd.read_file("https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/co_2018_MGN_MPIO_POLITICO.geojson")
    gdf=gdf.rename(columns={'MPIO_CNMBR':'municipio','MPIO_CCNCT':'ID_MUNICIPIO','DPTO_CNMBR':'departamento'})
    gdf['municipio']=gdf['municipio'].apply(lambda x:unidecode.unidecode(x))
    gdf['departamento']=gdf['departamento'].apply(lambda x:unidecode.unidecode(x))
    gdf['departamento']=gdf['departamento'].replace({'ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA':'SAN ANDRES','NARINO':'NARI??O'})
    gdf['municipio']=gdf['municipio'].replace('BOGOTA, D.C.','BOGOTA')
    return gdf
gdf=MunicipiosColombia()
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

st.markdown("<center><h2>??ndice de calidad de la experiencia - ICE</h2></center>",unsafe_allow_html=True)
select_seccion = st.selectbox('Escoja la secci??n del reporte',['Definici??n','Resultados'])   


reemplazo_Muni={'SANTA FE DE ANTIOQUIA':'SANTAFE DE ANTIOQUIA','BOGOTA, D.C.':'BOGOTA','CUASPUD CARLOSAMA':'CUASPUD',
                'SOTARA - PAISPAMBA':'SOTARA','EL CANTON DEL SAN PABLO':'CANTON DEL SAN PABLO'}

                
capitales_departamento={'AMAZONAS':'LETICIA','ANTIOQUIA':'MEDELLIN','ARAUCA':'ARAUCA','ATLANTICO':'BARRANQUILLA','BOGOTA, D.C.':'BOGOTA',
                        'BOLIVAR':'CARTAGENA','BOYACA':'TUNJA','CALDAS':'MANIZALES','CAQUETA':'FLORENCIA','CASANARE':'YOPAL','CAUCA':'POPAYAN',
                        'CESAR':'VALLEDUPAR','CHOCO':'QUIBDO','CORDOBA':'MONTERIA','GUAINIA':'INIRIDA','GUAVIARE':'SAN JOSE DEL GUAVIARE',
                        'HUILA':'NEIVA','LA GUAJIRA':'RIOHACHA','MAGDALENA':'SANTA MARTA','META':'VILLAVICENCIO','NARI??O':'PASTO',
                        'NORTE DE SANTANDER':'CUCUTA','PUTUMAYO':'MOCOA','QUINDIO':'RISARALDA','SAN ANDRES':'SAN ANDRES','SANTANDER':'BUCARAMANGA',
                        'SUCRE':'SINCELEJO','TOLIMA':'IBAGUE','VALLE DEL CAUCA':'CALI','VAUPES':'MITU','VICHADA':'PUERTO CARRENO'}                
capitales_departamento_inv={v: k for k, v in capitales_departamento.items()}
def capitales_Dep(x):
    y=capitales_departamento_inv[x]
    return y    
List_capitales=list(capitales_departamento.values())

Intro_Sec1=r"""<p style='text-align:justify'> 
El ??ndice de calidad de la experiencia -ICE- busca dar a conocer el comportamiento de las capitales de departamento del pa??s que cuentan con las mejores 
condiciones en t??rminos de calidad que experimenta el usuario en el servicio de Internet prestado a trav??s de redes de acceso m??vil y fijo.
</p>
"""

Intro_Sec2=r"""<p style='text-align:justify'> 
Teniendo en cuenta lo estipulado en la regulaci??n vigente, la CRC ha estado utilizando la metodolog??a de Crowdsourcing para capturar informaci??n de indicadores
de calidad directamente de los equipos terminales de los usuarios. En ese sentido, y con la finalidad de entregar a los usuarios informaci??n t??cnica de una 
manera m??s sencilla, nace la idea de consolidar los par??metros para la construcci??n de un ??ndice, en aras de facilitar la lectura y entendimiento de la 
calidad de los servicios que prestan los operados a los usuarios, para este caso, se definir?? un ??ndice para la calidad del servicio de Internet m??vil y un 
??ndice para Internet fijo.
</p>
"""

Intro_Sec3=r"""<p style='text-align:justify'>  
En ese contexto, el reporte t??cnico ETSI TR 103 559 analiza la construcci??n y la metodolog??a de una evaluaci??n comparativa en una medici??n nacional, 
considerando aspectos como el ??rea y la poblaci??n a cubrir, la recopilaci??n y agregaci??n de las mediciones, y la ponderaci??n de los diversos aspectos 
considerados, con el principal prop??sito de identificar las mejores pr??cticas que se deben tener en cuenta a la hora de realizar una evaluaci??n comparativa, 
de tal manera que esta refleje la verdadera experiencia del usuario.
</p>
"""

Intro_Sec4=r"""<p style='text-align:justify'> 
Considerando las recomendaciones y buenas pr??cticas contenidas en el mencionado reporte t??cnico de la ETSI, la CRC dise???? el ??ndice de calidad de la 
experiencia con el prop??sito de reducir la asimetr??a de la informaci??n hacia el usuario, de tal manera que pueda tomar decisiones bien informado, respecto de 
la contrataci??n de los servicios de Internet m??vil e Internet fijo. 
</p>
"""

Intro_Sec5=r""" <p style='text-align:justify'>
Adicionalmente, el ICE busca tambi??n incentivar la mejora continua de la calidad de los servicios de Internet fijo y m??vil que se prestan a los usuarios, 
considerando para tal efecto los cinco (5) siguientes par??metros:
<center>
<ul>
<li>Velocidad de descarga
<li>Velocidad de carga
<li>Latencia
<li>Jitter
<li>Tasa de p??rdida de paquetes
</ul>
</center>
</p>
"""

Intro_Sec6=r"""<p style='text-align:justify'>
Este ??ndice arroja un valor m??ximo de cien (100) puntos y se calcula de acuerdo con la evaluaci??n de los par??metros antes descritos, definiendo unos valores 
que permiten la normalizaci??n y con la aplicaci??n de unos ponderadores.
</p>
"""

Vel_descarga_Info=r"""<p style='text-align:justify'>
Se entiende como la rapidez con la que se pueden descargar contenidos (documentos, videos, im??genes, audio, etc.), normalmente desde una p??gina Web. A mayor 
velocidad obtenida en la medici??n, mayor rapidez en la descarga, y, por lo tanto, mejor experiencia del usuario. La medici??n de este par??metro se normaliza a 
un valor de 0 a 100, utilizando para ello un valor m??nimo de velocidad de 5 Mbps y un m??ximo de 25 Mbps en Internet m??vil y de 25 Mbps y 500 Mbps en Internet 
fijo.
</p>
"""
Vel_carga_Info=r"""<p style='text-align:justify'>
Se entiende como qu?? tan r??pido se env??an los datos en direcci??n desde un dispositivo hacia Internet. Es decir, es la rapidez con la que se pueden subir 
contenidos (cargar archivos adjuntos al correo, compartir pantalla en una video conferencia, subir im??genes a redes sociales, etc.) a Internet. A mayor 
velocidad obtenida en la medici??n, mayor rapidez en la carga, por lo tanto, mejor es la experiencia del usuario. La medici??n de este par??metro se normaliza a 
un valor de 0 a 100, utilizando para ello un valor m??nimo de velocidad de 2,6 Mbps y un m??ximo de 12,5 Mbps en Internet m??vil y de 5 Mbps y 500 Mbps en Internet
fijo.
</p>
"""
Lat_Info=r"""<p style='text-align:justify'>
Sirve para medir qu?? tan r??pido viajan los datos desde un punto de origen al destino. Por ejemplo, en los videojuegos en l??nea, cuando hay alta latencia se 
tarda en refrescar la pantalla con respecto a la velocidad de lo que ocurre en el juego. Por tal motivo, a latencias m??s bajas, la experiencia del usuario es
mejor. La latencia se mide en milisegundos (ms). La medici??n de este par??metro se normaliza a un valor de 0 a 100, utilizando para ello un valor m??nimo de 
latencia de 25 ms y un m??ximo de 100 ms, tanto para Internet m??vil como para el fijo.
</p>
"""
Jitter_Info=r"""<p style='text-align:justify'>
Es una medida en el tiempo de la fluctuaci??n en la entrega y recepci??n de paquetes. Este comportamiento puede ser percibido cuando en las llamadas (de audio o 
video) se presentan interrupciones. Esto se traduce en que a valores bajos (en milisegundos) de este par??metro, mejor es la experiencia del usuario. La medici??n
de este par??metro se normaliza a un valor de 0 a 100, utilizando para ello un valor m??nimo de jitter de 0 ms y un m??ximo de 50 ms, tanto para Internet m??vil 
como para el fijo.
</p>
"""
TPerida_paquetes_Info=r"""<p style='text-align:justify'>
Los paquetes pueden verse como contenedores de informaci??n (audio, video, archivos, etc.), los cuales se env??an y reciben en toda interacci??n en Internet. En 
este contexto, la p??rdida de paquetes ocurre cuando la cantidad de paquetes recibidos no es igual a la cantidad de paquetes transmitidos. En este caso, pueden 
evidenciarse interrupciones en las llamadas (audio o video), en la reproducci??n de contenidos multimedia, etc. A menor tasa de p??rdida de paquetes, mejor es la
experiencia del usuario. La medici??n de este par??metro se normaliza a un valor de 0 a 100, utilizando para ello un valor m??nimo de tasa de p??rdida de paquetes
de 0 % y un m??ximo de 100 % para Internet m??vil. La informaci??n de este par??metro no se encuentra disponible para Internet fijo.
</p>
"""

dict_parametros={'Velocidad de descarga':'download_speed','Velocidad de carga':'upload_speed','Latencia':'latency','Jitter':'jitter','ICE':'Indice_CRC'}
dict_parametros_unidad={'Velocidad de descarga':'(mpbs)','Velocidad de carga':'(mbps)','Latencia':'(ms)','Jitter':'(ms)','ICE':'(%)'}

if select_seccion=='Definici??n':
    st.markdown("")
    st.title("Definici??n del ICE")       
    st.markdown(r"""<hr>""",unsafe_allow_html=True)
    st.markdown("")
    st.markdown(Intro_Sec1,unsafe_allow_html=True)
    st.markdown(Intro_Sec2,unsafe_allow_html=True)
    st.markdown(Intro_Sec3,unsafe_allow_html=True)
    st.markdown(Intro_Sec4,unsafe_allow_html=True)
    st.markdown(Intro_Sec5,unsafe_allow_html=True)
    st.markdown(Intro_Sec6,unsafe_allow_html=True)
    st.markdown("A continuaci??n se presenta una definici??n detallada de cada uno de los par??metros usados para el c??lculo del ??ndice",unsafe_allow_html=True)
    
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
        with st.expander('Tasa p??rdida paquetes'):
            st.markdown(TPerida_paquetes_Info,unsafe_allow_html=True)

    st.markdown(r"""<p style='text-align:justify'>El c??lculo del ICE est?? conformado por la sumatoria de la relaci??n del valor de la medici??n y el valor de normalizaci??n y 
    el producto con el ponderador de cada uno de los indicadores. En las tablas 1 y 2 se pueden observar estos ponderadores, as?? como los valores de 
    normalizaci??n indicados previamente.</p>""",unsafe_allow_html=True)    
    
    col1,col2=st.columns(2)
    with col1:
        st.markdown("<p style='font-size:11px;text-align:center'><b>Tabla 1:</b> Valores de referencia para el c??lculo del ICE para el servicio de Internet m??vil</p>",unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/ICE%20Movil2.png")
    with col2:
        st.markdown("<p style='font-size:11px;text-align:center'><b>Tabla 2:</b> Valores de referencia para el c??lculo del ICE para el servicio de Internet fijo</p>",unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/ICE%20Fijo2.png")
        
if select_seccion=='Resultados':
    st.markdown("")
    st.title("Resultados ICE") 
    st.markdown(r"""<hr style='border:1px solid #FE9D82'>""",unsafe_allow_html=True)
                    
    
    st.markdown("<h3> Comparaci??n posiciones de ciudades por periodo</h3>",unsafe_allow_html=True) 
    st.markdown(r"""<hr>""",unsafe_allow_html=True) 

    BaseFijosMunicipios=BaseFijosMunicipios[(BaseFijosMunicipios['provider']=='All Providers Combined')&(BaseFijosMunicipios['municipio'].isin(List_capitales))]
    BaseFijosMunicipios['prueba']=BaseFijosMunicipios['municipio'].apply(capitales_Dep)
    BaseFijosMunicipios=BaseFijosMunicipios.loc[(BaseFijosMunicipios['departamento'] == BaseFijosMunicipios['prueba'])]
    BaseFijosMunicipios['Indice_CRC']=round(BaseFijosMunicipios['Indice_CRC'],2)
    BaseFijosMunicipios['municipio']=BaseFijosMunicipios['municipio'].replace({'SAN JOSE DEL GUAVIARE':'SJ. GUAVIARE'})
    BaseFijosMunicipios=BaseFijosMunicipios.sort_values(by=['periodo'],ascending=False)
    Ciudades_capitales=sorted(BaseFijosMunicipios['municipio'].unique().tolist())
    Ciudades_capitales.insert(0,'COLOMBIA')      
    #
    BaseMovilesMunicipio=BaseMovilesMunicipio[(BaseMovilesMunicipio['provider']=='All Providers Combined')&(BaseMovilesMunicipio['municipio'].isin(List_capitales))]
    BaseMovilesMunicipio['prueba']=BaseMovilesMunicipio['municipio'].apply(capitales_Dep)
    BaseMovilesMunicipio=BaseMovilesMunicipio.loc[(BaseMovilesMunicipio['departamento'] == BaseMovilesMunicipio['prueba'])]
    BaseMovilesMunicipio['municipio']=BaseMovilesMunicipio['municipio'].replace({'SAN JOSE DEL GUAVIARE':'SJ. GUAVIARE'})
    BaseMovilesMunicipio=BaseMovilesMunicipio.sort_values(by=['periodo'],ascending=False)
    Ciudades_capitales=sorted(BaseMovilesMunicipio['municipio'].unique().tolist())
    Ciudades_capitales.insert(0,'COLOMBIA') 
           
    periodos_posiciones=BaseFijosMunicipios['periodo'].unique().tolist()        
    
    col1b,col2b,col3b=st.columns(3)
    with col2b:
        select_periodoComp1=st.selectbox('Escoja un periodo',periodos_posiciones,0)
        if periodos_posiciones.index(select_periodoComp1)<len(periodos_posiciones)-1:
            second_period=periodos_posiciones[periodos_posiciones.index(select_periodoComp1)+1]
        else:
            second_period=select_periodoComp1
   
    st.markdown("""<p style='font-size:12px'><b>Nota</b>: El cambio en la posici??n se compara respecto al periodo inmediatamente anterior</p>""",unsafe_allow_html=True)
    
    col1c,col2c=st.columns(2)
    with col1c:    
        prueba1=BaseFijosMunicipios[BaseFijosMunicipios['periodo']==select_periodoComp1].sort_values(by=['Indice_CRC'],ascending=False).reset_index()
        prueba1['posici??n']=prueba1.index+1
        prueba1=prueba1[['periodo','municipio','Indice_CRC','posici??n','download_speed','upload_speed','latency','jitter']]
        prueba1[['download_speed','upload_speed','latency','jitter']]=round(prueba1[['download_speed','upload_speed','latency','jitter']],2)
        replace_colname={'download_speed':'Vel descarga '+select_periodoComp1,'upload_speed':'Vel carga '+select_periodoComp1,'latency':'Latencia '+select_periodoComp1,'jitter':'Jitter '+select_periodoComp1}
        prueba1=prueba1.rename(columns=replace_colname)

        prueba2=BaseFijosMunicipios[BaseFijosMunicipios['periodo']==second_period].sort_values(by=['Indice_CRC'],ascending=False).reset_index()
        prueba2['posici??n']=prueba2.index+1
        prueba2=prueba2[['periodo','municipio','Indice_CRC','posici??n']]
        
        Compara_Ciudad=prueba1.merge(prueba2, left_on=['municipio'],right_on=['municipio'])
        Compara_Ciudad['Cambio_indice']=round((Compara_Ciudad['Indice_CRC_x']-Compara_Ciudad['Indice_CRC_y']),2)   
        Compara_Ciudad['Cambio posici??n']=Compara_Ciudad['posici??n_y']-Compara_Ciudad['posici??n_x']
        Compara_Ciudad['Cambio posici??n']=Compara_Ciudad['Cambio posici??n'].apply(cambiopos)
        Compara_Ciudad=Compara_Ciudad.sort_values(by=['posici??n_x'],ascending=True)
        
        BaseFijosMunicipios2=BaseFijosMunicipios.copy()[['periodo','municipio','departamento','Indice_CRC']]
                
        pruebaHTML=Compara_Ciudad[['Cambio posici??n','posici??n_x','municipio','Indice_CRC_x']]
        pruebaHTML['barra']=""
        pruebaHTML=pruebaHTML.values.tolist()
        Title="""<table class='styled-table'>
          <tr>
            <th></th>
            <th>Posici??n</th>
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
        st.markdown(Title+htmlcode(pruebaHTML,0,26),unsafe_allow_html=True)  

    with col2c:                
        prueba1Movil=BaseMovilesMunicipio[BaseMovilesMunicipio['periodo']==select_periodoComp1].sort_values(by=['Indice_CRC'],ascending=False).reset_index()
        prueba1Movil['posici??n']=prueba1Movil.index+1
        prueba1Movil=prueba1Movil[['periodo','municipio','Indice_CRC','posici??n','download_speed','upload_speed','latency','jitter']].round(2)
        #prueba1Movil[['download_speed','upload_speed','latency','jitter']]=round(prueba1[['download_speed','upload_speed','latency','jitter']],2)
        replace_colnameMovil={'download_speed':'Vel descarga '+select_periodoComp1,'upload_speed':'Vel carga '+select_periodoComp1,'latency':'Latencia '+select_periodoComp1,'jitter':'Jitter '+select_periodoComp1}
        prueba1Movil=prueba1Movil.rename(columns=replace_colnameMovil)

        prueba2Movil=BaseMovilesMunicipio[BaseMovilesMunicipio['periodo']==second_period].sort_values(by=['Indice_CRC'],ascending=False).reset_index()
        prueba2Movil['posici??n']=prueba2Movil.index+1
        prueba2Movil=prueba2Movil[['periodo','municipio','Indice_CRC','posici??n']]
        
        Compara_CiudadMovil=prueba1Movil.merge(prueba2Movil, left_on=['municipio'],right_on=['municipio'])
        Compara_CiudadMovil['Cambio_indice']=round((Compara_CiudadMovil['Indice_CRC_x']-Compara_CiudadMovil['Indice_CRC_y']),2)   
        Compara_CiudadMovil['Cambio posici??n']=Compara_CiudadMovil['posici??n_y']-Compara_CiudadMovil['posici??n_x']
        Compara_CiudadMovil['Cambio posici??n']=Compara_CiudadMovil['Cambio posici??n'].apply(cambiopos)
        Compara_CiudadMovil=Compara_CiudadMovil.sort_values(by=['posici??n_x'],ascending=True)
        
        BaseMovilesMunicipios2=BaseMovilesMunicipio.copy()[['periodo','municipio','departamento','Indice_CRC']]        
        
        pruebaHTMLMovil=round(Compara_CiudadMovil[['Cambio posici??n','posici??n_x','municipio','Indice_CRC_x']],2)
        pruebaHTMLMovil['barra']=""
        pruebaHTMLMovil=pruebaHTMLMovil.values.tolist()
        TitleMovil="""<table class='styled-table'>
          <tr>
            <th></th>
            <th>Posici??n</th>
            <th style='width:200px'>Municipio</th>
            <th colspan="2" style='text-align:left'>ICE</th>
          </tr> 
          """
        def htmlcodeMovil(x,a,b):
            html=""
            maximo_Indice=max([i[3] for i in x])
            for i in x[a:b]:
                width_linea=round(i[3]*100/maximo_Indice,2)
                html+="""<tr><td>"""+i[0]+"""</td><td>"""+str(i[1])+"""</td><td style='text-align:left'>"""+i[2]+"""</td><td>"""+str(i[3])+"""</td>"""
                html+="""<td style="width:300px"><hr style='background:linear-gradient(to right,#39B399 """+str(width_linea)+"""%, #ADE5D9 """+str(width_linea)+"""%, #ADE5D9 100%);height:15px;'></td></tr>"""
            html=html+"""</table>"""    
            return html   
        
        st.markdown("<center><h2 style='color:#39B399'>Internet m??vil</h2></center>",unsafe_allow_html=True)     
        st.markdown(TitleMovil+htmlcodeMovil(pruebaHTMLMovil,0,26),unsafe_allow_html=True)   
        
        ################################################################################################################     

    
    st.markdown("<h3> Evoluci??n temporal capitales departamentales</h3>",unsafe_allow_html=True) 
    st.markdown(r"""<hr>""",unsafe_allow_html=True)
    param_Evo=st.radio('Escoja el par??metro a visualizar',['ICE','Velocidad de descarga','Velocidad de carga','Latencia','Jitter'],horizontal=True)
    Select_ciudCapital=st.multiselect('Escoja las ciudades capitales a comparar',Ciudades_capitales) 
    col1d,col2d=st.columns(2)

    with col1d:            
        dfFijoCiudCapi=BaseFijosMunicipios[BaseFijosMunicipios['municipio'].isin(Select_ciudCapital)]
        dfFijoCiudCapi=dfFijoCiudCapi[['periodo','municipio',dict_parametros[param_Evo]]]
        dfFijoCol=BaseFijosMunicipios.groupby(['periodo'])[dict_parametros[param_Evo]].mean().reset_index().round(1)
        dfFijoCol['municipio']='COLOMBIA'
        dfFijoCiudCapi=pd.concat([dfFijoCiudCapi,dfFijoCol])
        fig_ciudadesEv=make_subplots(rows=1,cols=1)
        for ciudad in Select_ciudCapital:
            dfFijoCiudCapi2=dfFijoCiudCapi[dfFijoCiudCapi['municipio']==ciudad]
            fig_ciudadesEv.add_trace(go.Scatter(x=dfFijoCiudCapi2['periodo'],y=dfFijoCiudCapi2[dict_parametros[param_Evo]],mode='lines+markers',name=ciudad,hovertemplate='<br><b>Ciudad: </b><extra></extra>'+ciudad+'<br>'+param_Evo+': %{y:.2f}'+'<br>'+'Periodo : %{x}'))
        fig_ciudadesEv.update_yaxes(tickfont=dict(family='Poppins', color='black', size=16),titlefont_size=16, title_text=param_Evo+' '+dict_parametros_unidad[param_Evo], row=1, col=1)
        fig_ciudadesEv.update_xaxes(tickangle=0, tickfont=dict(family='Poppins', color='black', size=14),title_text='Fecha (mes/a??o)',row=1, col=1
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
        
 
        ############################   
    with col2d:            
        dfMovilCiudCapi=BaseMovilesMunicipio[BaseMovilesMunicipio['municipio'].isin(Select_ciudCapital)]
        dfMovilCiudCapi=dfMovilCiudCapi[['periodo','municipio',dict_parametros[param_Evo]]]
        dfMovilCol=BaseMovilesMunicipio.groupby(['periodo'])[dict_parametros[param_Evo]].mean().reset_index().round(1)
        dfMovilCol['municipio']='COLOMBIA'
        dfMovilCiudCapi=pd.concat([dfMovilCiudCapi,dfMovilCol])
        fig_ciudadesEvMovil=make_subplots(rows=1,cols=1)
        for ciudad in Select_ciudCapital:
            dfMovilCiudCapi2=dfMovilCiudCapi[dfMovilCiudCapi['municipio']==ciudad]
            fig_ciudadesEvMovil.add_trace(go.Scatter(x=dfMovilCiudCapi2['periodo'],y=dfMovilCiudCapi2[dict_parametros[param_Evo]],mode='lines+markers',name=ciudad,hovertemplate='<br><b>Ciudad: </b><extra></extra>'+ciudad+'<br>'+param_Evo+': %{y:.2f}'+'<br>'+'Periodo : %{x}'))
        fig_ciudadesEvMovil.update_yaxes(tickfont=dict(family='Poppins', color='black', size=16),titlefont_size=16, title_text=param_Evo+' '+dict_parametros_unidad[param_Evo], row=1, col=1)
        fig_ciudadesEvMovil.update_xaxes(tickangle=0, tickfont=dict(family='Poppins', color='black', size=14),title_text='Fecha (mes/a??o)',row=1, col=1
        ,zeroline=True,linecolor = 'rgba(192, 192, 192, 0.8)',zerolinewidth=2)
        fig_ciudadesEvMovil.update_layout(height=550,legend_title=None)
        fig_ciudadesEvMovil.update_layout(font_color="Black",font_family="Poppins",title_font_color="Black",titlefont_size=16,
        title={
        'text':param_Evo+' por ciudad - Internet m??vil',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})        
        fig_ciudadesEvMovil.update_layout(legend=dict(orientation="h",y=1.07,x=0.01,font_size=11),showlegend=True)
        fig_ciudadesEvMovil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        fig_ciudadesEvMovil.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(192, 192, 192, 0.8)')
        fig_ciudadesEvMovil.update_layout(yaxis_tickformat ='d')
        fig_ciudadesEvMovil.update_layout(xaxis_tickformat ='%m/%y')
        fig_ciudadesEvMovil.add_annotation(
        showarrow=False,
        text='',
        font=dict(size=11), xref='x domain',x=0.5,yref='y domain',y=-0.2) 
        st.plotly_chart(fig_ciudadesEvMovil,use_container_width=True)


    st.markdown("<p style='font-size:12px;text-align:center'><b>Nota:</b> Resultados basados en el an??lisis realizado por CRC de los datos de Speedtest Intelligence?? para 2018 - 2021. </p>",unsafe_allow_html=True)
            
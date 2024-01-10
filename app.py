import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import datetime as datetime
from datetime import datetime as dt

import plotly.graph_objs as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Glava",
    layout="centered"
)

with open("styles/main.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.title("Glava")


with open("styles/main.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.title('Timedata Glava')

filnavn = st.file_uploader('Last opp Excel-fil med timedata')

if filnavn:

    sted = st.selectbox('Velg sted som data skal vises fra',options=['Pottemakergata','Havnegata'])

    data = pd.read_excel(filnavn,sheet_name=sted,usecols='A:B')

    data = data[:-1]


    data['Dato-time'] = pd.to_datetime(data['Dato-time'],format="%Y-%m-%d %H:%M:%S")
    data['Dato-time'] = data["Dato-time"].dt.round("H")

    aar20 = data.loc[(data['Dato-time'] >= '2020-01-01') & (data['Dato-time'] < '2021-01-01')]
    aar21 = data.loc[(data['Dato-time'] >= '2021-01-01') & (data['Dato-time'] < '2022-01-01')]
    aar22 = data.loc[(data['Dato-time'] >= '2022-01-01') & (data['Dato-time'] < '2023-01-01')]
    aar23 = data.loc[(data['Dato-time'] >= '2023-01-01') & (data['Dato-time'] < '2024-01-01')]

    #aar20['Timenummer'] = aar20['Dato-time'].apply(lambda x: (x.timetuple().tm_yday - 1) * 24 + x.hour)
    #aar21['Timenummer'] = aar21['Dato-time'].apply(lambda x: (x.timetuple().tm_yday - 1) * 24 + x.hour)
    #aar22['Timenummer'] = aar22['Dato-time'].apply(lambda x: (x.timetuple().tm_yday - 1) * 24 + x.hour)
    #aar23['Timenummer'] = aar23['Dato-time'].apply(lambda x: (x.timetuple().tm_yday - 1) * 24 + x.hour)

    aar21 = aar21.reset_index(drop = True)
    aar21.rename(columns={'Dato-time':'Dato 2021','Sum Timeverdi': 'Effekt 2021'}, inplace=True)
    aar22 = aar22.reset_index(drop = True)
    aar22.rename(columns={'Dato-time':'Dato 2022','Sum Timeverdi': 'Effekt 2022'}, inplace=True)
    aar23 = aar23.reset_index(drop = True)
    aar23.rename(columns={'Dato-time':'Dato 2023','Sum Timeverdi': 'Effekt 2023'}, inplace=True)

    aar_alle = pd.concat([aar21,aar22,aar23], axis=1)

    ###
    temp21 = pd.read_excel('data/Temp 2021.xlsx',usecols='C:D')
    temp21['Tid(norsk normaltid)'] = pd.to_datetime(temp21['Tid(norsk normaltid)'],format="%d.%m.%Y %H:%M")
    temp21['Tid(norsk normaltid)'] = temp21['Tid(norsk normaltid)'].dt.round("H")
    temp21.rename(columns={'Tid(norsk normaltid)':'Dato 2021'}, inplace=True)
    aar21_medtemp = pd.merge(aar21,temp21,on='Dato 2021',how='outer')

    temp22 = pd.read_excel('data/Temp 2022.xlsx',usecols='C:D')
    temp22['Tid(norsk normaltid)'] = pd.to_datetime(temp22['Tid(norsk normaltid)'],format="%d.%m.%Y %H:%M")
    temp22['Tid(norsk normaltid)'] = temp22['Tid(norsk normaltid)'].dt.round("H")
    temp22.rename(columns={'Tid(norsk normaltid)':'Dato 2022'}, inplace=True)
    aar22_medtemp = pd.merge(aar22,temp22,on='Dato 2022',how='outer')

    temp23 = pd.read_excel('data/Temp 2023.xlsx',usecols='C:D')
    temp23['Tid(norsk normaltid)'] = pd.to_datetime(temp23['Tid(norsk normaltid)'],format="%d.%m.%Y %H:%M")
    temp23['Tid(norsk normaltid)'] = temp23['Tid(norsk normaltid)'].dt.round("H")
    temp23.rename(columns={'Tid(norsk normaltid)':'Dato 2023'}, inplace=True)
    aar23_medtemp = pd.merge(aar23,temp23,on='Dato 2023',how='outer')


    def plottefunksjon_2akser(x_data, x_navn, y_data1, y_navn1, y_data2, y_navn2, yakse_navn, tittel):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=x_data, y=y_data1, mode="lines", name=y_navn1, line=dict(color='#367A2F')), secondary_y=False)
        fig.add_trace(go.Scatter(x=x_data, y=y_data2, mode="lines", name=y_navn2, line=dict(color='#FFC358')), secondary_y=True)
        fig.update_layout(title=tittel, xaxis_title=x_navn, yaxis_title=yakse_navn, legend_title=None)
        fig.update_yaxes(title_text=y_navn1, secondary_y=False)
        fig.update_yaxes(title_text=y_navn2, secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
        #return fig


    with st.expander('Effektforbruk og utetemperatur'):
        plottefunksjon_2akser(aar21_medtemp['Dato 2021'],'Dato',aar21_medtemp['Effekt 2021'],'Effekt',aar21_medtemp['Lufttemperatur'],'Lufttemperatur','Lala','Effektforbruk og utetemperatur 2021')
        plottefunksjon_2akser(aar22_medtemp['Dato 2022'],'Dato',aar22_medtemp['Effekt 2022'],'Effekt',aar22_medtemp['Lufttemperatur'],'Lufttemperatur','Lala','Effektforbruk og utetemperatur 2022')
        plottefunksjon_2akser(aar23_medtemp['Dato 2023'],'Dato',aar23_medtemp['Effekt 2023'],'Effekt',aar23_medtemp['Lufttemperatur'],'Lufttemperatur','Lala','Effektforbruk og utetemperatur 2023')


    c1, c2, c3 = st.columns(3)
    sum_2021 = f"{int(np.sum(aar21['Effekt 2021'])/1000):,} MWh".replace(",", " ")
    sum_2022 = f"{int(np.sum(aar22['Effekt 2022'])/1000):,} MWh".replace(",", " ")
    sum_2023 = f"{int(np.sum(aar23['Effekt 2023'])/1000):,} MWh".replace(",", " ")
    with c1:
        st.metric('Energiforbruk 2021',sum_2021)
    with c2:
        st.metric('Energiforbruk 2022',sum_2022)
    with c3:
        st.metric('Energiforbruk 2023',sum_2023)

    c1, c2, c3 = st.columns(3)
    maks_2021 = f"{int(np.max(aar21['Effekt 2021'])):,} kW".replace(",", " ")
    maks_2022 = f"{int(np.max(aar22['Effekt 2022'])):,} kW".replace(",", " ")
    maks_2023 = f"{int(np.max(aar23['Effekt 2023'])):,} kW".replace(",", " ")
    with c1:
        st.metric('Effektforbruk 2021',maks_2021)
    with c2:
        st.metric('Effektforbruk 2022',maks_2022)
    with c3:
        st.metric('Effektforbruk 2023',maks_2023)


    fig = px.line(aar_alle, x='Dato 2021', y=['Effekt 2021','Effekt 2022','Effekt 2023'], title='Effektforbruk', color_discrete_sequence=['#367A2F', '#C2CF9F', '#FFC358', '#FFE7BC'])
    fig.update_layout(xaxis_title='Dato', yaxis_title='Effekt (kW)',legend_title=None)

    st.plotly_chart(fig, use_container_width=True)

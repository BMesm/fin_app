import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

def format_func(option):
    return range_date[option]

df = pd.read_csv("./data/test.csv")
df = df.loc[~df['Catégorie'].isna()]
df['Montant'] = df['Montant'].str.replace(',','.').astype(float).abs()
df["Date valeur"] = pd.to_datetime(df["Date valeur"])
df["Date comptable"] = pd.to_datetime(df["Date comptable"])

min_date = df['Date comptable'].min()
max_date = df['Date comptable'].max()
col1,col2 = st.columns(2)
with col2:
  range_date = {(max_date - datetime.timedelta(days=30), max_date): "Dernier 30 jours", (min_date , max_date): "Toute les dates"}
  select_range_date = st.selectbox("Select option", options=list(range_date.keys()), format_func=format_func,label_visibility="collapsed",index=1)
with col1:
  d = st.date_input(
      "",
      select_range_date,
      min_date,
      max_date,
      format="MM.DD.YYYY",
      label_visibility="collapsed"
  )

df = df[(df["Date valeur"].dt.date> d[0]) & (df["Date valeur"].dt.date < d[1])]

df

fig = px.sunburst(df,
                #   names = 'Sous-catégorie',
                #   parents = 'Catégorie',
                  path=['Catégorie','Sous-catégorie'],
                  values = 'Montant',
                  branchvalues = 'total'
                  )


st.plotly_chart(fig, use_container_width=True)
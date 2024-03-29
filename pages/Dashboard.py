import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

def format_date(option):
    return range_date[option]

def format_amount(option):
    return range_amount[option]

def load_format_data():
  dfb = pd.read_csv("./saved_data/testbel.csv")
  dfi = pd.read_csv("./saved_data/testing.csv")
  dfbel = dfb.loc[:,['Date de comptabilisation','Montant','Catégorie','Sous-catégorie']].rename(columns={'Date de comptabilisation':'Date comptable'})
  dfbel['Compte'] = 'Belfius'
  dfing = dfi.loc[:,['Date comptable','Montant','Catégorie','Sous-catégorie']]
  dfing['Compte'] = 'Ing'
  df = pd.concat([dfbel,dfing],ignore_index=True)
  df = df.loc[~df['Catégorie'].isna()]
  df["Date comptable"] = pd.to_datetime(df["Date comptable"])
  return df

df = load_format_data()
cat_data = pd.read_csv('./data/cat.csv')

min_date = df['Date comptable'].min()
max_date = df['Date comptable'].max()
col1,col2 = st.columns(2)
with col2:
  range_date = {(max_date - datetime.timedelta(days=30), max_date): "Dernier 30 jours", (min_date , max_date): "Toute les dates"}
  select_range_date = st.selectbox("Select range date", options=list(range_date.keys()), format_func=format_date,label_visibility="hidden",index=1)
with col1:
  d = st.date_input(
      "Période",
      select_range_date,
      min_date,
      max_date,
      label_visibility="visible"
  )

col1,col2 = st.columns(2)
with col1:
  select_cat = st.multiselect('Selection des catégories', cat_data.loc[:,'cat'].unique())
with col2:
  amount_type = ((df['Montant'] < 0),(df['Montant'] > 0))
  range_amount = {0:'Dépenses',1:'Rentrées'}
  select_amount_type = st.selectbox("Selection type de montant", options=list(range_amount.keys()), format_func=format_amount)

df = df[(df["Date comptable"].dt.date> d[0]) & (df["Date comptable"].dt.date < d[1])]
df = df.loc[df['Catégorie'].isin(select_cat)]
df = df.loc[amount_type[select_amount_type]]
df['Montant'] = df['Montant'].abs()

df

fig = px.sunburst(df,
                  path=['Catégorie','Sous-catégorie'],
                  values = 'Montant',
                  # branchvalues = 'total',
                  )
fig2 = go.Figure(go.Sunburst(
                  labels=fig['data'][0]['labels'].tolist(),
                  parents=fig['data'][0]['parents'].tolist(),
                  values=fig['data'][0]['values'].tolist(),
                  branchvalues='total',
                  # hovertemplate='<b>%{label} :</b> %{value} €'
                  ))

fig2.update_layout(margin = dict(t=0, l=0, r=0, b=0))

st.plotly_chart(fig2, use_container_width=True)
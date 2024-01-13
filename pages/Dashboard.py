import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("./test.csv")
df = df.loc[~df['Catégorie'].isna() & df['Montant']>0]
df['Montant'] = df['Montant'].str.replace(',','.').astype(float).abs()
    # df_details = df.loc[df['Catégorie'].isna() & ~df["Détails du mouvement"].isna(),'Date comptable':"Sous-catégorie"]

df

fig = px.sunburst(df,
                #   names = 'Sous-catégorie',
                #   parents = 'Catégorie',
                  path=['Catégorie','Sous-catégorie'],
                  values = 'Montant',
                  branchvalues = 'total'
                  )


st.plotly_chart(fig, use_container_width=True)
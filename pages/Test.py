import streamlit as st
import pandas as pd
import numpy as np

cat_data = pd.read_csv("./data/cat.csv")
sub_cat = st.selectbox("Sous-catégorie",cat_data["sub_cat"].unique(),index=None,placeholder="Select subcat...",)
if sub_cat==None:
   cat = st.selectbox("Catégorie",cat_data["cat"].unique(),index=None,placeholder="Select cat...",)
else:
   cat = st.selectbox("Catégorie",cat_data.loc[cat_data['sub_cat']==sub_cat,'cat'].unique(),placeholder="Select caté...",)


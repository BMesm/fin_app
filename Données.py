import streamlit as st
import datetime
import pandas as pd

#Style
st.set_page_config(
    page_title="Finance App",
    page_icon=":chart_with_upwards_trend:",
    layout='wide',
    initial_sidebar_state='auto',
    menu_items=None
)
st.write('<style>div.row-widget.stRadio > *{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
# st.write('<style>div.row-widget.stRadio > label{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
        num_rows="dynamic"
    )
    return edited_df

def add_columns(df):
    df['Catégorie']=None
    df["Sous-catégorie"]=None
    return df

def save_df(df_tosave,path):
    df_tosave.index = pd.RangeIndex(1,len(df_tosave)+1)
    df_tosave.to_csv(path,index=False)

def record_index(selected_rows,column_selected):
    mask_search = (search_word_data['cat'] == cat) & (search_word_data['sub_cat'] == sub_cat) & (search_word_data['word'] == search_word)
    if not search_word_data.loc[mask_search].index.empty:
        index = search_word_data.loc[mask_search].index[0]
        search_word_data.at[index,'indexes'] = selected_rows
    else:
        search_word_data.loc[max(search_word_data.index)+1,['cat','sub_cat','word','search_col','search_colB','indexes']] = [cat, sub_cat, search_word,column_selected,'Nom contrepartie contient', selected_rows]
    search_word_data.to_json('./data/search_words.json',orient="index",indent=4)

def submit_cat(df,selection,cat,sub_cat,search_word_data):
    df.loc[df.index.isin(selection.index.to_list()),"Catégorie"] = cat
    df.loc[df.index.isin(selection.index.to_list()),"Sous-catégorie"] = sub_cat
    df.to_csv('./saved_data/testing.csv',index=False)

def apply_search_words(search_word_data):
    df = pd.read_csv("./data/ingb.csv")
    df["Date valeur"] = pd.to_datetime(df["Date valeur"])
    df["Date comptable"] = pd.to_datetime(df["Date comptable"])
    if ~{'Catégorie','Sous-catégorie'}.issubset(df.columns):
        df = add_columns(df)

    df_searched = df.copy()

    for i, row in search_word_data.loc[~search_word_data.search_col.isna()].iterrows():
        if row['indexes']:
            mask = (df[row['search_col']].str.contains(row['word'],na=False,case=False,regex=True) & ~df["Unnamed: 0"].isin(row["indexes"]))
        else:
            mask = (df[row['search_col']].str.contains(row['word'],na=False,case=False,regex=True))
        df_searched.loc[mask,'Sous-catégorie'] = row['sub_cat']
        df_searched.loc[mask,'Catégorie'] = row['cat']
    df_searched['Montant'] = df_searched['Montant'].str.replace(',','.').astype(float)

    return df_searched

def format_funcr(option):
    return range_date[option]

cat_data = pd.read_csv("./data/cat.csv")
search_word_data = pd.read_json("./data/search_words.json",orient='index')
df = apply_search_words(search_word_data)

min_dates = df['Date comptable'].min()
max_dates = df['Date comptable'].max()
col1,col2 = st.columns(2)
with col2:
    range_date = {(max_dates - datetime.timedelta(days=30), max_dates): "Dernier 30 jours",
                (min_dates , max_dates): "Toute les dates"}
    select_range_dates = st.selectbox("Select option", options=list(range_date.keys()), format_func=format_funcr,label_visibility="collapsed",index=1)
with col1:
    date_selected = st.date_input(
        "Selected",
        select_range_dates,
        min_dates,
        max_dates,
        label_visibility="collapsed",
        key="dez"
    )

with st.expander("Données non classifiés : Libellés"):
    df_label = df.loc[df['Catégorie'].isna() & df["Détails du mouvement"].isna(),'Date comptable':"Sous-catégorie"]
    df_label[(df_label["Date valeur"].dt.date> date_selected[0]) & (df_label["Date valeur"].dt.date < date_selected[1])]
    #Debug line
    st.write(len(df_label[(df_label["Date valeur"].dt.date> date_selected[0]) & (df_label["Date valeur"].dt.date < date_selected[1])]))

with st.expander("Données non classifiés : Détails du mouvement"):
    df_details = df.loc[df['Catégorie'].isna() & ~df["Détails du mouvement"].isna(),'Date comptable':"Sous-catégorie"]
    df_details[(df_details["Date valeur"].dt.date> date_selected[0]) & (df_details["Date valeur"].dt.date < date_selected[1])]
    #Debug line
    st.write(len(df_details[(df_details["Date valeur"].dt.date> date_selected[0]) & (df_details["Date valeur"].dt.date < date_selected[1])]))

with st.expander("Ajouter une catégorie"):
    with st.form("add_cat"):
        new_cat = st.data_editor(cat_data,num_rows="dynamic")
        st.form_submit_button("submit",on_click=save_df(new_cat,"./data/cat.csv"))

with st.container():
    column_selected = st.radio("Sélection de colonne",["Libellés","Détails du mouvement"],label_visibility="visible")
    search_word = st.text_input("Terme à chercher")
    col1, col2 = st.columns(2)
    with col1:
        cat = st.selectbox("Catégorie",cat_data["cat"].unique(),)
    with col2:
        sub_cat = st.selectbox("Sous-catégorie",cat_data["sub_cat"].unique())
    df_filtred = df[df[column_selected].str.contains(search_word,na=False,case=False,regex=True)]
    edited_df = dataframe_with_selections(df_filtred)

    #Debug line
    # st.write(len(selection))
    if st.button('Submit'):
        selected_rows = edited_df.loc[edited_df.Select,'Unnamed: 0'].to_list()
        record_index(selected_rows,column_selected)

        unselected_rows = edited_df[edited_df.Select == False]
        selection = unselected_rows.drop('Select', axis=1)
        submit_cat(df,selection,cat,sub_cat,search_word_data)




import streamlit as st
import streamlit_local_storage as sls

def LocalStorageManager():
    return sls.LocalStorage()

localS = LocalStorageManager()

if "get_val" not in st.session_state:
    st.session_state["get_val"] = None


with st.form("get_data"):
    st.text_input("key", key="get_local_storage_v")
    st.form_submit_button("Submit") 

if st.session_state["get_local_storage_v"] != "":
    val_ = localS.getItem(st.session_state["get_local_storage_v"], key="test_get_item")
    st.session_state["get_val"] = val_
st.write(st.session_state["get_val"])

ket = st.text_input("key")
vat = st.text_input("value")

if st.button('test'):
    localS.setItem(ket,vat)
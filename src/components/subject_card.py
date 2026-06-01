
import streamlit as st

def subject_card(name, code, section, students, classes):
    with st.container(border=True):
        st.subheader(name)
        st.write(
            f"📘 Code : `{code}`  |  🏫 Section : {section}"
        )
        c1, c2= st.columns(2)

        with c1:
            st.info(f"👥 {students} Students")
        with c2:
            st.warning(f"📚 {classes} Classes")
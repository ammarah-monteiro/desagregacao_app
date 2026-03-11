import streamlit as st
import pandas as pd
from processamento import processar_dataframe

st.set_page_config(page_title="Desagregação de Linhas", layout="wide")

st.title("Aplicação de Desagregação de Linhas")
st.write("Carrega um ficheiro CSV, processa os dados e descarrega o resultado.")

def ler_csv_upload(ficheiro):
    # tenta ; primeiro
    try:
        ficheiro.seek(0)
        return pd.read_csv(ficheiro, sep=";")
    except Exception:
        try:
            ficheiro.seek(0)
            return pd.read_csv(ficheiro, sep=",")
        except Exception:
            ficheiro.seek(0)
            return pd.read_csv(ficheiro)


ficheiro = st.file_uploader("Escolhe um ficheiro CSV", type=["csv"])

if ficheiro is not None:
    try:
        df = ler_csv_upload(ficheiro)

        st.success("Ficheiro carregado com sucesso.")
        st.write(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")

        st.subheader("Pré-visualização do input")
        st.dataframe(df.head(20), use_container_width=True)

        if st.button("Processar ficheiro"):
            with st.spinner("A processar..."):
                df_final = processar_dataframe(df)

            st.success("Processamento concluído.")

            st.subheader("Pré-visualização do output")
            st.dataframe(df_final.head(20), use_container_width=True)

            csv_saida = df_final.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Descarregar resultado CSV",
                data=csv_saida,
                file_name="resultado_expandido.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

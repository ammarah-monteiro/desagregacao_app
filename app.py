import streamlit as st
import pandas as pd
from io import StringIO
from processamento import processar_dataframe

st.set_page_config(page_title="Desagregação de Linhas", layout="wide")

st.title("Aplicação de Desagregação de Linhas")
st.write("Carrega um ficheiro CSV, processa os dados e descarrega o resultado.")

def ler_csv_upload(ficheiro):
    from io import StringIO
    import pandas as pd

    ficheiro.seek(0)
    conteudo = ficheiro.read().decode("utf-8", errors="ignore")
    linhas = conteudo.splitlines()

    header_idx = 0
    for i, linha in enumerate(linhas[:15]):
        texto = linha.upper()
        if "AIRPORT" in texto and "START DATE" in texto:
            header_idx = i
            break

    linhas_dados = linhas[header_idx:]
    total_linhas_brutas = len(linhas_dados) - 1  # sem cabeçalho
    conteudo_limpo = "\n".join(linhas_dados)

    try:
        df = pd.read_csv(
            StringIO(conteudo_limpo),
            sep=None,
            engine="python",
            skip_blank_lines=True,
            quotechar='"',
            on_bad_lines="skip"
        )
    except Exception:
        df = pd.read_csv(
            StringIO(conteudo_limpo),
            sep=";",
            engine="python",
            skip_blank_lines=True,
            quotechar='"',
            on_bad_lines="skip"
        )

    df.columns = df.columns.astype(str).str.strip()
    df = df.dropna(axis=1, how="all")

    linhas_lidas = len(df)
    linhas_ignoradas = max(total_linhas_brutas - linhas_lidas, 0)

    return df, linhas_ignoradas

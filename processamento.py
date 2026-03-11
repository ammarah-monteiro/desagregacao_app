import pandas as pd

# Mapeamento de dias
day_map = {
    "1": 0,  # Monday
    "2": 1,  # Tuesday
    "3": 2,  # Wednesday
    "4": 3,  # Thursday
    "5": 4,  # Friday
    "6": 5,  # Saturday
    "7": 6   # Sunday
}


def expand_days(row):
    # Garantir que FREQ é string limpa
    freq = "" if pd.isna(row["FREQ"]) else str(row["FREQ"]).replace(".", "")

    # Criar todas as datas entre START DATE e END DATE
    all_dates = pd.date_range(row["START DATE"], row["END DATE"])

    # Obter dias válidos de operação
    days_of_operation = [day_map[char] for char in freq if char in day_map]

    # Filtrar datas pelos dias da semana indicados em FREQ
    filtered_dates = [date for date in all_dates if date.weekday() in days_of_operation]

    # Retornar todas as colunas da linha + nova coluna DATE
    expanded_rows = pd.DataFrame({**row.to_dict(), "DATE": filtered_dates})
    return expanded_rows


def processar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Limpar nomes das colunas
    df.columns = df.columns.str.strip()

    # Validar colunas obrigatórias
    colunas_obrigatorias = ["START DATE", "END DATE", "TIME", "REQ TIME", "FREQ"]
    faltam = [col for col in colunas_obrigatorias if col not in df.columns]

    if faltam:
        raise ValueError(f"Faltam colunas obrigatórias: {', '.join(faltam)}")

    # Converter colunas para datetime
    df["START DATE"] = pd.to_datetime(df["START DATE"], errors="coerce")
    df["END DATE"] = pd.to_datetime(df["END DATE"], errors="coerce")

    # Converter TIME para hora
    df["TIME"] = pd.to_datetime(
        df["TIME"].astype(str).str.zfill(4),
        format="%H%M",
        errors="coerce"
    ).dt.time

    # Converter REQ TIME para hora
    df["REQ TIME"] = pd.to_datetime(
        df["REQ TIME"].astype(str).str.zfill(4),
        format="%H%M",
        errors="coerce"
    ).dt.time

    # Limpar FREQ
    df["FREQ"] = df["FREQ"].astype(str).str.replace(".", "", regex=False)

    # Remover linhas sem datas válidas
    df = df.dropna(subset=["START DATE", "END DATE"])

    # Expandir linhas por dias
    resultado_expandido = df.apply(expand_days, axis=1).to_list()

    if not resultado_expandido:
        return pd.DataFrame()

    result = pd.concat(resultado_expandido, ignore_index=True)

    # Adicionar número da semana
    result["WEEK NUMBER"] = result["DATE"].dt.isocalendar().week.astype(int)

    # Adicionar nome do dia da semana
    result["WEEK DAY"] = result["DATE"].dt.strftime("%a")

    # Remover duplicados
    result = result.drop_duplicates().reset_index(drop=True)

    return result
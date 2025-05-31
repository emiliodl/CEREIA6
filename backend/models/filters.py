import pandas as pd
import ast
from dicionarios import equivalencia_estadiamento, bio_to_column

def converter_lista_string_para_lista(string_lista):
    try:
        return ast.literal_eval(string_lista)
    except (ValueError, SyntaxError):
        return []

def filtrar_estudos_tipo_tumor(df, tipo_tumor, termo_2=None):
    colunas_esperadas = ["term_1", "term_2", "term_3", "term_4", "term_5"]
    for coluna in colunas_esperadas:
        if coluna not in df.columns:
            raise KeyError(f"A coluna '{coluna}' não existe no DataFrame.")

    if tipo_tumor:
        mask = (
            df["term_1"].str.strip().eq(tipo_tumor)
            | df["term_2"].str.strip().eq(tipo_tumor)
            | df["term_3"].str.strip().eq(tipo_tumor)
            | df["term_4"].str.strip().eq(tipo_tumor)
            | df["term_5"].str.strip().eq(tipo_tumor)
        )
        if termo_2:
            mask &= (
                df["term_1"].str.strip().eq(termo_2)
                | df["term_2"].str.strip().eq(termo_2)
                | df["term_3"].str.strip().eq(termo_2)
                | df["term_4"].str.strip().eq(termo_2)
                | df["term_5"].str.strip().eq(termo_2)
            )
        filtered_df = df[mask]
        return filtered_df
    else:
        return df

def filtrar_estudos_estadiamento(df, estadiamento):
    if estadiamento:
        # Verificar se o estadiamento começa com "Estágio"
        estagio_romano = None
        if estadiamento.startswith("Estágio "):
            # Extrair o número romano (I, II, III, IV)
            estagio_romano = estadiamento.replace("Estágio ", "")
            # Usar o número romano diretamente
            if estagio_romano in equivalencia_estadiamento:
                estadiamentos_equivalentes = equivalencia_estadiamento[estagio_romano]
                estadiamentos_df = df["Tipo_stages"].apply(converter_lista_string_para_lista)
                filtrado = df[
                    estadiamentos_df.apply(
                        lambda x: any(item in estadiamentos_equivalentes for item in x)
                    )
                ]
                return filtrado
            else:
                print(f"Estágio '{estagio_romano}' não encontrado no dicionário de equivalência.")
                return df
        else:
            # Método original para outros formatos de estadiamento
            estadiamentos_reverso = {}
            for k, v in equivalencia_estadiamento.items():
                for x in v:
                    estadiamentos_reverso[x] = k

            if estadiamento in estadiamentos_reverso:
                estadiamentos_equivalentes = equivalencia_estadiamento[
                    estadiamentos_reverso[estadiamento]
                ]
                
                if estadiamentos_equivalentes:
                    estadiamentos_df = df["Tipo_stages"].apply(converter_lista_string_para_lista)
                    filtrado = df[
                        estadiamentos_df.apply(
                            lambda x: any(item in estadiamentos_equivalentes for item in x)
                        )
                    ]
                    return filtrado
            
            print(f"Estadiamento '{estadiamento}' não encontrado no dicionário de equivalência.")
            return df
    else:
        return df

def filtrar_por_ecog(df, valor_ecog):
    if valor_ecog:
        if "Tem ECOG" not in df.columns:
            raise KeyError("A coluna 'Tem ECOG' não existe no DataFrame.")

        df["ECOG_score"] = df["ECOG_score"].str.strip()
        df_filtrado = df[
            df["ECOG_score"].str.contains(valor_ecog, case=False, na=False)
        ]

        return df_filtrado
    else:
        return df

def filtrar_estudos_por_biomarcadores(df, selecoes_biomarcadores):
    df = df.copy()
    df["biomarcador_match"] = True  # Assume all studies match initially

    for biomarcador, valor in selecoes_biomarcadores.items():
        if valor:
            coluna = bio_to_column.get(biomarcador)
            if coluna:
                if coluna in df.columns:
                    df[coluna] = df[coluna].fillna("")
                    match = df[coluna] == valor
                    df["biomarcador_match"] &= match
                    print(f"Aplicando filtro: {coluna} == {valor}")
    return df
import pandas as pd
import ast

# Carregar os dados do arquivo CSV
file_path = 'df_final_matches_tipo_cancer_atualizado.csv'
df_a = pd.read_csv(file_path)

# Substituir valores NaN por listas vazias
df_a['meshes'] = df_a['meshes'].fillna('[]')

# Converter a coluna 'meshes' de strings para listas de dicionários
df_a['meshes'] = df_a['meshes'].apply(ast.literal_eval)

# Função para criar o dicionário
def create_dictionary_from_meshes(df):
    result_dict = {}
    for mesh_list in df['meshes']:
        if isinstance(mesh_list, list) and mesh_list:  # Verifica se é uma lista e não está vazia
            first_term = mesh_list[0].get('term', 'Unknown')  # Pega o primeiro termo, usa 'Unknown' se não existir
            other_terms = [mesh.get('term', 'Unknown') for mesh in mesh_list[1:]]  # Pega os demais termos, usa 'Unknown' se não existir
            result_dict[first_term] = other_terms
    return result_dict

# Criar o dicionário
meshes_dict_novo = create_dictionary_from_meshes(df_a)

print(meshes_dict_novo)

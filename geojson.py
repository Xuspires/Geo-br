import geopandas as gpd
import pandas as pd
import os
from pathlib import Path

# Caminho da pasta com os arquivos JSON
pasta_json = r"C:\Users\vitor.barbosa\Documents\Json estados"

# Nomes dos arquivos
arquivos_nomes = ['br_es.json', 'br_mg.json', 'br_rj.json', 'br_sp.json']

# Constrói caminhos completos
arquivos = [os.path.join(pasta_json, f) for f in arquivos_nomes]
gdfs = []

try:
    # Valida e lê arquivos
    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            print(f"⚠️ Arquivo não encontrado: {arquivo}")
            continue
        
        try:
            gdf = gpd.read_file(arquivo)
            if gdf.empty:
                print(f"⚠️ Arquivo vazio: {arquivo}")
                continue
            print(f"✓ {arquivo}: {len(gdf)} registros lidos")
            gdfs.append(gdf)
        except Exception as e:
            print(f"❌ Erro ao ler {arquivo}: {e}")
            continue
    
    if not gdfs:
        raise ValueError("Nenhum arquivo foi carregado com sucesso!")
    
    # Valida CRS
    crs_list = [gdf.crs for gdf in gdfs]
    if len(set(str(crs) for crs in crs_list)) > 1:
        print("⚠️ CRS diferentes detectados. Unificando para o primeiro arquivo...")
        gdfs = [gdf.to_crs(gdfs[0].crs) if gdf.crs != gdfs[0].crs else gdf for gdf in gdfs]
    
    # Concatena e exporta
    sudeste = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
    arquivo_saida = os.path.join(pasta_json, "sudeste_brasil.json")
    sudeste.to_file(arquivo_saida, driver='GeoJSON')
    print(f"✓ Arquivo exportado com sucesso: {len(sudeste)} registros totais")
    print(f"📍 Localização: {arquivo_saida}")

except Exception as e:
    print(f"❌ Erro crítico: {e}")
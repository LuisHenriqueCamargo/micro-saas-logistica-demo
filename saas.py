import os
import pandas as pd
import openrouteservice
from datetime import datetime
from tinydb import TinyDB, Query
from pathlib import Path
import uuid

# === CONFIGURAÇÕES ===
ORS_API_KEY = "5b3ce3597851110001cf62481247f0b46098443fa36ee782e4c0430a"
DB_PATH = "rotas.json"
CTE_FOLDER = "cte_files"
DADOS_BASE = "dados_base"
INSIGHTS_FOLDER = "insights"
MODELO_PATH = os.path.join(CTE_FOLDER, "cte_modelo.xlsx")
EXPORT_PATH = os.path.join(INSIGHTS_FOLDER, "fato_cte.txt")

# === CLIENT OPENROUTESERVICE ===
client = openrouteservice.Client(key=ORS_API_KEY)

# === CRIA PASTAS ===
for pasta in [CTE_FOLDER, DADOS_BASE, INSIGHTS_FOLDER]:
    Path(pasta).mkdir(parents=True, exist_ok=True)

# === FUNÇÕES UTILITÁRIAS ===
def normalizar(valor):
    if pd.isna(valor) or not str(valor).strip():
        return "NÃO INFORMADO"
    return str(valor).strip().upper()

def gerar_id():
    return str(uuid.uuid4())

def iniciar_banco():
    if not os.path.exists(DB_PATH):
        open(DB_PATH, 'w').close()
    return TinyDB(DB_PATH)

def obter_ou_criar_id(db, tabela, campo_nome, valor):
    tb = db.table(tabela)
    valor = normalizar(valor)
    encontrado = tb.get(Query()[campo_nome] == valor)
    if encontrado:
        return encontrado['id']
    else:
        novo_id = gerar_id()
        tb.insert({"id": novo_id, campo_nome: valor})
        return novo_id

def salvar_cte(db, cte):
    ctes = db.table("ctes")
    CT = Query()
    existe = ctes.search((CT.cte_numero == cte['cte_numero']) & (CT.id_filial == cte['id_filial']))
    if not existe:
        ctes.insert(cte)
        print(f"✅ CT-e {cte['cte_numero']} salvo.")
    else:
        print(f"⚠️ CT-e {cte['cte_numero']} já existe. Ignorado.")

# === CRIAR PLANILHAS MODELO (DEMO) ===
def criar_modelos_base():
    if not os.path.exists(MODELO_PATH):
        dados = []
        for i in range(1, 51):
            dados.append({
                "cte_numero": f"CTE{i:03}",
                "filial": ["São Paulo", "Rio de Janeiro", "Cuiabá"][i % 3],
                "origem_latitude": [-23.5505, -22.9068, -15.6010][i % 3],
                "origem_longitude": [-46.6333, -43.1729, -56.0974][i % 3],
                "destino_latitude": [-22.9083, -23.5075, -23.6235][i % 3],
                "destino_longitude": [-47.0626, -46.7354, -46.7006][i % 3],
                "destino_nome": ["Campinas", "Osasco", "Santo André"][i % 3],
                "frete_valor": 1000 + i * 15,
                "frequencia_semanal": (i % 5) + 1,
                "transportadora": ["LogRio", "TransPaulista", "Rapidão MT"][i % 3],
                "cliente": ["Cliente A", "Cliente B", "Cliente C"][i % 3],
                "produto": ["Eletrônicos", "Alimentos", "Vestuário"][i % 3],
                "região": ["Sudeste", "Centro-Oeste", "Sul"][i % 3]
            })
        pd.DataFrame(dados).to_excel(MODELO_PATH, index=False)

    # Dimensões fixas
    pd.DataFrame([
        {"nome": "São Paulo", "latitude": -23.5505, "longitude": -46.6333},
        {"nome": "Rio de Janeiro", "latitude": -22.9068, "longitude": -43.1729},
        {"nome": "Cuiabá", "latitude": -15.6010, "longitude": -56.0974},
    ]).to_excel(os.path.join(DADOS_BASE, "filiais.xlsx"), index=False)

    pd.DataFrame([
        {"nome": "LogRio", "latitude": -22.9, "longitude": -43.1},
        {"nome": "TransPaulista", "latitude": -23.5, "longitude": -46.6},
        {"nome": "Rapidão MT", "latitude": -15.6, "longitude": -56.1},
    ]).to_excel(os.path.join(DADOS_BASE, "transportadoras.xlsx"), index=False)

    pd.DataFrame([
        {"nome": "Cliente A", "latitude": -23.56, "longitude": -46.65},
        {"nome": "Cliente B", "latitude": -22.91, "longitude": -43.17},
        {"nome": "Cliente C", "latitude": -15.60, "longitude": -56.09},
    ]).to_excel(os.path.join(DADOS_BASE, "clientes.xlsx"), index=False)

    print("📄 Planilhas modelo criadas.")

# === PROCESSAR CTEs ===
def processar_arquivo(db, caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)
    for _, row in df.iterrows():
        try:
            origem = [row['origem_longitude'], row['origem_latitude']]
            destino = [row['destino_longitude'], row['destino_latitude']]
            rota = client.directions(coordinates=[origem, destino], profile='driving-car', format='geojson')
            resumo = rota['features'][0]['properties']['summary']

            cte = {
                "id": gerar_id(),
                "cte_numero": normalizar(row.get("cte_numero")),
                "id_filial": obter_ou_criar_id(db, "filiais", "nome", row.get("filial")),
                "id_transportadora": obter_ou_criar_id(db, "transportadoras", "nome", row.get("transportadora")),
                "id_cliente": obter_ou_criar_id(db, "clientes", "nome", row.get("cliente")),
                "id_produto": obter_ou_criar_id(db, "produtos", "nome", row.get("produto")),
                "id_regiao": obter_ou_criar_id(db, "regioes", "nome", row.get("região")),
                "frete_valor": float(row.get("frete_valor", 0)),
                "frequencia_semanal": int(row.get("frequencia_semanal", 1)),
                "distancia_km": round(resumo['distance'] / 1000, 2),
                "duracao_min": round(resumo['duration'] / 60, 2),
                "data_hora": datetime.now().isoformat()
            }

            salvar_cte(db, cte)
        except Exception as e:
            print(f"❌ Erro ao processar CT-e {row.get('cte_numero', '---')}: {e}")

def processar_pasta(db, pasta):
    arquivos = [f for f in os.listdir(pasta) if f.endswith(".xlsx") and not f.startswith("~$")]
    for arquivo in arquivos:
        print(f"\n🔄 Processando: {arquivo}")
        processar_arquivo(db, os.path.join(pasta, arquivo))

# === EXPORTAR FATO E DIMENSÕES ===
def exportar_fato_cte(db):
    df = pd.DataFrame(db.table("ctes").all())
    if df.empty:
        print("⚠️ Nenhum dado para fato_cte.")
        return
    df['custo_km'] = df['frete_valor'] / df['distancia_km'].replace({0: 1})
    df['custo_mensal'] = df['frete_valor'] * df['frequencia_semanal'] * 4

    colunas = [
        'id', 'cte_numero', 'frete_valor', 'frequencia_semanal', 'distancia_km',
        'duracao_min', 'data_hora', 'custo_km', 'custo_mensal',
        'id_filial', 'id_transportadora', 'id_cliente', 'id_produto', 'id_regiao'
    ]
    df = df[[col for col in colunas if col in df.columns]]
    df.to_csv(EXPORT_PATH, sep='|', index=False)
    print(f"✅ fato_cte.txt exportado para: {EXPORT_PATH}")

def exportar_dimensoes(db):
    def exportar(tabela, nome_arquivo):
        df = pd.DataFrame(db.table(tabela).all())
        if not df.empty:
            caminho = os.path.join(INSIGHTS_FOLDER, nome_arquivo)
            df.to_csv(caminho, sep='|', index=False)
            print(f"✅ {nome_arquivo} exportado.")
        else:
            print(f"⚠️ Tabela {tabela} vazia.")
    exportar("filiais", "dim_filiais.txt")
    exportar("transportadoras", "dim_transportadoras.txt")
    exportar("clientes", "dim_clientes.txt")
    exportar("produtos", "dim_produtos.txt")
    exportar("regioes", "dim_regioes.txt")

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    criar_modelos_base()
    db = iniciar_banco()
    processar_pasta(db, CTE_FOLDER)
    exportar_fato_cte(db)
    exportar_dimensoes(db)

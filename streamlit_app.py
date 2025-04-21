import streamlit as st
import os
import shutil
import zipfile

# Substituições conhecidas
substituicoes = {
    '├ö': 'Ô',
    '├ô': 'Ó',
    '├Ü': 'Ú',
    '┬░': 'º',
    '├º': 'ç',
    '├ú': 'ã',
    '├¡': 'í',
    '├│': 'ó',
    '├¬': 'ê',
    '├ü': 'Á',
    '├®': 'é',
    '├í': 'á',
    '├║': 'ú',
    '├ó': 'â',
    '├á': 'à',
    '├â': 'Ã',
    '├Á': 'õ',
}

# Corrigir caracteres bugados nos nomes
def corrigir_nome(nome):
    for bugado, correto in substituicoes.items():
        nome = nome.replace(bugado, correto)
    return nome

# Renomeia os arquivos
def renomear_arquivos(pasta):
    for arquivo in os.listdir(pasta):
        caminho_antigo = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho_antigo):
            novo_nome = corrigir_nome(arquivo)
            caminho_novo = os.path.join(pasta, novo_nome)
            if caminho_antigo != caminho_novo:
                os.rename(caminho_antigo, caminho_novo)
                st.write(f'Renomeado: "{arquivo}" → "{novo_nome}"')
            else:
                st.write(f'Sem alteração: "{arquivo}"')

# Extrai ZIP com correção de nomes
def extrair_zip_com_encoding(zip_path, destino):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for info in zip_ref.infolist():
            try:
                # Corrige o nome do arquivo se estiver bugado
                nome_corrigido = info.filename.encode('cp437').decode('latin1')
                info.filename = nome_corrigido
            except Exception:
                pass  # Se falhar, mantém como está
            zip_ref.extract(info, destino)

# Limpa os arquivos temporários
def limpar_temp():
    if os.path.exists("fotos"):
        shutil.rmtree("fotos")
    if os.path.exists("temp.zip"):
        os.remove("temp.zip")
    if os.path.exists("fotos_corrigidas.zip"):
        os.remove("fotos_corrigidas.zip")

# Interface Streamlit
st.title("🔄 Renomeador de Fotos - SGL")
st.write("Corrige automaticamente nomes de fotos com símbolos estranhos.")

arquivo_zip = st.file_uploader("Envie a pasta compactada (ZIP) com as fotos:", type=["zip"])

if arquivo_zip:
    limpar_temp()

    with open("temp.zip", "wb") as f:
        f.write(arquivo_zip.getbuffer())

    extrair_zip_com_encoding("temp.zip", "fotos")
    st.success("Arquivo recebido e extraído com sucesso!")

    if st.button("🔄 Renomear fotos"):
        renomear_arquivos("fotos")
        shutil.make_archive("fotos_corrigidas", 'zip', "fotos")

        with open("fotos_corrigidas.zip", "rb") as f:
            st.download_button("📥 Baixar fotos corrigidas", f, "fotos_corrigidas.zip")

        limpar_temp()
else:
    st.info("Aguardando envio do arquivo ZIP...")

import streamlit as st
import os
import shutil
import time

# Função para renomear os arquivos
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
    '├¬': 'ê',
    '├Á': 'õ',
    '├⌐': 'é',
    '├┤': 'ô',
    '├ç': 'Ç'
}

def corrigir_nome(nome):
    for simbolo, letra in substituicoes.items():
        nome = nome.replace(simbolo, letra)
    return nome

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

def limpar_diretorios():
    """Remove os diretórios temporários se existirem"""
    if os.path.exists("temp.zip"):
        os.remove("temp.zip")
    if os.path.exists("fotos_corrigidas.zip"):
        os.remove("fotos_corrigidas.zip")
    if os.path.exists("fotos"):
        shutil.rmtree("fotos")

# Configuração do Streamlit
st.title("🔄 Renomeador de Fotos - SGL")
st.write("Corrige automaticamente nomes de fotos com símbolos estranhos.")

# Limpa diretórios antigos no início
limpar_diretorios()

# Upload da pasta compactada (ZIP)
arquivo_zip = st.file_uploader("Envie a pasta compactada (ZIP) com as fotos:", type=["zip"])

if arquivo_zip:
    with open("temp.zip", "wb") as f:
        f.write(arquivo_zip.getbuffer())

    shutil.unpack_archive("temp.zip", "fotos")
    st.success("Arquivo recebido e extraído com sucesso!")

    if st.button("🔄 Renomear fotos"):
        renomear_arquivos("fotos")
        shutil.make_archive("fotos_corrigidas", 'zip', "fotos")
        
        with open("fotos_corrigidas.zip", "rb") as f:
            btn = st.download_button(
                label="📥 Baixar fotos corrigidas",
                data=f,
                file_name="fotos_corrigidas.zip",
                on_click=lambda: limpar_diretorios()  # Limpa após o download
            )
        
        # Se o usuário não clicar no botão de download, limpa após 1 minuto
        time.sleep(60)
        limpar_diretorios()
else:
    st.info("Aguardando envio do arquivo ZIP...")

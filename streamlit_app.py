import streamlit as st
import os
import shutil

# Função para corrigir nomes com codificação errada
def corrigir_nome(nome):
    try:
        # Tenta simular nomes lidos com a codificação errada (ex: UTF-8 que era pra ser CP1252)
        return nome.encode('latin1').decode('utf-8')
    except UnicodeDecodeError:
        return nome  # Se falhar, retorna o nome original

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

# Limpa os arquivos e pastas temporárias
def limpar_temp():
    if os.path.exists("fotos"):
        shutil.rmtree("fotos")
    if os.path.exists("temp.zip"):
        os.remove("temp.zip")
    if os.path.exists("fotos_corrigidas.zip"):
        os.remove("fotos_corrigidas.zip")

# Interface
st.title("🔄 Renomeador de Fotos - SGL")
st.write("Corrige automaticamente nomes de fotos com símbolos estranhos.")

# Upload
arquivo_zip = st.file_uploader("Envie a pasta compactada (ZIP) com as fotos:", type=["zip"])

if arquivo_zip:
    limpar_temp()  # limpa arquivos antigos antes de processar

    with open("temp.zip", "wb") as f:
        f.write(arquivo_zip.getbuffer())

    shutil.unpack_archive("temp.zip", "fotos")
    st.success("Arquivo recebido e extraído com sucesso!")

    if st.button("🔄 Renomear fotos"):
        renomear_arquivos("fotos")
        shutil.make_archive("fotos_corrigidas", 'zip', "fotos")

        with open("fotos_corrigidas.zip", "rb") as f:
            st.download_button("📥 Baixar fotos corrigidas", f, "fotos_corrigidas.zip")

        limpar_temp()  # limpa tudo depois do download
else:
    st.info("Aguardando envio do arquivo ZIP...")

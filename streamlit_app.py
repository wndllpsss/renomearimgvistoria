import streamlit as st
import os
import shutil
import time
from pathlib import Path

def corrigir_nome(nome_errado):
    try:
        # Tenta corrigir via conversão de codificação (caso seja problema de encoding)
        return nome_errado.encode('cp1252').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Se falhar, mantém o nome original (ou pode adicionar fallback aqui)
        return nome_errado

def renomear_arquivos(pasta):
    for root, _, files in os.walk(pasta):
        for arquivo in files:
            caminho_antigo = os.path.join(root, arquivo)
            
            # Corrige o nome do arquivo
            novo_nome = corrigir_nome(arquivo)
            caminho_novo = os.path.join(root, novo_nome)
            
            if caminho_antigo != caminho_novo:
                try:
                    os.rename(caminho_antigo, caminho_novo)
                    st.write(f'Renomeado: "{arquivo}" → "{novo_nome}"')
                except Exception as e:
                    st.error(f"Erro ao renomear {arquivo}: {str(e)}")

def limpar_diretorios():
    """Remove os diretórios temporários se existirem"""
    temp_files = ["temp.zip", "fotos_corrigidas.zip"]
    temp_dirs = ["fotos"]
    
    for file in temp_files:
        if os.path.exists(file):
            try:
                os.remove(file)
            except:
                pass
                
    for dir in temp_dirs:
        if os.path.exists(dir):
            try:
                shutil.rmtree(dir)
            except:
                pass

# Configuração do Streamlit
st.title("🔄 Renomeador de Fotos - SGL (Versão Avançada)")
st.write("Corrige automaticamente nomes de fotos com problemas de codificação.")

# Limpa diretórios antigos no início
limpar_diretorios()

# Upload da pasta compactada (ZIP)
arquivo_zip = st.file_uploader("Envie a pasta compactada (ZIP) com as fotos:", type=["zip"])

if arquivo_zip:
    with open("temp.zip", "wb") as f:
        f.write(arquivo_zip.getbuffer())

    # Extrai o ZIP tratando a codificação
    try:
        shutil.unpack_archive("temp.zip", "fotos")
        st.success("Arquivo recebido e extraído com sucesso!")
    except Exception as e:
        st.error(f"Erro ao extrair arquivo: {str(e)}")
        st.stop()

    if st.button("🔄 Renomear fotos automaticamente"):
        with st.spinner("Processando arquivos..."):
            renomear_arquivos("fotos")
            
            # Cria novo ZIP
            shutil.make_archive("fotos_corrigidas", 'zip', "fotos")
            
            with open("fotos_corrigidas.zip", "rb") as f:
                btn = st.download_button(
                    label="📥 Baixar fotos corrigidas",
                    data=f,
                    file_name="fotos_corrigidas.zip",
                    mime="application/zip",
                    on_click=lambda: limpar_diretorios()
                )
        
        # Limpa após 2 minutos se não baixar
        time.sleep(120)
        limpar_diretorios()
else:
    st.info("Aguardando envio do arquivo ZIP...")

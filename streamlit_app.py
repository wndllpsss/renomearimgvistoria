import streamlit as st
import os
import shutil

def corrigir_nome(nome_errado):
    try:
        # Tenta corrigir via conversão de codificação
        return nome_errado.encode('cp1252').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return nome_errado

def renomear_arquivos(pasta):
    st.write("Iniciando processo de renomeação...")
    
    for root, _, files in os.walk(pasta):
        for arquivo in files:
            caminho_antigo = os.path.join(root, arquivo)
            novo_nome = corrigir_nome(arquivo)
            caminho_novo = os.path.join(root, novo_nome)
            
            st.write(f"Processando: {arquivo}")
            
            if caminho_antigo != caminho_novo:
                try:
                    os.rename(caminho_antigo, caminho_novo)
                    st.write(f"✅ Renomeado: {arquivo} -> {novo_nome}")
                except Exception as e:
                    st.error(f"❌ Erro ao renomear {arquivo}: {str(e)}")
            else:
                st.write(f"⚠️ Nome já correto: {arquivo}")

def limpar_diretorios():
    temp_files = ["temp.zip", "fotos_corrigidas.zip"]
    temp_dirs = ["fotos"]
    
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)
                
    for dir in temp_dirs:
        if os.path.exists(dir):
            shutil.rmtree(dir)

# Interface principal
st.title("Renomeador de Fotos - SGL")
st.write("Corrige nomes de fotos com problemas de codificação")

# Limpeza inicial
limpar_diretorios()

# Upload do arquivo
arquivo_zip = st.file_uploader("Envie o arquivo ZIP com as fotos:", type=["zip"])

if arquivo_zip:
    # Salva arquivo temporário
    with open("temp.zip", "wb") as f:
        f.write(arquivo_zip.getbuffer())
    
    # Extrai arquivos
    try:
        shutil.unpack_archive("temp.zip", "fotos")
        st.success("Arquivo extraído com sucesso!")
        
        if st.button("Renomear Arquivos"):
            renomear_arquivos("fotos")
            
            # Cria novo ZIP
            shutil.make_archive("fotos_corrigidas", 'zip', "fotos")
            
            # Botão de download
            with open("fotos_corrigidas.zip", "rb") as f:
                st.download_button(
                    label="Baixar Fotos Corrigidas",
                    data=f,
                    file_name="fotos_corrigidas.zip",
                    mime="application/zip"
                )
            
            st.success("Processo concluído!")
            
    except Exception as e:
        st.error(f"Erro ao processar arquivo: {str(e)}")
        limpar_diretorios()

import streamlit as st
import os
import shutil
from pathlib import Path

def corrigir_nome(nome_errado):
    try:
        # Tenta corrigir via conversão de codificação
        return nome_errado.encode('cp1252').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Se falhar, mantém o nome original
        return nome_errado

def renomear_arquivos(pasta):
    # Conta o total de arquivos para a barra de progresso
    total_files = sum([len(files) for _, _, files in os.walk(pasta)])
    progress_bar = st.progress(0)
    processed_files = 0
    
    for root, _, files in os.walk(pasta):
        for arquivo in files:
            caminho_antigo = os.path.join(root, arquivo)
            
            # Corrige o nome do arquivo
            novo_nome = corrigir_nome(arquivo)
            caminho_novo = os.path.join(root, novo_nome)
            
            if caminho_antigo != caminho_novo:
                try:
                    if not os.access(caminho_antigo, os.W_OK):
                        st.warning(f"Sem permissão para modificar: {arquivo}")
                        continue
                        
                    os.rename(caminho_antigo, caminho_novo)
                    st.write(f'Renomeado: "{arquivo}" → "{novo_nome}"')
                except Exception as e:
                    st.error(f"Erro ao renomear {arquivo}: {str(e)}")
            
            # Atualiza a barra de progresso
            processed_files += 1
            progress_bar.progress(processed_files / total_files)

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
st.set_page_config(page_title="Renomeador de Fotos - SGL", page_icon="🔄")
st.title("🔄 Renomeador de Fotos - SGL")
st.write("Corrige automaticamente nomes de fotos com problemas de codificação.")

# Limpa diretórios antigos no início
limpar_diretorios()

# Upload da pasta compactada (ZIP)
arquivo_zip = st.file_uploader("Envie a pasta compactada (ZIP) com as fotos:", type=["zip"])

if arquivo_zip:
    try:
        # Salva o arquivo temporário
        with st.spinner("Salvando arquivo temporário..."):
            with open("temp.zip", "wb") as f:
                f.write(arquivo_zip.getbuffer())
        
        # Extrai o arquivo ZIP
        with st.spinner("Extraindo arquivos..."):
            shutil.unpack_archive("temp.zip", "fotos")
            st.success("✅ Arquivo recebido e extraído com sucesso!")
            
        if st.button("🔄 Renomear fotos automaticamente", type="primary"):
            # Processa os arquivos
            with st.spinner("Processando arquivos..."):
                renomear_arquivos("fotos")
                
                # Cria novo ZIP
                with st.spinner("Criando arquivo ZIP corrigido..."):
                    shutil.make_archive("fotos_corrigidas", 'zip', "fotos")
                
                # Disponibiliza para download
                with open("fotos_corrigidas.zip", "rb") as f:
                    st.download_button(
                        label="📥 Baixar fotos corrigidas",
                        data=f,
                        file_name="fotos_corrigidas.zip",
                        mime="application/zip",
                        on_click=limpar_diretorios
                    )
                
                st.balloons()
                st.success("🎉 Processo concluído com sucesso!")
                
    except Exception as e:
        st.error(f"❌ Erro durante o processamento: {str(e)}")
        limpar_diretorios()
else:
    st.info("ℹ️ Aguardando envio do arquivo ZIP...")

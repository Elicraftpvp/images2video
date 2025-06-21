"""
Script para criar um vídeo MP4 a partir de uma sequência de imagens.

O script procura por imagens com sequencia numerica no mesmo diretorio que o .py
le elas de forma numericamente crescente e as compila em um
único arquivo de vídeo MP4 de qualidade customizavel.
"""
import re
from pathlib import Path
import imageio

# --- CONFIGURAÇÕES ---
# Altere estas variáveis para ajustar o comportamento do script

# 1. Diretório onde as imagens estão localizadas, relativo à pasta do script.
# 
#    O script espera ter a seguinte estrutura de arquivos:
#    - pasta onde esta o script/
#      - script.py
#      - imagens/
#        -imagem_01.jpeg
#        -imagem_02.jpeg...     
#
#    A linha abaixo constrói o caminho para esse diretório imagens.
DIRETORIO_IMAGENS = Path(__file__).parent / 'Images'

# 2. Padrão do nome dos arquivos de imagem a serem procurados.
#    '*' encontrará qualquer arquivo de imagem não coloque nem um outro tipo dentro de imagens.
PADRAO_ARQUIVO = '*'

# 3. Nome do arquivo de vídeo que será gerado no mesmo diretório das imagens.
NOME_VIDEO_SAIDA = 'OUTPUT.mp4'

# 4. Taxa de quadros por segundo (FPS) do vídeo final.
FPS = 24

# 5. Parâmetros de qualidade do vídeo (usando FFMPEG).
#    - codec: 'libx264' é o padrão para H.264/MP4, ótima qualidade e compatibilidade.
#    - ffmpeg_params: ['-crf', '17']
#      'crf' (Constant Rate Factor) controla a qualidade. Valores mais baixos = melhor qualidade.
#      0 é sem perdas, ~17-18 é considerado visualmente sem perdas. 23 é o padrão.
FFMPEG_PARAMS = ['-crf', '17']

# --- FIM DAS CONFIGURAÇÕES ---


def extrair_numero(path_arquivo: Path) -> int:
    """
    Extrai o número de um nome de arquivo para ordenação correta.
    Ex: 'imagemlegal_12.png' -> 12
    Retorna 0 se nenhum número for encontrado.
    """
    match = re.search(r'\d+', path_arquivo.name)
    if match:
        return int(match.group())
    return 0

def criar_video():
    """
    Função principal que encontra as imagens, ordena e cria o vídeo MP4.
    """
    print("🎬 Iniciando criação do vídeo MP4...")
    
    if not DIRETORIO_IMAGENS.is_dir():
        print(f"❌ Erro: O diretório de imagens não foi encontrado!")
        print(f"   Caminho esperado: '{DIRETORIO_IMAGENS.resolve()}'")
        print(f"   Verifique se a estrutura de pastas está correta.")
        return

    print(f"🔎 Procurando por imagens em: '{DIRETORIO_IMAGENS.resolve()}'")
    
    try:
        # Encontra todos os arquivos que correspondem ao padrão
        arquivos_imagem = list(DIRETORIO_IMAGENS.glob(PADRAO_ARQUIVO))
        
        # Filtra para garantir que estamos pegando apenas arquivos de imagem comuns
        extensoes_validas = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        arquivos_imagem = [f for f in arquivos_imagem if f.suffix.lower() in extensoes_validas]

        if not arquivos_imagem:
            print(f"❌ Erro: Nenhuma imagem encontrada com o padrão '{PADRAO_ARQUIVO}' no diretório especificado.")
            return

        # Ordena os arquivos numericamente
        arquivos_ordenados = sorted(arquivos_imagem, key=extrair_numero)

        print("\n✅ Imagens encontradas e ordenadas:")
        for arq in arquivos_ordenados:
            print(f"  -> {arq.name}")

        caminho_saida = DIRETORIO_IMAGENS / NOME_VIDEO_SAIDA
        print(f"\n⚙️  Preparando para criar o vídeo em '{caminho_saida}'")
        print(f"    - FPS: {FPS}")
        print(f"    - Qualidade (CRF): {FFMPEG_PARAMS[1]}")

        # Usa um 'writer' para adicionar os frames um a um.
        # Isso é mais eficiente em termos de memória do que carregar todas as imagens de uma vez.
        with imageio.get_writer(caminho_saida, fps=FPS, codec='libx264', ffmpeg_params=FFMPEG_PARAMS) as writer:
            
            primeira_resolucao = None
            for i, caminho_imagem in enumerate(arquivos_ordenados):
                print(f"    -> Adicionando frame {i+1}/{len(arquivos_ordenados)}: {caminho_imagem.name}")
                try:
                    frame = imageio.imread(caminho_imagem)

                    # Define a resolução do vídeo com base na primeira imagem
                    if primeira_resolucao is None:
                        primeira_resolucao = frame.shape[:2]
                        print(f"    - Resolução do vídeo definida para: {frame.shape[1]}x{frame.shape[0]}")
                    
                    # Alerta se as resoluções forem diferentes
                    if frame.shape[:2] != primeira_resolucao:
                        print(f"    ⚠️  Aviso: A imagem '{caminho_imagem.name}' tem uma resolução diferente e será redimensionada.")
                        # O FFMPEG geralmente lida com isso, mas o aviso é importante.

                    writer.append_data(frame)
                except Exception as e:
                    print(f"    ⚠️  Aviso: Não foi possível processar '{caminho_imagem.name}'. Pulando. Erro: {e}")
        
        print(f"\n✨ Vídeo '{caminho_saida.name}' criado com sucesso!")

    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado durante a criação do vídeo: {e}")

if __name__ == "__main__":
    criar_video()
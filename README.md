# Gerador de Vídeo a partir de Sequência de Imagens

Este script Python cria um vídeo no formato MP4 a partir de uma sequência de imagens numeradas.

## 🚀 Funcionalidades

- Busca automaticamente imagens em um diretório.
- Ordena as imagens numericamente.
- Cria um vídeo MP4 com qualidade configurável.
- Suporte a vários formatos de imagem: PNG, JPG, JPEG, BMP, TIFF.

## 🗂️ Estrutura de Pastas

```
📂 SeuProjeto
 ┣ 📂 Images
 ┃ ┣ 🖼️ imagem_01.jpg
 ┃ ┣ 🖼️ imagem_02.jpg
 ┃ ┗ 🖼️ ...
 ┗ ⚙️ script.py
```

## ⚙️ Configurações no Script

- **DIRETORIO_IMAGENS:** Define a pasta onde estão as imagens.
- **PADRAO_ARQUIVO:** Padrão dos arquivos a serem buscados (use '*' para todos).
- **NOME_VIDEO_SAIDA:** Nome do arquivo MP4 de saída.
- **FPS:** Taxa de quadros por segundo do vídeo.
- **FFMPEG_PARAMS:** Parâmetros de qualidade do FFMPEG (ex.: \`-crf 17\`).

## 🛠️ Pré-requisitos

- Python 3.x
- Instale as dependências necessárias:

```
pip install imageio[ffmpeg]
```

Caso o de cima não funcione coloque diretamente na pasta a força

``` bash
"C:/Program Files/Python312/python.exe" -m pip install imageio[ffmpeg]
```

## ▶️ Como Usar

1. Coloque suas imagens numeradas na pasta ```Images```.
2. Execute o script:

```
image2video.py
```

3. O vídeo gerado estará na mesma pasta das imagens, com o nome definido em \`NOME_VIDEO_SAIDA\`.

## 🔧 Personalização

- Para mudar a qualidade, ajuste o valor de \`crf\` dentro da variável \`FFMPEG_PARAMS\`.  
Valores recomendados:
- ```0``` = Sem perdas (arquivo muito grande)
- ```17-18``` = Visualmente sem perdas
- ```23``` = Qualidade padrão

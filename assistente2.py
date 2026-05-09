import keyboard
import speech_recognition as sr
import pyautogui as pg
import time
import datetime
import sounddevice as sd
import soundfile as sf
import pyperclip
import win32gui
from gtts import gTTS
import os # MUDOU
# TEMPERATURA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_NOMES_PATH = os.path.join(BASE_DIR, 'save_nomes.txt')
SAVE_VIDEOS_PATH = os.path.join(BASE_DIR, 'save_videos.txt')

'''import requests # MUDOU


API_KEY = "3af2bcc6b61fef54d95c007032ca1868"
cidade = "Porto Alegre"

url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"

dados = requests.get(url).json()

if "main" in dados:
    temperatura = dados["main"]["temp"]
    print(f"Temperatura em {cidade}: {temperatura}°C")
else:
    print("Erro:")
    print(dados)'''

# Assistente de Voz para Windows
'''def create_save():
    global level, dinheiro
    level = 1 
    dinheiro = 0'''
def salvar_video():
    falar("Qual nome deseja salvar o vídeo?")
    comando = ouvir_comando().strip()
    if not comando:
        falar("Não entendi o nome do vídeo")
        return

    keyboard.press_and_release('ctrl + l')  # VAI PRO URL
    time.sleep(0.5)
    pg.hotkey('ctrl', 'c')
    time.sleep(0.5)
    texto = pyperclip.paste().strip()
    if not texto:
        falar("Não consegui copiar o URL")
        return

    with open(SAVE_NOMES_PATH, 'a', encoding='utf-8') as save_nome:
        save_nome.write(comando + '\n')

    with open(SAVE_VIDEOS_PATH, 'a', encoding='utf-8') as save_video:
        save_video.write(texto + '\n')

    falar('vídeo salvo')



    falar('senha salva')
def carregar_video():
    falar("Qual vídeo você deseja carregar?")
    video_nome = ouvir_comando().strip()
    print(f"Procurando vídeo: '{video_nome}'")

    if not video_nome:
        falar("Não entendi o nome do vídeo")
        return

    if os.path.exists(SAVE_NOMES_PATH) and os.path.exists(SAVE_VIDEOS_PATH):
        with open(SAVE_NOMES_PATH, 'r', encoding='utf-8') as nomes_file:
            nomes_linhas = [linha.rstrip('\n') for linha in nomes_file]

        with open(SAVE_VIDEOS_PATH, 'r', encoding='utf-8') as videos_file:
            videos_linhas = [linha.rstrip('\n') for linha in videos_file]

        nomes = [linha[5:].strip() if linha.lower().startswith('nome:') else linha.strip() for linha in nomes_linhas]
        urls = [linha[4:].strip() if linha.lower().startswith('url:') else linha.strip() for linha in videos_linhas]

        print(f"Nomes salvos: {nomes}")
        print(f"URLs salvas: {urls}")

        for idx, nome_salvo in enumerate(nomes):
            if video_nome.lower() in nome_salvo.lower():
                if idx < len(urls) and urls[idx]:
                    url = urls[idx]
                    print(f"Vídeo encontrado! Abrindo URL: {url}")
                    keyboard.press_and_release('ctrl + l')
                    time.sleep(0.5)
                    keyboard.write(url)
                    keyboard.press_and_release('enter')
                    falar(f"Vídeo {nome_salvo} carregado")
                    return
                break

        print("Vídeo não encontrado nos arquivos de save")
        falar("Vídeo não encontrado nos salvos")
    else:
        print("Arquivos de save não encontrados")
        falar("Arquivos de save não encontrados")



'''    else:
        create_save()'''


# =========================
# CONFIG
# =========================
tasks = ""
ex_mode = "normal"  # normal, youtube, 
mode = "normal"  # normal, narrador, tarefas
# =========================
# VOZ
# =========================
def falar(texto):
    try:
        tts = gTTS(texto, lang='pt')
        tts.save('voz.mp3')
        data, fs = sf.read('voz.mp3', dtype='int16')
        sd.play(data, fs)
        sd.wait()
    except:
        print("Erro ao falar.")

# =========================
# OUVIR COMANDO
# =========================
def ouvir_comando():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Diga o comando...")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                print("Nenhum som detectado.")
                return ""
            except KeyboardInterrupt:
                print("Interrompido pelo teclado durante a captura de áudio.")
                return ""
    except KeyboardInterrupt:
        print("Interrompido pelo teclado ao abrir o microfone.")
        return ""
    except Exception as e:
        print(f"Erro ao acessar o microfone: {e}")
        return ""

    try:
        comando = r.recognize_google(audio, language='pt-BR')
        print("Você disse:", comando)
        return comando.lower()
    except KeyboardInterrupt:
        print("Interrompido pelo teclado durante o reconhecimento.")
        return ""
    except Exception as e:
        print(f"Erro ao reconhecer: {e}")
        return ""

# =========================
# FUNÇÕES
# =========================
def click():
    pg.click()

def escrever():
    falar("O que deseja escrever?")
    texto = ouvir_comando()
    keyboard.write(texto)

def abrir():
    falar("O que deseja abrir?")
    app = ouvir_comando()
    keyboard.press_and_release('win')
    time.sleep(0.5)
    keyboard.write(app)
    time.sleep(1)
    keyboard.press_and_release('enter')
    falar(f"Abrindo {app}")

def exibir_hora():
    hora = datetime.datetime.now().strftime("%H:%M")
    falar(f"São {hora} agora")

def volume():
    falar("Aumentar, diminuir ou mutar?")
    cmd = ouvir_comando()

    if "diminuir" in cmd:
        for _ in range(5):
            keyboard.press_and_release('volume down')

    elif "aumentar" in cmd:
        for _ in range(5):
            keyboard.press_and_release('volume up')

    elif "mutar" in cmd:
        keyboard.press_and_release('volume mute')

# =========================
# NARRADOR / TELA
# =========================
def narrador():
    keyboard.press_and_release('win+ctrl+enter')

def ler_selecao():
    pg.hotkey('ctrl', 'c')
    time.sleep(0.5)
    texto = pyperclip.paste()

    if texto:
        falar(texto[:500])
    else:
        falar("Nada selecionado")

def janela_ativa():
    hwnd = win32gui.GetForegroundWindow()
    titulo = win32gui.GetWindowText(hwnd)

    if titulo:
        falar(f"Você está em {titulo}")
    else:
        falar("Não consegui identificar a janela")

def modo_ditar():
    falar("Modo ditar ativado. Pressione ESC para sair.")
    palavra_atual = ""
    frase_completa = ""

    while True:
        evento = keyboard.read_event()
        if evento.event_type != 'down':
            continue

        tecla = evento.name

        if tecla == 'esc':
            falar("Saindo do modo ditar")
            break

        if tecla == 'backspace':
            if palavra_atual:
                palavra_atual = palavra_atual[:-1]
                falar("Apagando")
            continue

        if tecla == 'space':
            if palavra_atual:
                frase_completa += palavra_atual + " "
                falar(palavra_atual)
                palavra_atual = ""
            continue

        if tecla in ('.', 'dot', 'period'):
            if palavra_atual:
                frase_completa += palavra_atual
                palavra_atual = ""
            if frase_completa.strip():
                falar(frase_completa.strip())
                frase_completa = ""
            continue

        if len(tecla) == 1 and tecla.isalpha():
            palavra_atual += tecla
            falar(tecla)
            continue

        # ignorar outras teclas no modo ditar

# =========================
# TAREFAS
# =========================
def adicionar_tarefa():
    global tasks
    falar("Qual tarefa deseja adicionar?")
    t = ouvir_comando()

    if t:
        tasks += t + "\n"
        falar("Tarefa adicionada")

def listar_tarefas():
    if tasks.strip():
        falar(tasks)
    else:
        falar("Você não tem tarefas")

def remover_tarefa():
    global tasks
    falar("Qual tarefa deseja remover?")
    t = ouvir_comando()

    if t in tasks:
        tasks = tasks.replace(t, "")
        falar("Tarefa removida")
    else:
        falar("Não encontrei essa tarefa")

# =========================
# PESQUISAR
# =========================
def pesquisar():
    falar("O que deseja pesquisar?")
    q = ouvir_comando()

    keyboard.press_and_release('win')
    time.sleep(0.5)
    keyboard.write("Opera GX")
    time.sleep(1)
    keyboard.press_and_release('enter')

    time.sleep(3)
    keyboard.write(q)
    keyboard.press_and_release('enter')


# =========================
# LOOP PRINCIPAL
# =========================
falar("Assistente iniciado")
print("Assistente rodando...")

 # MUDOU
while True: 
    #QUANDO ESCREVE, DITA A LETRA E QUANDO CLICA ESPAÇO, DIGITA A PALAVRA COMPLETA E QUANDO USA PONTO FINAL FALA A FRASE COMPLETA.
    
        

    comando = ouvir_comando()
    if mode == "normal":
        if not comando:
            continue

        elif "clicar" in comando or "clica" in comando or "pausa" in comando or "despausa" in comando:
            click()

        elif "hora" in comando:
            exibir_hora()

        elif "volume" in comando:
            volume()

        elif "abrir" in comando:
            abrir()

        elif "escreva" in comando:
            escrever()

        elif "pesquisar" in comando:
            pesquisar()
        elif "ler tudo" in comando or "ler tudo" in comando:
            keyboard.press_and_release('control + a')
            ler_selecao()
        elif "ler tela" in comando or "narrador" in comando:
            falar("Ativando narrador")
            narrador() 


        elif "ler seleção" in comando:
            ler_selecao()

        elif "onde estou" in comando:
            janela_ativa()

        elif "adicionar tarefa" in comando:
            adicionar_tarefa()

        elif "ver tarefas" in comando or "missões" in comando:
            listar_tarefas()
        elif "ditar" in comando:
            modo_ditar()
        elif "remover tarefa" in comando:
            remover_tarefa()
        elif "youtube" in comando:# modo youtube
            
            keyboard.press_and_release('win')
            time.sleep(0.5)
            keyboard.write("Opera GX")
            time.sleep(1)
            keyboard.press_and_release('enter')

            time.sleep(3)
            keyboard.write("youtube.com")
            keyboard.press_and_release('enter')
            ex_mode = mode
            mode = "youtube"
            falar("Você está na página inicial do YouTube")
            falar("Diga comandos para mais comandos relacionados ao YouTube, ou diga 'sair' para voltar ao modo normal")
        elif "sair" in comando or "parar" in comando:
            falar("Encerrando assistente")
            raise SystemExit
    elif mode == "youtube":
        
        
        if "comandos" in comando:
            falar("Comandos disponíveis: pesquisar, vídeos curtos, sair")
        elif "carregar vídeo" in comando:
            carregar_video()
        
        elif "pesquisar" in comando:
            falar("O que deseja pesquisar no YouTube?")
            q = ouvir_comando()
            keyboard.press_and_release('ctrl + l')
            time.sleep(0.5)
            keyboard.write("youtube.com/results?search_query=" + q.replace(" ", "+"))
            keyboard.press_and_release('enter')
            ex_mode = mode
            falar("entrando no modo seleção de vídeos")
            falar("Diga 'próximo' ou 'anterior' para navegar, e 'selecionar' para abrir o vídeo. Diga 'sair' para voltar ao modo normal")
            mode = "seleção"
            keyboard.press_and_release('ctrl + windows + enter')
        elif "curtos" in comando or "vídeos curtos" in comando or "shorts" in comando:
            keyboard.press_and_release('ctrl + l')
            time.sleep(0.5)
            keyboard.write("youtube.com/shorts")
            keyboard.press_and_release('enter')
            falar("Entrando no modo shorts")
            mode = "shorts"

        elif "sair" in comando or "parar" in comando:
            mode = "normal"
            falar("Voltando ao modo normal")
    elif mode == "seleção":
          # minimizar janela para facilitar navegação
        if "próximo" in comando:
            keyboard.press_and_release('tab')
        elif "comandos" in comando:
            falar("Comandos disponíveis: próximo, anterior, selecionar, sair")
        elif "anterior" in comando:
            keyboard.press_and_release('shift + tab')
        elif "selecionar" in comando:
            keyboard.press_and_release('enter')
            falar("Vídeo selecionado. entrando no modo vídeo")
            ex_mode = mode
            mode = "vídeo"
        elif "sair" in comando or "parar" in comando:
            keyboard.press_and_release('ctrl + windows + enter')
            if ex_mode == "youtube":
                mode = "youtube"
                falar("Voltando ao modo YouTube")
            elif ex_mode == "normal":
                mode = "normal"
                falar("Voltando ao modo normal")
    elif mode == "shorts":
        if "próximo" in comando:
            keyboard.press_and_release('down')  # seta para baixo
        elif "salvar vídeo" in comando:
            salvar_video()
        elif "comandos" in comando:
            falar("Comandos disponíveis: próximo, anterior, pause, salvar vídeo, sair")
        elif "anterior" in comando:
            keyboard.press_and_release('up')  # seta para cima
        elif "pause" in comando:
            keyboard.press_and_release('space')
        elif "sair" in comando or "parar" in comando:
            mode = "youtube"
            falar("Voltando ao modo YouTube")
    elif mode == "vídeo":
        if "pausar" in comando or "pause" in comando:
            keyboard.press_and_release('space')
        elif "comandos" in comando:
            falar("Comandos disponíveis: pausar, salvar vídeo, sair")
        elif "salvar vídeo" in comando:
            salvar_video()
        elif "sair" in comando or "parar" in comando:
            mode = "seleção"
            falar("Voltando ao modo seleção de vídeos") 
    #ADICIONAR TRADUÇÃO + modo vídeo com like, deslike, plkaylist, comentário
    #cuidado com modo narrador para não ter dois narradores ativos ao mesmo tempo
    #melhorar modo de pesquisa

    

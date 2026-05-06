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
    with sr.Microphone() as source:
        print("Diga o comando...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Nenhum som detectado.")
            return ""

    try:
        comando = r.recognize_google(audio, language='pt-BR')
        print("Você disse:", comando)
        return comando.lower()
    except:
        print("Erro ao reconhecer.")
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

while True:
    
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
        elif "comandos" in comando:
            falar("Comandos disponíveis: próximo, anterior, pause, sair")
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
            falar("Comandos disponíveis: pausar, sair")
        elif "sair" in comando or "parar" in comando:
            mode = "seleção"
            falar("Voltando ao modo seleção de vídeos") 
    #ADICIONAR TRADUÇÃO + modo vídeo com like, deslike, plkaylist, comentário
    #cuidado com modo narrador para não ter dois narradores ativos ao mesmo tempo
    #melhorar modo de pesquisa

    

import keyboard
import speech_recognition as sr
import pyautogui as pg
import time
import datetime
import pyttsx3
import pyperclip
import win32gui
import os
import requests




# CONFIGURAÇÕES DE CAMINHOS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_NOMES_PATH = os.path.join(BASE_DIR, 'save_nomes.txt')
SAVE_VIDEOS_PATH = os.path.join(BASE_DIR, 'save_videos.txt')

# =========================
# CONFIG
# =========================
tasks = ""
ex_mode = "normal"  # normal, youtube
mode = "normal"  # normal, narrador, tarefas, ditar, youtube, seleção, shorts, vídeo

# =========================
# VOZ - usando pyttsx3
# =========================
def falar(texto):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # velocidade de fala
        engine.say(texto)
        engine.runAndWait()
    except Exception as e:
        print(f"Erro ao falar: {e}")

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
# FUNÇÕES DE VÍDEO
# =========================
def salvar_video():
    falar("Qual nome deseja salvar o vídeo?")
    comando = ouvir_comando().strip()
    if not comando:
        falar("Não entendi o nome do vídeo")
        return

    keyboard.press_and_release('ctrl+l')  # VAI PRO URL
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

        nomes = [linha.strip() for linha in nomes_linhas]
        urls = [linha.strip() for linha in videos_linhas]

        print(f"Nomes salvos: {nomes}")
        print(f"URLs salvas: {urls}")

        for idx, nome_salvo in enumerate(nomes):
            if video_nome.lower() in nome_salvo.lower():
                if idx < len(urls) and urls[idx]:
                    url = urls[idx]
                    print(f"Vídeo encontrado! Abrindo URL: {url}")
                    keyboard.press_and_release('ctrl+l')
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

# =========================
# FUNÇÕES PRINCIPAIS
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

def pegar_clima(cidade): #PRECISA DE INTERNEt
    base_url = f"https://wttr.in/{cidade}?format=%C+%t"
    response = requests.get(base_url)

    if response.status_code == 200:
        return response.text.strip()
    else:
        return "Não foi possível pegar as informações. Verifique a cidade e a conexão."

# =========================
# LOOP PRINCIPAL
# =========================
falar("Assistente iniciado com pyttsx3")
print("Assistente rodando...")

while True:
    comando = ouvir_comando()
    if mode == "normal":
        if not comando:
            continue

        elif "clicar" in comando or "clica" in comando or "pausa" in comando or "despausa" in comando:
            click()
        elif "clima" in comando or "temperatura" in comando:
            falar("De qual cidade você quer saber o clima?")
            cidade = ouvir_comando()
            falar(pegar_clima(cidade))


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
        
        elif "ler tudo" in comando:
            keyboard.press_and_release('ctrl+a')
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
            falar("ATIVANDO MODO DITADO")
            mode = "ditar"
        
        elif "remover tarefa" in comando:
            remover_tarefa()
        
        elif "youtube" in comando:
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
            keyboard.press_and_release('ctrl+l')
            time.sleep(0.5)
            keyboard.write("youtube.com/results?search_query=" + q.replace(" ", "+"))
            keyboard.press_and_release('enter')
            ex_mode = mode
            falar("entrando no modo seleção de vídeos")
            falar("Diga 'próximo' ou 'anterior' para navegar, e 'selecionar' para abrir o vídeo. Diga 'sair' para voltar ao modo normal")
            mode = "seleção"
            keyboard.press_and_release('ctrl+windows+enter')
        
        elif "curtos" in comando or "vídeos curtos" in comando or "shorts" in comando:
            keyboard.press_and_release('ctrl+l')
            time.sleep(0.5)
            keyboard.write("youtube.com/shorts")
            keyboard.press_and_release('enter')
            falar("Entrando no modo shorts")
            mode = "shorts"

        elif "sair" in comando or "parar" in comando:
            mode = "normal"
            falar("Voltando ao modo normal")
    
    elif mode == "seleção":
        if "próximo" in comando:
            keyboard.press_and_release('tab')
        elif "comandos" in comando:
            falar("Comandos disponíveis: próximo, anterior, selecionar, sair")
        elif "anterior" in comando:
            keyboard.press_and_release('shift+tab')
        elif "selecionar" in comando:
            keyboard.press_and_release('enter')
            falar("Vídeo selecionado. entrando no modo vídeo")
            ex_mode = mode
            mode = "vídeo"
        elif "sair" in comando or "parar" in comando:
            keyboard.press_and_release('ctrl+windows+enter')
            if ex_mode == "youtube":
                mode = "youtube"
                falar("Voltando ao modo YouTube")
            elif ex_mode == "normal":
                mode = "normal"
                falar("Voltando ao modo normal")
    
    elif mode == "shorts":
        if "próximo" in comando:
            keyboard.press_and_release('down')
        elif "salvar vídeo" in comando:
            salvar_video()
        elif "comandos" in comando:
            falar("Comandos disponíveis: próximo, anterior, pause, salvar vídeo, sair")
        elif "anterior" in comando:
            keyboard.press_and_release('up')
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
    
    elif mode == "ditar":
        falar("Esc para sair do modo ditar")
        palavra_atual = ""
        frase_completa = ""
        
        while mode == "ditar":
            if keyboard.is_pressed('backspace'):
                palavra_atual = palavra_atual[:-1]
                falar("Apagando")
            elif keyboard.is_pressed('space'):
                falar(str(palavra_atual))
                palavra_atual = ""
                frase_completa += palavra_atual + " "
            elif keyboard.is_pressed('.'):
                falar(frase_completa)
                frase_completa = ""
            elif keyboard.is_pressed('A'):
                falar("A")
                palavra_atual += "A"
            elif keyboard.is_pressed('B'):
                falar("B")
                palavra_atual += "B"
            elif keyboard.is_pressed('C'):
                falar("C")
                palavra_atual += "C"
            elif keyboard.is_pressed('D'):
                falar("D")
                palavra_atual += "D"
            elif keyboard.is_pressed('E'):
                falar("E")
                palavra_atual += "E"
            elif keyboard.is_pressed('F'):
                falar("F")
                palavra_atual += "F"
            elif keyboard.is_pressed('G'):
                falar("G")
                palavra_atual += "G"
            elif keyboard.is_pressed('H'):
                falar("H")
                palavra_atual += "H"
            elif keyboard.is_pressed('I'):
                falar("I")
                palavra_atual += "I"
            elif keyboard.is_pressed('J'):
                falar("J")
                palavra_atual += "J"
            elif keyboard.is_pressed('K'):
                falar("K")
                palavra_atual += "K"
            elif keyboard.is_pressed('L'):
                falar("L")
                palavra_atual += "L"
            elif keyboard.is_pressed('M'):
                falar("M")
                palavra_atual += "M"
            elif keyboard.is_pressed('N'):
                falar("N")
                palavra_atual += "N"
            elif keyboard.is_pressed('O'):
                falar("O")
                palavra_atual += "O"
            elif keyboard.is_pressed('P'):
                falar("P")
                palavra_atual += "P"
            elif keyboard.is_pressed('Q'):
                falar("Q")
                palavra_atual += "Q"
            elif keyboard.is_pressed('R'):
                falar("R")
                palavra_atual += "R"
            elif keyboard.is_pressed('S'):
                falar("S")
                palavra_atual += "S"
            elif keyboard.is_pressed('T'):
                falar("T")
                palavra_atual += "T"
            elif keyboard.is_pressed('U'):
                falar("U")
                palavra_atual += "U"
            elif keyboard.is_pressed('V'):
                falar("V")
                palavra_atual += "V"
            elif keyboard.is_pressed('W'):
                falar("W")
                palavra_atual += "W"
            elif keyboard.is_pressed('X'):
                falar("X")
                palavra_atual += "X"
            elif keyboard.is_pressed('Y'):
                falar("Y")
                palavra_atual += "Y"
            elif keyboard.is_pressed('Z'):
                falar("Z")
                palavra_atual += "Z"
            elif keyboard.is_pressed('esc'):
                falar("Saindo do modo ditar")
                mode = "normal"


import keyboard, speech_recognition as sr, pyautogui as pg, time, datetime, sounddevice as sd, soundfile as sf
from gtts import gTTS





#modficável
tasks = ''
data_hora_atual = datetime.datetime.now()
hora_atual = datetime.datetime.now().strftime("%H")
email = ''
#não modficável
def narrador():
    keyboard.press_and_release('win+ctrl+enter')

def ouvir_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source: #AS VEZES PEGA O AUDIO DO EASE US
        print("Diga o comando (ex: 'clicar' , 'parar' ou 'pausa')...")
        audio = r.listen(source)
    try:
        comando = r.recognize_google(audio, language='pt-BR')
        print("Você disse:", comando)
        return comando.lower()
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
    except sr.RequestError:
        print("Erro no serviço de reconhecimento.")
    return ""

#
def task():
    b = gTTS(tasks, lang='pt')
    b.save('voz.mp3')
    filename = 'voz.mp3'
    data, fs = sf.read(filename, dtype='int16')
    sd.play(data, fs)

def printar():# printa a tela

    keyboard.press_and_release('win')

def falar(x):
    b = gTTS(x, lang='pt')
    b.save('voz.mp3')
    filename = 'voz.mp3'
    data, fs = sf.read(filename, dtype='int16')
    sd.play(data, fs)
    
def escreva():
    keyboard.write(ouvir_comando())

def abrir():
    a = ouvir_comando()
    keyboard.press_and_release('win')
    keyboard.write(a)
    for i in range(3):
        time.sleep(1)
        keyboard.press_and_release('enter')
    falar("Abrindo..." + a)
    
def exibir_lista_comandos():

    falar('C O M A N D O S\n'
    'Clica-(clicar,clica,pausa,despausa)\n'
    'Autoclick[pausa com h]-(auto,automático)\n'  
    'Abre o que disser-(abrir[algo no pc])\n' 
    'Escreva-(fale escreva, depois o que deseja escrever)\n' 
    'Missões(fala seus objetivos)\n'
    'Fim do código-(sair, parar)\n')
def click():
    pg.click()
def farm_automatica():
    pg.click()

def rap():
    #https://www.youtube.com/watch?v=Hn6D3K8rWfI&list=RDQQLIn91wE3o&index=2 - KUNIGAMI
    #https://youtube.com/playlist?list=PLSDHHB0zAFUZBxCSpmvqsb2219zDVp57P&si=6WVWqAWOLfokCcdu - Tuilist
    keyboard.press_and_release('win')
    keyboard.write('Opera GX')
    for i in range(3):
        time.sleep(1)
        keyboard.press_and_release('enter')
    keyboard.write('https://www.youtube.com/watch?v=Hn6D3K8rWfI&list=RDQQLIn91wE3o&index=2')
    keyboard.press_and_release('enter')

def volume():

    t = ouvir_comando()
    if "diminuir" in t or "abaixar" in t:
        for i in range(5):
            keyboard.press_and_release('volume down')
    elif "aumentar" in t or "subir" in t:
        for i in range(5):
            keyboard.press_and_release('volume up')
    elif "mutar" in t or "mudo" in t:
        keyboard.press_and_release('volume mute')
    


def pesquisar():
    keyboard.press_and_release('win')
    time.sleep(0.2)
    keyboard.write('Opera GX')
    for i in range(3):
        time.sleep(1)
        keyboard.press_and_release('enter')
    falar("O que deseja pesquisar?")
    keyboard.write(ouvir_comando())
    keyboard.press_and_release('enter') # TAB FAZ SELEÇÂO PARA BAIXO< SHIFT + TAB PARA CIMA

def exibir_hora():
    hora_atual = datetime.datetime.now().strftime("%H:%M")
    falar(f"São {hora_atual} agora.")


#colocar mais funções (Opcional)
# HORÁRIO E FALA OS TEMAS
#palavras-chave que iniciam as funções
falar("Esperando comando de voz...")
print("Esperando comando de voz...")
time.sleep(3)

while True:
    
    comando = ouvir_comando()

    if "clicar" in comando or "clica" in comando or "pausa" in comando or "despausa" in comando:

        click()
    elif "hora" in comando or "horas" in comando:
        exibir_hora()
    elif "volume" in comando:
        falar("O que deseja fazer com o volume? (aumentar, diminuir ou mutar)")
        time.sleep(3)
        volume()
    elif "adicionar tarefa" in comando or "adicionar tarefas" in comando:
        falar("Diga a tarefa que deseja adicionar.")
        time.sleep(3)
        a = ouvir_comando()
        falar(f"Deseja adicionar '{a}' a suas tarefas?")
        time.sleep(3)
        b = ouvir_comando()
        if "sim" in b:
            tasks += a + "\n"
            falar(f"Tarefa '{a}' adicionada.")
        else:
            falar("Tarefa não adicionada.")
    elif "tirar tarefa" in comando or "remover tarefa" in comando:
        falar("Diga a tarefa que deseja remover.")
        a = ouvir_comando()
        falar(f"Deseja remover '{a}' de suas tarefas?")
        b = ouvir_comando()
        if "sim" in b:
            for i in range(len(tasks)):
                if i in a:
                    tasks.delete(i)
        else:
            falar("Tarefa não removida.")

    elif "comandos" in comando or "comando" in comando:
        exibir_lista_comandos()
    elif "automático" in comando or "auto" in comando or keyboard.is_pressed('g'):
        falar('Iniciando modo automático. Pressione "h" para pausar.')
        while not keyboard.is_pressed('h') :
            farm_automatica()
        falar('Modo automático pausado.')
    elif "abrir" in comando or "Abrir" in comando:
        falar("O que deseja abrir?")
        abrir()

    elif "escreva" in comando:
        falar("O que deseja escrever?")
        escreva() 
    elif 'missões' in comando or 'missão' in comando or 'tarefas' in comando or 'tarefa' in comando:
        task()
    elif 'Rap' in comando or 'rap' in comando:
        rap()
    elif "parar" in comando or "sair" in comando:
        print("Encerrando script.")
        break
    elif "pesquisar" in comando:
        pesquisar()
    
    #ADICIONAR Matemática, Probabilidade e Estatística, modo narrador (windows + ctrl + enter)

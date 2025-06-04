from speech_to_text import voice_to_text
from read_response import answer
import time
import threading
import queue


#Entrée de la prononciation du nom
answer("S'il te plait, tu peux me prononcer aussi ton nom sans aucun autre mot ?")
time.sleep(3)
def ask_input_voice(q):
    name_voice = voice_to_text("voice_me") 
    q.put(name_voice)

q = queue.Queue()
thread = threading.Thread(target=ask_input_voice, args=(q,))
thread.start()

try:
    name_pron = q.get(timeout=60)
except queue.Empty:
    print("Temps écoulé ! Aucune réponse.")
    answer("Temps écoulé ! Aucune réponse.")
    name_pron = None

print("Nom prononcé :", name_pron)

time.sleep(3)

# Entrée de l'écriture du nom
answer("S'il te plait, tu peux m'écrire ton nom ?")

def ask_input(q):
    name = input("S'il te plait, tu peux m'écrire ton nom ? ")
    q.put(name)

q = queue.Queue()
thread = threading.Thread(target=ask_input, args=(q,))
thread.start()

try:
    name_script = q.get(timeout=60)
except queue.Empty:
    print("Temps écoulé ! Aucune réponse.")
    answer("Temps écoulé ! Aucune réponse.")
    name_script = None

print("Nom écrit :", name_script)




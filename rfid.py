import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep, time
import signal
import sys
import requests

# Configurações de hardware
GPIO.setmode(GPIO.BOARD)
BUZZER = 38

GPIO.setup(BUZZER, GPIO.OUT)

# Iniciando o leitor RFID
leitorRfid = SimpleMFRC522()

# URL da API (ajuste para o endereço correto do servidor)
URL_API = "http://localhost:5000"

# Funções para o buzzer
def tocar_buzzer(frequencia, duracao):
    p = GPIO.PWM(BUZZER, frequencia)
    p.start(50)  # Duty cycle de 50%
    sleep(duracao)
    p.stop()

def buzzer_leitura_feita():
    tocar_buzzer(500, 0.5)

def buzzer_erro():
    tocar_buzzer(200, 0.5)

def buzzer_sucesso():
    tocar_buzzer(1000, 0.5)

# Função para finalizar o programa
def finalizar_programa(signal, frame):
    print("\nFinalizando o programa...")
    GPIO.cleanup()
    sys.exit(0)

# Captura o sinal de interrupção (CTRL+C)
signal.signal(signal.SIGINT, finalizar_programa)

try:
    while True:
        print("Aguardando leitura da tag...")
        tag, nome = leitorRfid.read()  # Lê a tag e o nome associado
        print(f"ID do cartão: {tag}, Nome: {nome}")

        # Confirmação de leitura com o buzzer
        buzzer_leitura_feita()

        # Exemplo de decisão entre empréstimo ou devolução
        acao = input("Digite 'e' para empréstimo ou 'd' para devolução: ").strip().lower()

        if acao == 'e':
            # Chamada POST para registrar empréstimo
            response = requests.post(f"{URL_API}/emprestar", json={'aluno_id': tag, 'nome': nome})
        elif acao == 'd':
            # Chamada POST para registrar devolução
            response = requests.post(f"{URL_API}/devolver", json={'aluno_id': tag})
        else:
            print("Ação inválida. Tente novamente.")
            buzzer_erro()
            continue

        # Verifica a resposta da API
        if response.status_code == 200:
            print(response.json())
            buzzer_sucesso()  # Toca buzzer de sucesso
        else:
            print(f"Erro: {response.json().get('message', 'Erro desconhecido')}")
            buzzer_erro()  # Toca buzzer de erro

        sleep(1)

finally:
    GPIO.cleanup()
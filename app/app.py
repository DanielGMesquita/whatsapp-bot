import pywhatkit as pwk
import schedule
import time
import logging
import pyautogui

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../whatsapp_bot.log'),
        logging.StreamHandler()
    ]
)

CONTACTS = [
    "+5599999999999",
    "+5588888888888"
]

MESSAGE = "Esta é uma mensagem automática para lembrar você de descer com os cachorros e colocar comida para eles."

SEND_TIME = "07:50".strip()  # Horário de envio das mensagens (formato 24h)

# Função para focar a janela do WhatsApp Web (ajuste as coordenadas conforme sua tela)
def browser_focus():
    """
    Força o foco na janela do navegador (Ubuntu)
    """
    # Coordenadas aproximadas do campo de texto da mensagem
    x = 600
    y = 1050
    pyautogui.click(x, y)
    time.sleep(1)  # esperar foco

def send_whatsapp_message(phone_number):
    try:
        logging.info(f"Iniciando envio para {phone_number}")

        pwk.sendwhatmsg_instantly(phone_number, MESSAGE, wait_time=20, tab_close=False)
        time.sleep(2)
        browser_focus()
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'w')  # fecha aba
        time.sleep(2)

        logging.info(f"Mensagem enviada para {phone_number}")
        return True
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem para {phone_number}: {str(e)}")
        return False


def send_daily_messages():
    """
    Envia mensagens para todos os contatos da lista
    """
    logging.info("Iniciando envio de mensagens diárias...")

    for contact in CONTACTS:
        try:
            send_whatsapp_message(contact)
            # Aguarda 30 segundos entre cada envio para evitar spam
            time.sleep(30)
        except Exception as e:
            logging.error(f"Erro geral ao processar contato {contact}: {str(e)}")

    logging.info("Envio de mensagens diárias concluído!")


def main():
    """
    Função principal que agenda e executa a automação
    """
    print("🤖 Automação WhatsApp iniciada!")
    print("📱 Mensagens serão enviadas diariamente às 07:50")
    print("📝 Pressione Ctrl+C para parar a automação")

    # Agenda a execução diária às 07:50
    schedule.every().day.at(SEND_TIME).do(send_daily_messages)

    # Loop principal
    while True:
        try:
            # Verifica se há tarefas agendadas para executar
            schedule.run_pending()

            # Aguarda 1 minuto antes de verificar novamente
            time.sleep(60)

        except KeyboardInterrupt:
            print("\n🛑 Automação interrompida pelo usuário")
            logging.info("Automação interrompida pelo usuário")
            break
        except Exception as e:
            logging.error(f"Erro no loop principal: {str(e)}")
            time.sleep(60)  # Aguarda 1 minuto antes de tentar novamente

if __name__ == "__main__":
    main()
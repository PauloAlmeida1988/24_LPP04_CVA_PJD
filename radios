import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
import datetime
import os
import schedule
import time
import threading  # Importa a biblioteca threading

DATA_FILE = 'radio_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    print("Salvando dados...")
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print("Dados salvos com sucesso.")

def send_to_discord(message):
    webhook_url = "https://discord.com/api/webhooks/1283000077991804952/TiNOKt2Im2HgPS7_lCUVEBeWCJrrt6lq3aF9PrAnszyrr_b90F5mf14skgFwJYgNhm9X"  # Coloque seu Webhook aqui.
    data = {
        "content": message  # Mensagem que será enviada.
    }
    
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Mensagem enviada com sucesso para o Discord.")
        else:
            print(f"Erro ao enviar mensagem para o Discord: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ao Discord: {e}")

def get_radio_status(url, format_type='xml'):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if format_type == 'xml':
                listeners = extract_listeners_from_xml(response.text)
            elif format_type == 'html':
                listeners = extract_listeners_from_html(response.text)
            elif format_type == 'json':
                listeners = extract_listeners_from_json(response.text)
            else:
                print(f"Formato desconhecido para {url}.")
                return None
            
            if listeners is not None:
                return listeners
            else:
                print(f"Não foi possível extrair o número de ouvintes de {url}.")
                return None
        else:
            print(f"Erro ao conectar com {url}, código de status: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com {url}: {e}")
        return None

def extract_listeners_from_xml(xml_data):
    try:
        root = ET.fromstring(xml_data)
        current_listeners = root.find('CURRENTLISTENERS').text
        return int(current_listeners)
    except Exception as e:
        print(f"Erro ao processar XML: {e}")
        return None

def extract_listeners_from_html(html_data):
    try:
        soup = BeautifulSoup(html_data, 'html.parser')
        listeners_element = soup.find('td', string='Current Listeners:')
        if listeners_element:
            listeners = listeners_element.find_next_sibling('td').text.strip()
            return int(listeners)
        else:
            print("Elemento 'Current Listeners' não encontrado no HTML.")
            return None
    except Exception as e:
        print(f"Erro ao processar HTML: {e}")
        return None

def extract_listeners_from_json(json_data):
    try:
        data = json.loads(json_data)
        listeners = data.get('ouvintes')
        if listeners is not None:
            return int(listeners)
        else:
            print("Elemento 'ouvintes' não encontrado no JSON.")
            return None
    except Exception as e:
        print(f"Erro ao processar JSON: {e}")
        return None

def update_data():
    print("Atualizando dados...")
    radio_urls = [
        {"url": "https://s10.w3bserver.com/radio/8160/", "format": "html", "name": "Kihabbo"},
        {"url": "http://stream.truesecurity.com.br:8048/stats", "format": "xml", "name": "LightHabbo"},
        {"url": "http://painel.dedicado.stream:8036/stats", "format": "xml", "name": "Panela Dourada"},
        {"url": "http://stream1.svrdedicado.org:8530/stats", "format": "xml", "name": "Habblindados"},
        {"url": "https://sv13.hdradios.net:7770/stats", "format": "xml", "name": "HabboNight"},
        {"url": "https://www.raduckets.com.br/api/v1/status", "format": "json", "name": "Raduckets"},
    ]

    data = load_data()
    
    for radio in radio_urls:
        listeners = get_radio_status(radio['url'], format_type=radio['format'])
        if listeners is not None:
            name = radio['name']
            now = datetime.datetime.now()
            date_str = now.strftime('%Y-%m-%d')
            
            if name not in data:
                data[name] = {
                    'daily': {},
                    'weekly': {},
                    'monthly': {}
                }

            if date_str not in data[name]['daily']:
                data[name]['daily'][date_str] = []
            data[name]['daily'][date_str].append(listeners)

            if now.strftime('%Y-%U') not in data[name]['weekly']:
                data[name]['weekly'][now.strftime('%Y-%U')] = []
            data[name]['weekly'][now.strftime('%Y-%U')].append(listeners)

            if now.strftime('%Y-%m') not in data[name]['monthly']:
                data[name]['monthly'][now.strftime('%Y-%m')] = []
            data[name]['monthly'][now.strftime('%Y-%m')].append(listeners)

    save_data(data)

def calculate_averages():
    print("Calculando médias...")
    data = load_data()
    now = datetime.datetime.now()
    
    message = "Médias calculadas:\n"
    for radio, records in data.items():
        daily = records['daily']
        weekly = records['weekly']
        monthly = records['monthly']

        daily_avg = {k: sum(v)/len(v) for k, v in daily.items()}
        weekly_avg = {k: sum(v)/len(v) for k, v in weekly.items()}
        monthly_avg = {k: sum(v)/len(v) for k, v in monthly.items()}

        message += f"{radio} - Média Diária: {daily_avg}\n"
        message += f"{radio} - Média Semanal: {weekly_avg}\n"
        message += f"{radio} - Média Mensal: {monthly_avg}\n"

        print(f"{radio} - Média Diária: {daily_avg}")
        print(f"{radio} - Média Semanal: {weekly_avg}")
        print(f"{radio} - Média Mensal: {monthly_avg}")
    
    # Enviar a mensagem ao Discord
    send_to_discord(message)

def print_live_listeners():
    print("Imprimindo ouvintes ao vivo...")
    data = load_data()
    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    
    message = "Ouvintes ao vivo:\n"
    for radio, records in data.items():
        if date_str in records['daily']:
            listeners = records['daily'][date_str][-1]  # Pega o último registro do dia
            message += f"Rádio: {radio}, Ouvintes ao vivo: {listeners}\n"
    
    # Enviar a mensagem ao Discord
    send_to_discord(message)
    print(message)

def live_listener_task():
    print_live_listeners()

def daily_task():
    update_data()
    calculate_averages()

def schedule_tasks():
    schedule.every().minute.do(update_data)
    schedule.every().day.at("23:59").do(calculate_averages)
    schedule.every(60).seconds.do(live_listener_task)  # Atualiza a cada 30 segundos

    while True:
        schedule.run_pending()
        time.sleep(1)

def menu():
    while True:
        print("\nMenu:")
        print("1. Atualizar dados")
        print("2. Calcular médias")
        print("3. Imprimir ouvintes ao vivo")
        print("4. Sair")
        
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            update_data()
        elif choice == '2':
            calculate_averages()
        elif choice == '3':
            print_live_listeners()
        elif choice == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    print("Iniciando script...")

    # Inicia as tarefas agendadas em uma thread separada
    schedule_thread = threading.Thread(target=schedule_tasks)
    schedule_thread.daemon = True
    schedule_thread.start()

    # Executa o menu
    menu()

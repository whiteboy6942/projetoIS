import requests
import json

URL_IMPORTAR_JSON = "http://192.168.246.38:5000/importar/json"
URL_EXPORTAR_JSON = "http://192.168.246.38:5000/exportar/json"
URL_IMPORTAR_XML = "http://192.168.246.38:5000/importar/xml"
URL_EXPORTAR_XML = "http://192.168.246.38:5000/exportar/xml"

# === IMPORTAR JSON LOCAL PARA O SERVIDOR ===
def importar_json():
    try:
        with open("produtos.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
        resposta = requests.post(URL_IMPORTAR_JSON, json=dados)
        print("Importar JSON:", resposta.text)
    except Exception as e:
        print("Erro ao importar JSON:", e)

# === EXPORTAR JSON DO SERVIDOR PARA FICHEIRO LOCAL ===
def exportar_json():
    try:
        resposta = requests.get(URL_EXPORTAR_JSON)
        if resposta.status_code == 200:
            with open("produtos_backup.json", "w", encoding="utf-8") as f:
                json.dump(resposta.json(), f, ensure_ascii=False, indent=2)
            print("Exportar JSON: dados guardados em 'produtos_backup.json'")
        else:
            print("Erro ao exportar JSON:", resposta.status_code)
    except Exception as e:
        print("Erro ao exportar JSON:", e)

# === IMPORTAR XML LOCAL PARA O SERVIDOR ===
def importar_xml():
    try:
        with open("produtos.xml", "r", encoding="utf-8") as f:
            conteudo = f.read()
        headers = {"Content-Type": "application/xml"}
        resposta = requests.post(URL_IMPORTAR_XML, data=conteudo, headers=headers)
        print("Importar XML:", resposta.text)
    except Exception as e:
        print("Erro ao importar XML:", e)

# === EXPORTAR XML DO SERVIDOR PARA FICHEIRO LOCAL ===
def exportar_xml():
    try:
        resposta = requests.get(URL_EXPORTAR_XML)
        if resposta.status_code == 200:
            with open("produtos_backup.xml", "w", encoding="utf-8") as f:
                f.write(resposta.text)
            print("Exportar XML: dados guardados em 'produtos_backup.xml'")
        else:
            print("Erro ao exportar XML:", resposta.status_code)
    except Exception as e:
        print("Erro ao exportar XML:", e)

# === MENU INTERATIVO ===
def menu():
    while True:
        print("\n=== CLIENTE IMPORT/EXPORT ===")
        print("1. Importar JSON para o servidor")
        print("2. Exportar JSON do servidor para ficheiro")
        print("3. Importar XML para o servidor")
        print("4. Exportar XML do servidor para ficheiro")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            importar_json()
        elif opcao == "2":
            exportar_json()
        elif opcao == "3":
            importar_xml()
        elif opcao == "4":
            exportar_xml()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()

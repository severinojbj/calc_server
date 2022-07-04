'''
Created on 14 de abr de 2021

Faculdade Alpha
Curso de Tecnologia em Análise e Desenvolvimento de Sistemas
Disciplina: Sistemas Distribuidos
@author: Severino José (severino.jose@alpha.edu.br)

calc_server: 

Um servidor de calculo vetorial, integrante de uma aplicacao distribuida.
A parte complementar do sistema, correspondente a dois processos, serao
desenvolvidos pelos aludos da referida disciplina.
A comunicacao entre o servidor e os processos eh feita atraves do protocolo MQTT,
usando o broker mosquitto.
No servidor, ha rotinas de geracao dos vetores a serem calculados, 
alem das operacoes a serem feitas em cada membro desse vetor.
Cada processo cliente deve receber um vetor correspondente e sua operacao unária.
Assim que o processo recebe e realiza a operacao em cada membro de seu vetor, o
resultado é somado (caso seja Processo A) ou subtraido (caso seja Processo B)
com o resultado do outro processo. 
O servidor entao aguarda as respostas de soma e diferenca entre os vetores,
para exibir os reultados recebidos e esperados.
Mais detalhes de especificacao estão no slide do Projeto.

Como executar o calc_server:

- Caso não tenha interpretador python, instale-o em sua máquina
- Instale também a biblioteca paho.mqtt, através do gerenciador pip (no terminal):
    pip install paho.mqtt
- Caso o comando não esteja disponível, adicione ele no path do sistema 
(geralmente ele fica na pasta do Python, no Windows)
- Certifique-se que o broker mosquitto está instalado e executando
- Execute o servidor para que possa interagir com os processos:
    python calc_server.py

'''

import paho.mqtt.client as mqtt
import random

MQTT_URL = "localhost"
MQTT_PORT = 1883

#Estados
INICIO = 1
ESPERA_RESULTADO_1 = 2
ESPERA_RESULTADO_2 = 3

lista_operacoes = ["+", "-", "*", "/", "^"]
lista_topicos = ["novaOperacao","vetorA","operacaoA","vetorB","operacaoB","soma","diferenca"]
lista_inscricao = ["novaOperacao", "soma", "diferenca"]

class VetorException (Exception):
    def __init__ (self, topico, valor):
        self.topico = topico
        self.valor = valor        
    def print_detail (self):
        print ("Vetor recebido em " + str(self.topico) + " esta fora do formato aceito: " + str (self.valor [1:]))
        print ("Exemplo de formato aceito: " + '\'[1,2,3]\'')
        print ("Reiniciando e aguardando novo inicio...\n")

class Servidor ():
    
    estadoAtual = 0
    vetA = list()
    vetB = list()
    vetSomaRec = list()
    vetSubRec = list()
    opA = ""
    opB = ""
    
    def __init__ (self):
        self.estadoAtual = INICIO
    
    def gerar_vetor (self, tamanho):
        listRet = list()
        for i in range (tamanho):
            num = random.randint(0, 20)
            listRet.append (num)
        return listRet
    
    def gerar_operacao (self):
        operacao = lista_operacoes [random.randint(0, len(lista_operacoes) - 1)]
        num = random.randint (1, 5)
        opNum = operacao + str(num)
        return opNum
    
    def aplicar_operacao_1_num (self, n, operacao, operando):
        res = n
        if (operacao == "+"):
            res = res + operando
        elif (operacao == "-"):
            res = res - operando
        elif (operacao == "*"):
            res = res * operando
        elif (operacao == "/"):
            res = res / operando
        elif (operacao == "^"):
            res = res ** operando
        return res
    
    def aplicar_operacao_1_vetor (self, operacao, vetor):
        oprRecebida = operacao [0]
        numRecebido = int(operacao [1:])
        vetorRet = list() 
        for i in range (len(vetor)):
            vetorRet.append (self.aplicar_operacao_1_num (vetor[i], oprRecebida, numRecebido))
        return vetorRet
    
    def soma_vetores (self, vetorA, vetorB):
        vetorC = list()
        for i in range(len(vetorA)):
            vetorC.append(vetorA [i] + vetorB [i])
        return vetorC
    
    def subtracao_vetores (self, vetorA, vetorB):
        vetorC = list()
        for i in range(len(vetorA)):
            vetorC.append(vetorA [i] - vetorB [i])
        return vetorC
    
    def converter_string_para_vetor (self, topico, vetorStr):
        try: 
            stringNum = vetorStr [3:-2]
            listString = stringNum.split(",")
            listNum = []
            for n in listString:
                listNum.append (int(n))
            return listNum
        except:
            raise VetorException (topico, vetorStr)
    
    def calcular_e_comparar (self):
        vetAProc = self.aplicar_operacao_1_vetor(self.opA, self.vetA)
        vetBProc = self.aplicar_operacao_1_vetor(self.opB, self.vetB)
        vetSoma = self.soma_vetores(vetAProc, vetBProc)
        vetSub = self.subtracao_vetores(vetAProc, vetBProc)
        print ("Fim do processamento")
        print ("Vetor esperado de soma:\n" + str(vetSoma))
        print ("Vetor recebido de soma:\n" + str(self.vetSomaRec))
        print ("Vetor esperado de diferenca:\n" + str(vetSub))
        print ("Vetor recebido de diferenca:\n" + str(self.vetSubRec))
        print ("Reiniciando e aguardando novo inicio...\n")
        pass 
    
    def processar_protocolo (self, cliente_mqtt, topico, mensagem):
        if (self.estadoAtual == INICIO):
            if (topico == "novaOperacao"):
                tamanho = random.randint(5, 30)
                self.vetA = self.gerar_vetor (tamanho)
                self.vetB = self.gerar_vetor (tamanho)
                self.opA = self.gerar_operacao ()
                self.opB = self.gerar_operacao ()
                cliente_mqtt.publish("vetorA", str(self.vetA))
                cliente_mqtt.publish("vetorB", str(self.vetB)) 
                cliente_mqtt.publish("operacaoA", self.opA)
                cliente_mqtt.publish("operacaoB", self.opB)  
                print ("VetorA, VetorB, OperacaoA, OperacaoB enviados.")
                self.estadoAtual = ESPERA_RESULTADO_1
            else:
                self.estadoAtual = INICIO
        elif (self.estadoAtual  == ESPERA_RESULTADO_1):
            if (topico == "soma"):
                try:
                    self.vetSomaRec = self.converter_string_para_vetor(topico, mensagem)
                    print ("Vetor soma recebido. Aguardando o vetor diferenca...")
                    self.estadoAtual = ESPERA_RESULTADO_2
                except VetorException as e:
                    e.print_detail()
                    self.estadoAtual = INICIO
            elif (topico == "diferenca"):
                try:
                    self.vetSubRec = self.converter_string_para_vetor(topico, mensagem)            
                    print ("Vetor diferenca recebido. Aguardando o vetor soma...")
                    self.estadoAtual = ESPERA_RESULTADO_2
                except VetorException as e:
                    e.print_detail()
                    self.estadoAtual = INICIO
            else:
                self.estadoAtual = ESPERA_RESULTADO_1
        elif (self.estadoAtual  == ESPERA_RESULTADO_2):
            if (topico == "soma"):
                try: 
                    self.vetSomaRec = self.converter_string_para_vetor(topico, mensagem)
                    self.calcular_e_comparar()
                except VetorException as e:
                    e.print_detail()         
                self.estadoAtual = INICIO       
            elif (topico == "diferenca"):
                try:
                    self.vetSubRec = self.converter_string_para_vetor(topico, mensagem)       
                    self.calcular_e_comparar()    
                except VetorException as e:
                    e.print_detail()
                self.estadoAtual = INICIO
            else:
                self.estadoAtual = ESPERA_RESULTADO_2  
        else:
            self.estadoAtual = INICIO
        pass
    
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        for topico in lista_inscricao:
            client.subscribe (topico)
        print ("Aguardando sinal de inicio...")
            
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg): 
        #print(msg.topic+" "+str(msg.payload))
        self.processar_protocolo (client, msg.topic, str(msg.payload))

if __name__ == "__main__":
    servidor = Servidor ()
    clienteMqtt = mqtt.Client()
    clienteMqtt.on_connect = servidor.on_connect
    clienteMqtt.on_message = servidor.on_message    
    clienteMqtt.connect(MQTT_URL, MQTT_PORT, 60)
    try:
        clienteMqtt.loop_forever()
    except KeyboardInterrupt:
        print ("Fechando Servidor...")

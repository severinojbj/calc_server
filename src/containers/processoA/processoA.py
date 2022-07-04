'''
Created on 5 de mai de 2021
Faculdade Alpha
Curso de Tecnologia em Análise e Desenvolvimento de Sistemas
Disciplina: Sistemas Distribuidos
@author: Severino José (severino.jose@alpha.edu.br)

'''

import paho.mqtt.client as mqtt
from utils import Utils

MQTT_URL = "mqtt"
MQTT_PORT = 1883

#Estados
INICIO = 1
RECEBER_2_TOPICO = 2
ESPERA_RESULTADO_B = 3

lista_operacoes = ["+", "-", "*", "/", "^"]
lista_topicos = ["vetorA","operacaoA","vetorProcB"]
#lista_topicos_server = ["novaOperacao","vetorA","operacaoA","vetorB","operacaoB","soma","diferenca"]

class ProcessoA ():
    estadoAtual = None
    vetorA = None
    vetorB = None
    vetorC = None
    operacaoA = None
    utils = None
    
    def __init__ (self):
        self.estadoAtual = INICIO
        self.vetorA = []
        self.vetorA = []
        self.vetorC = []
        self.operacaoA = ""
        self.utils = Utils()
        pass    
        
    def processar_protocolo (self, client, topico, mensagem):
        if (self.estadoAtual == INICIO):
            if (topico == "vetorA"):
                self.vetorA = self.utils.converter_string_para_vetor(mensagem)
                self.estadoAtual = RECEBER_2_TOPICO 
            elif (topico == "operacaoA"):
                self.operacaoA = mensagem
                self.estadoAtual = RECEBER_2_TOPICO      
            else:
                self.estadoAtual = INICIO            
        elif (self.estadoAtual == RECEBER_2_TOPICO):
            if (topico == "operacaoA"):
                self.operacaoA = mensagem
                self.vetorA = self.utils.aplicar_operacao_1_vetor (self.operacaoA, self.vetorA)
                client.publish ("vetorProcA", self.utils.converter_vetor_para_string(self.vetorA))
                self.estadoAtual = ESPERA_RESULTADO_B
            elif (topico == "vetorA"):
                self.vetorA = self.utils.converter_string_para_vetor(mensagem)
                self.vetorA = self.utils.aplicar_operacao_1_vetor (self.operacaoA, self.vetorA)                
                client.publish ("vetorProcA", self.utils.converter_vetor_para_string(self.vetorA))
                self.estadoAtual = ESPERA_RESULTADO_B  
            else:          
                self.estadoAtual = RECEBER_2_TOPICO
        
        if (self.estadoAtual == ESPERA_RESULTADO_B):    
            if (topico == "vetorProcB"):
                # self.vetorA = self.aplicar_operacao_1_vetor (self.operacaoA, self.vetorA)
                self.vetorB = self.utils.converter_string_para_vetor(mensagem)
                self.vetorC = self.utils.soma_vetores(self.vetorA, self.vetorB)
                client.publish ("soma", self.utils.converter_vetor_para_string(self.vetorC))
            else:
                self.estadoAtual = ESPERA_RESULTADO_B
        pass
    
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        for topico in lista_topicos:
            client.subscribe (topico) 
        client.publish ("novaOperacao", "start")           
        
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg): 
        #print(msg.topic+" "+str(msg.payload))
        self.processar_protocolo (client, msg.topic, str(msg.payload))

if __name__ == "__main__":
    processo = ProcessoA ()
    clienteMqtt = mqtt.Client()
    clienteMqtt.on_connect = processo.on_connect
    clienteMqtt.on_message = processo.on_message    
    clienteMqtt.connect(MQTT_URL, MQTT_PORT, 60)
    try:
        clienteMqtt.loop_forever()
    except KeyboardInterrupt:
        print ("Fechando Processo...")
        
        
        
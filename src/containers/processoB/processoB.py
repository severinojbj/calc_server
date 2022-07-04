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
ESPERA_RESULTADO_A = 3

lista_operacoes = ["+", "-", "*", "/", "^"]
lista_topicos = ["vetorB","operacaoB","vetorProcA"]
#lista_topicos_server = ["novaOperacao","vetorA","operacaoA","vetorB","operacaoB","soma","diferenca"]

class ProcessoB ():
    estadoAtual = None
    vetorA = None
    vetorB = None
    vetorC = None
    operacaoB = None
    utils = None
    
    def __init__ (self):
        self.estadoAtual = INICIO
        self.vetorA = []
        self.vetorB = []
        self.vetorC = []
        self.operacaoB = ""
        self.utils = Utils()
        pass 
        
    def processar_protocolo (self, client, topico, mensagem):
        if (self.estadoAtual == INICIO):
            if (topico == "vetorB"):
                self.vetorB = self.utils.converter_string_para_vetor(mensagem)
                self.estadoAtual = RECEBER_2_TOPICO 
            elif (topico == "operacaoB"):
                self.operacaoB = mensagem
                self.estadoAtual = RECEBER_2_TOPICO      
            else:
                self.estadoAtual = INICIO            
        elif (self.estadoAtual == RECEBER_2_TOPICO):
            if (topico == "operacaoB"):
                self.operacaoB = mensagem
                self.vetorB = self.utils.aplicar_operacao_1_vetor (self.operacaoB, self.vetorB)
                client.publish ("vetorProcB", self.utils.converter_vetor_para_string(self.vetorB))
                self.estadoAtual = ESPERA_RESULTADO_A
            elif (topico == "vetorB"):
                self.vetorB = self.utils.converter_string_para_vetor(mensagem)
                self.vetorB = self.utils.aplicar_operacao_1_vetor (self.operacaoB, self.vetorB)                
                client.publish ("vetorProcB", self.utils.converter_vetor_para_string(self.vetorB))
                self.estadoAtual = ESPERA_RESULTADO_A  
            else:          
                self.estadoAtual = RECEBER_2_TOPICO
        
        if (self.estadoAtual == ESPERA_RESULTADO_A):    
            if (topico == "vetorProcA"):
                self.vetorA = self.utils.converter_string_para_vetor(mensagem)
                self.vetorC = self.utils.subtracao_vetores(self.vetorA, self.vetorB)
                client.publish ("diferenca", self.utils.converter_vetor_para_string(self.vetorC))
            else:
                self.estadoAtual = ESPERA_RESULTADO_A
        pass
    
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        for topico in lista_topicos:
            client.subscribe (topico)  
                    
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg): 
        #print(msg.topic+" "+str(msg.payload))
        self.processar_protocolo (client, msg.topic, str(msg.payload))

if __name__ == "__main__":
    processo = ProcessoB ()
    clienteMqtt = mqtt.Client()
    clienteMqtt.on_connect = processo.on_connect
    clienteMqtt.on_message = processo.on_message    
    clienteMqtt.connect(MQTT_URL, MQTT_PORT, 60)
    try:
        clienteMqtt.loop_forever()
    except KeyboardInterrupt:
        print ("Fechando Processo...")
        
        
        
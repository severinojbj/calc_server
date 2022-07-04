'''
Created on 6 de mai de 2021

@author: sjbj
'''

class Utils ():
        
    def __init__ (self):
        pass
    
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
        oprRecebida = operacao [2]
        numRecebido = int(operacao [3:-1])
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
    
    def converter_string_para_vetor (self, vetorStr):
        stringNum = vetorStr [3:-2]
        listString = stringNum.split(",") 
        listNum = []
        for n in listString:
            listNum.append (int(n))
        return listNum
            
    def converter_vetor_para_string (self, vetorInt):
        listStr = "["
        for n in vetorInt:
            listStr = listStr + (str (n)) + ","
        listStr = listStr[:-1] + "]"
        return str(listStr)
        
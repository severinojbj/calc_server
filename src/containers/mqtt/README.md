#MQTT Broker (mosquitto)

## Construção do container

Para construir uma imagem do broker mosquitto, certifique-se que o docker esteja
devidamente instalado e o console na pasta do Dockerfile. Execute o comando:

* docker

  ```sh
  docker build -t mqtt .
  ```

## Execução do container

Para executar, o comando deve incluir a porta do broker:

* docker

  ```sh
  docker run -p 1883:1883 mqtt
  ```
  
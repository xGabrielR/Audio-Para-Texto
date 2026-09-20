Primeiro construa a imagem que esta na pasta `./spark-image`, basta entrar na pasta e com o comando `docker build -t my-spark:4.0.2 .` você vai construir a imagem do spark.

Após isso, basta voltar ao diretório raiz das pastas e escrever `docker-compose up` para subir o cluster.

Para submeter aplicações para serem executadas, basta escrveer o comando:

```sh
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 --deploy-mode client  --conf spark.executor.instances=2  /tmp/spark-jobs/main.py
```

Spark Master URL: http://localhost:8085/
Spark History Server URL: http://localhost:18080/


**Bônus: Jupyter Notebook no topo do driver**.

Para isso, existem algumas formas.

A primeira é você instalar dentro do driver o Jupyter Notebook, dessa forma você vai poder submeter as aplicações direto pelo notebook.
Para isso, basta seguir o passo a passo:

1. Acesse o container do spark master com o comando `docker exec -it  CONTAINER_ID_DO_SPARK_MASTER /bin/bash`.
2. Instale a biblioteca do py4j e do jupyterlab, disponíveis no diretório `spark-jupyter-notebook` no arquivo requirements.txt utilizando o proprio pip install dentro do container que você acabou de acessar.
3. Agora basta iniciar o jupyterlab com o comando: `jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root`.
4. O notebook `notebook_no_driver.ipynb` contem como inicializar o spark e também alguns comandos para testar a ferramenta.

Você consegue verificar o seu notebook conectado dentro do Spark Master e também os seus jobs no Spark History Server.



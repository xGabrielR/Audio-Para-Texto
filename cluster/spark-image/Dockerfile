FROM maven:3.8.3-openjdk-17 AS mvn-build
WORKDIR /usr/src/spark/

COPY ./pom.xml .
RUN mvn clean dependency:copy-dependencies

FROM spark:4.0.2 AS spark
USER root
# Python 3.10.12
# Scala: 2.13.16

RUN mkdir /opt/spark/conf
RUN touch /opt/spark/conf/hadoop-metrics2-s3a-file-system.properties

RUN mkdir /opt/spark/logs
RUN mkdir /opt/spark/logs/events

#COPY ./main_iceberg.py /tmp/main_iceberg.py
#COPY ./main_delta.py /tmp/main_delta.py

COPY --from=mvn-build /usr/src/spark/lib/* /opt/spark/jars/
COPY spark-defaults.conf /opt/spark/conf

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN chmod u+x /opt/spark/sbin/* && chmod u+x /opt/spark/bin/*
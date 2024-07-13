FROM redhat/ubi8
RUN mkdir -p /opt/hadoop/ && mkdir -p /opt/spark/

RUN yum -y install wget procps rsync curl sudo openssh-clients java-1.8.0-openjdk python3
RUN wget https://downloads.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3-scala2.13.tgz
RUN tar xvf spark-3.5.1-bin-hadoop3-scala2.13.tgz --directory /opt/spark/ --strip-components 1
RUN rm -rf spark*hadoop3-scala2.13.tgz

RUN chmod u+x /opt/spark/bin/
RUN chmod u+x /opt/spark/sbin/

ENV SPARK_HOME=/opt/spark
ENV HADOOP_HOME=/opt/hadoop

WORKDIR $SPARK_HOME

COPY spark-defaults.conf "$SPARK_HOME/conf"
RUN yum -y install hostname
RUN EXPORT SPARK_MASTER_HOST = `hostname`

ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin:$HADOOP_HOME
ENV PYSPARK_PYTHON=/usr/bin/python3
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_PORT=7077
ENV SPARK_WORKER_WEBUI_PORT=8080
ENV SPARK_MASTER_WEBUI_PORT=8080
EXPOSE 7077 8080
ENTRYPOINT ["start-master.sh","-p","7077"]
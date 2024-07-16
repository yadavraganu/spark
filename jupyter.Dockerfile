FROM redhat/ubi8
RUN mkdir -p /opt/hadoop/
ENV HADOOP_HOME=/opt/hadoop
RUN yum -y install python3.8 curl java-1.8.0-openjdk
RUN curl https://bootstrap.pypa.io/pip/3.6/get-pip.py -o get-pip.py
RUN python3 get-pip.py
WORKDIR $HADOOP_HOME
COPY requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT ["jupyter","notebook","--allow-root","--no-browser","--port=8888", "--ip=0.0.0.0","--NotebookApp.token=''","--NotebookApp.password=''"]
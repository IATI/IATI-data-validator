FROM openjdk:8-jdk-slim

LABEL maintainer="Rolf Kleef <rolf@drostan.org>" \
  description="IATI Data Validator Engine" \
  repository="https://github.com/data4development/IATI-data-validator"

ENV ANT_VERSION    1.10.1
ENV SAXON_VERSION  9.8.0-14
ENV WEBHOOK_VERSION 2.6.8

ENV HOME /home
ENV ANT_HOME /opt/ant
ENV SAXON_HOME /opt/ant

WORKDIR $HOME

RUN apt-get update && \
  apt-get -y install --no-install-recommends wget libxml2-utils curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN wget -q http://archive.apache.org/dist/ant/binaries/apache-ant-${ANT_VERSION}-bin.tar.gz && \
  tar -xzf apache-ant-${ANT_VERSION}-bin.tar.gz && \
  rm apache-ant-${ANT_VERSION}-bin.tar.gz && \
  mv apache-ant-${ANT_VERSION} ${ANT_HOME}

RUN wget -q http://central.maven.org/maven2/net/sf/saxon/Saxon-HE/${SAXON_VERSION}/Saxon-HE-${SAXON_VERSION}.jar && \
  mv *.jar ${ANT_HOME}/lib

RUN wget -q https://github.com/adnanh/webhook/releases/download/${WEBHOOK_VERSION}/webhook-linux-amd64.tar.gz && \
  tar -xzf webhook-linux-amd64.tar.gz --strip 1 && \
  rm webhook-linux-amd64.tar.gz

ENV PATH $PATH:$ANT_HOME/bin

COPY . $HOME
VOLUME /workspace

#ENTRYPOINT ["/opt/ant/bin/ant", "-e"]
#CMD ["-p"]
EXPOSE 9000
ENTRYPOINT ["/home/webhook"]
CMD ["-urlprefix=process", "-hooks=/home/webhook-scripts/hooks.json", "-hotreload", "-verbose"]
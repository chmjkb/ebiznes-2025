FROM ubuntu:22.04

# As python <= 3.12 is deprecated we have to update apt repositories to have a way to install 3.10
# for further details visit: https://gist.github.com/rutcreate/c0041e842f858ceb455b748809763ddb
RUN apt update && \
    apt install software-properties-common -y && \
    apt install curl -y

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt update

RUN apt install python3.10 python3.10-venv python3.10-dev -y

# Installing jdk-8 
RUN apt install openjdk-8-jdk -y 
RUN apt install unzip zip -y 

# Installing sdkman for easy gradle & kotlin setup
RUN curl -s "https://get.sdkman.io" | bash
RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && \
             sdk install kotlin && \
             sdk install gradle"

ENV PATH="~/.sdkman/candidates/gradle/current/bin:$PATH"

# Install gradle dependencies
RUN apt install sqlite3

# Copy the app and run it
WORKDIR /app
COPY . .
CMD ["/bin/bash", "-c", "gradle", "run"]

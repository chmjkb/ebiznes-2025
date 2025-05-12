FROM ubuntu:22.04

RUN apt update && \
    apt install curl -y

# Installing jdk-8 
RUN apt install openjdk-8-jdk -y 
RUN apt install unzip zip -y 

# Installing sdkman for easy gradle & kotlin setup
RUN curl -s "https://get.sdkman.io" | bash
RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && \
             sdk install kotlin && \
             sdk install gradle"

ENV PATH="~/.sdkman/candidates/gradle/current/bin:$PATH"

# Copy the app and run it
WORKDIR /app
COPY . .
CMD ["./gradlew", "run"]

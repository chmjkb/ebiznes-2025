FROM ubuntu:22.04

WORKDIR /app

COPY ./app /app

# Install required packages and Scala with sbt
RUN apt-get update && apt-get install -y curl zip unzip bash && \
    curl -s "https://get.sdkman.io" | bash && \
    bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && \
    sdk install java 11.0.20-tem && \
    sdk install scala && \
    sdk install sbt"

# Set environment variables for SDKMAN
ENV SDKMAN_DIR="/root/.sdkman"
ENV PATH="${SDKMAN_DIR}/bin:${SDKMAN_DIR}/candidates/java/current/bin:${SDKMAN_DIR}/candidates/scala/current/bin:${SDKMAN_DIR}/candidates/sbt/current/bin:${PATH}"

EXPOSE 9000

ENTRYPOINT ["/bin/bash", "-c", "source $SDKMAN_DIR/bin/sdkman-init.sh && sbt run"]

FROM node:23-alpine

COPY . /frontend

WORKDIR /frontend

RUN yarn 

EXPOSE 3000

ENTRYPOINT [ "yarn", "dev", "--host", "0.0.0.0", "--port", "3000"]
FROM node:18-alpine

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install

COPY . .

EXPOSE 3000

CMD ["yarn", "dev", "--host", "0.0.0.0"]
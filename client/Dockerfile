#  Dockerfile to build the client application using node 24

FROM node:24-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

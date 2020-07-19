FROM node:alpine AS build
WORKDIR /app
ADD package.json .
RUN npm install
ADD . .
RUN npm run build

FROM alpine:latest
WORKDIR /app/server
RUN apk update
RUN apk add nginx
RUN apk add gcc
RUN apk add libc-dev 
RUN apk add linux-headers
RUN apk add python3-dev
RUN apk add py-pip
ADD api/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install wheel
RUN pip3 install -r requirements.txt --src /usr/local/src
COPY api .
COPY nginx.conf /etc/nginx
RUN addgroup -S www && adduser -S www-data -G www
RUN chmod +x /app/server/startup.sh
COPY --from=build /app/dist /app/dist
CMD ["./startup.sh"]

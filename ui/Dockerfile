FROM node:7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install dependencies
COPY package.json /usr/src/app/
RUN npm install && npm cache clean

COPY . /usr/src/app/

ENTRYPOINT ["npm"]
CMD ["run", "build"]

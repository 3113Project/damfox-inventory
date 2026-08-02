FROM node:22-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
EXPOSE 5173
HEALTHCHECK --interval=5s --timeout=3s --start-period=10s --retries=12 CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1:5173/"]
CMD ["npm", "run", "dev"]

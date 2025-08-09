FROM node:20-alpine
WORKDIR /app

ENV NODE_ENV=production
ENV NPM_CONFIG_FETCH_TIMEOUT=120 NPM_CONFIG_FETCH_RETRIES=5

COPY package*.json ./
RUN npm ci --omit=dev || npm install --omit=dev --legacy-peer-deps

COPY . .
EXPOSE 3000
CMD ["npm","start"]

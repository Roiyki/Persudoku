# Use an appropriate base image for your frontend. Assuming a simple static site.
FROM node:14-alpine as build

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the application code and build
COPY . .
RUN npm run build

# Serve the frontend using a simple server like serve
FROM node:14-alpine
RUN npm install -g serve
COPY --from=build /app/build /app
EXPOSE 5000
CMD ["serve", "-s", "/app", "-l", "5000"]

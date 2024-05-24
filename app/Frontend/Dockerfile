# Use an appropriate base image for serving static files
FROM nginx:alpine as production-stage

# Copy static files from the templates directory to the Nginx HTML directory
COPY ./templates /usr/share/nginx/html

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the port Nginx will run on
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]

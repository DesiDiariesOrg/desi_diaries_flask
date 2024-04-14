# Use an official Nginx image as a parent image
FROM nginx:latest

# Copy the Nginx configuration file from the host into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]

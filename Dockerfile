# Use official Node image
FROM node:18

# Create app directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN npm install

# Expose port (change if your app uses a different one)
EXPOSE 3000

# Run the app
CMD ["npm", "start"]

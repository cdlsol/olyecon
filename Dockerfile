#Python Image
FROM python:3.12.3

#Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY python /app/python
COPY olympicsdata.ddb /app/olympicsdata.ddb
COPY olympics-economics.csv /app/olympics-economics.csv

# Expose port for Shiny dashboard 
#EXPOSE 8080
EXPOSE 40331

# Define the command to run app 
CMD ["python", "/app/python/app.py"]
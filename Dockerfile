#Python Image
FROM python:3.12.3

#Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


#Run Virtual Environment
RUN python -m venv /env
ENV VIRTUAL_ENV=/env
ENV PATH="/env/bin:$PATH"
ENV SHINY_PORT=40331


# Copy the rest of the project files
COPY python /app/python
COPY python /app/pipe 
COPY olympicsdata.ddb /app/olympicsdata.ddb
COPY olympics-economics.csv /app/olympics-economics.csv

# Expose port for Shiny dashboard 
#EXPOSE 8080
EXPOSE 40331

# Define the command to run app 
# CMD ["python", "app.py"]
CMD ["shiny", "run", "--host", "0.0.0.0", "--port", "40331", "/app/python/app.py"]

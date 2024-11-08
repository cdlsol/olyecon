FROM python:3.12.3

#Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Create and activate virtual environment, then install dependencies
RUN python -m venv /env
ENV VIRTUAL_ENV=/env
ENV PATH="/env/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY python /app/python
COPY python /app/pipe.py
COPY olympicsdata.ddb /app/olympicsdata.ddb
COPY olympics-economics.csv /app/olympics-economics.csv

# Set environment variable for Shiny Express port
ENV SHINY_PORT=35603

# Expose port for Shiny dashboard 
# EXPOSE 40331
EXPOSE 35603


# Define the command to run app 
# CMD ["python", "/app/python/app.py"]
# CMD ["python", "app.py"]
CMD ["python", "-m", "shiny", "run", "--host", "0.0.0.0", "--port", "35603", "--reload", "/app/python/app.py"]

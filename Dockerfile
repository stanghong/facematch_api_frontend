# Use the official Python image from the Docker Hub
FROM python:3.9.6

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies, including streamlit
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Create a user and switch to it to run the application
RUN useradd -m appuser
RUN chown -R appuser /tmp /code

USER appuser

# Set the default command to run the app using Streamlit
CMD ["streamlit", "run", "streamlit.py", "--server.port=8000", "--server.address=0.0.0.0"]

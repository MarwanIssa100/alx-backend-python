FROM python:3.10
WORKDIR /app

# Install the application dependencies
COPY Requirements.txt ./
RUN pip install --no-cache-dir -r Requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 8000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
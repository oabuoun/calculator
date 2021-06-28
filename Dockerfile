FROM python:3
COPY calculator /calculator
COPY requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "calculator/main.py"]

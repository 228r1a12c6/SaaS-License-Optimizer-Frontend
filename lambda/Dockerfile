FROM public.ecr.aws/lambda/python:3.12

# Copy function code and model into the container
COPY app.py model.pkl requirements.txt ./

# Install required Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set the Lambda function handler
CMD ["app.lambda_handler"]

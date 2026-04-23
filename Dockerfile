# WORKDIR -> the current working directory inside the container.
# I don't need to set the full path! My WORKDIR is like cd, enter in the folder and stay there.

FROM python:3.12

WORKDIR /usr/local/code

COPY ./requirements.txt ./
# Pass the requirements.txt to the folder we the app we using. 

COPY . .
# Copy current directory to WORKDIR

RUN pip install --no-cache-dir --upgrade -r /usr/local/code/requirements.txt
# I can't do `./` here, because the pip have to know the file he needs to read.
# no-cache-dir -> tells pip to not save the downloaded packages locally. Only related to pip!
# upgrade -> updgrade packages if they already installed

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
# Execute the code will run in the CMD.

# Flask CL results

Create Python virtual env:

Linux
```
python -m virtualenv env
```
Windows
```
python -m venv env
```

Activate vritual env:

Linux

```
source env/bin/activate
```
Windows

```
env/scripts/activate
```

Install requirements.txt
```
pip install -r requirements.txt
```

Run on Linux:
```
export FLASK_APP=app.py
flask run
```
Run on Windows with PS:
```
$env:FLASK_APP = "app.py"
flask run
```

Run tests:
```
python -m unittest discover
```

Docker:
Build docker image:
```
docker build --tag=[image_name] .
```
Run docker container on port 5000 (docker container expose port 5000):
```
docker run -p 5000:5000 [image_name]
```

App runs on localhost:5000

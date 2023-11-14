checkout ollama from: https://github.com/jmorganca/ollama.git

copy Dockerfile.gpu and em_german_modelfile into base folder


> docker build -t ollama:latest -f ./Dockerfile.gpu .
> docker tag ollama:latest 728986473007.dkr.ecr.us-east-1.amazonaws.com/onecx/ollama:0.1.9-gpu

> docker push 728986473007.dkr.ecr.us-east-1.amazonaws.com/onecx/ollama:0.1.9-gpu
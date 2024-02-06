# create two ebs volumes and update pv.yaml´s -> volumeID if no volume exists already: 
# ollama
aws ec2 create-volume --availability-zone us-east-1a --size 200
# qdrant
aws ec2 create-volume --availability-zone us-east-1a --size 10


# take volume id and set it in pv.yaml files of llama2 and qdrant

# install storage-class
kubectl apply -f storageclass.yaml


# enable GPU based workload - for version update check https://github.com/NVIDIA/k8s-device-plugin/releases

# kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.2/nvidia-device-plugin.yml

helm repo add nvdp https://nvidia.github.io/k8s-device-plugin
helm repo update
# gpu slicing config

kubectl apply -f nvidia-device-plugin.yaml

helm upgrade -i nvdp nvdp/nvidia-device-plugin \
  --namespace kube-system \
  -f nvdp-values.yaml \
  --version 0.14.3 \
  --set config.name=nvidia-device-plugin \
  --force





#install ollama
helm upgrade --install --force ollama -n genai --create-namespace ./ollama

#install qdrant
helm upgrade --install --force qdrant -n genai --create-namespace ./qdrant

#install onecx-ai-svc
helm upgrade --install --force onecx-ai-svc -n genai --create-namespace ./onecx-ai-svc

#install onecx-ai-ui
helm upgrade --install --force onecx-ai-ui -n genai --create-namespace ./onecx-ai-ui


#check connection
http://llama2.one-cx.org:8000/

http://qdrant.one-cx.org:6333/

http://chat-svc.one-cx.org/

http://chat-ui.one-cx.org/

#update scale up and down lambdas with cluster policy
add policy "genai-dev-admin-policy" to 
https://us-east-1.console.aws.amazon.com/iamv2/home#/roles/details/genaiScaleUp-role-6zjp1ufz?section=permissions
https://us-east-1.console.aws.amazon.com/iamv2/home#/roles/details/genaiScaleDown-role-rzktzgl7?section=permissions

#set right clusterName in code of both (genaiScaleUp and genaiScaleDown Lambdas) -> see aws/lambda/lambda_function_scale_up / lambda_function_scale_down


#set permission to access s3 bucket for document embedding
add AmazonS3ReadOnlyAccess (or AmazonS3FullAccess) and AmazonRoute53FullAccess to genai-dev-eks-nodegroup-role role


#optional install metrics to use kubectl top node/pod
>kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml



#check gpu utilization
connect to node instance and run
> nvidia-smi

# running a gpu job to check kubernetes configuration
https://github.com/NVIDIA/k8s-device-plugin#running-gpu-jobs






# Scaling up and down the infrastructure

api gateway uses basic_authorizer lambda for basic authentication

https://00xng0wt39.execute-api.us-east-1.amazonaws.com/dev/genaiScaleUp
 
 
The server is getting  automatically scaled down at 15:50 and 17:50 every day or with manually with the following url
https://00xng0wt39.execute-api.us-east-1.amazonaws.com/dev/genaiScaleDown
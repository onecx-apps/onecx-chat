#create two ebs volumes and update pv.yaml´s -> volumeID if no volume exists already: 
#llama2
aws ec2 create-volume --availability-zone us-east-1a --size 24
#qdrant
aws ec2 create-volume --availability-zone us-east-1a --size 10


#take volume id and set it in pv.yaml files of llama2 and qdrant

#install storage-class
kubectl apply -f storageclass.yaml

#enable GPU based workload - for version update check https://github.com/NVIDIA/k8s-device-plugin/releases
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.2/nvidia-device-plugin.yml


#install llama2
helm upgrade --install --force ollama -n genai --create-namespace ./ollama
or 
helm upgrade --install --force llama2 -n genai --create-namespace ./llama2



#install qdrant
helm upgrade --install --force qdrant -n genai --create-namespace ./qdrant

#install onecx-chat-svc
helm upgrade --install --force onecx-chat-svc -n genai --create-namespace ./onecx-chat-svc

#install onecx-chat-ui
helm upgrade --install --force onecx-chat-ui -n genai --create-namespace ./onecx-chat-ui

#update route 53 to loadbalancers 
https://us-east-1.console.aws.amazon.com/route53/v2/hostedzones#ListRecordSets/Z04691503R1QKP3NPCK74


#check connection
http://llama2.one-cx.org:8000/

http://qdrant.one-cx.org:6333/

http://chat-svc.one-cx.org/

http://chat-ui.one-cx.org/

#update scale up and down lambdas with cluster policy
add policy "genai-dev-admin-policy" to 
https://us-east-1.console.aws.amazon.com/iamv2/home#/roles/details/genaiScaleUp-role-6zjp1ufz?section=permissions
https://us-east-1.console.aws.amazon.com/iamv2/home#/roles/details/genaiScaleDown-role-rzktzgl7?section=permissions


#set permission to access s3 bucket for document embedding
add AmazonS3ReadOnlyAccess (or AmazonS3FullAccess) to genai-dev-eks-nodegroup-role role



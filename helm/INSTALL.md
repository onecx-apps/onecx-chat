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


#install ollama
helm upgrade --install --force ollama -n genai --create-namespace ./ollama

#install qdrant
helm upgrade --install --force qdrant -n genai --create-namespace ./qdrant

#install onecx-chat-svc
helm upgrade --install --force onecx-chat-svc -n genai --create-namespace ./onecx-chat-svc

#install onecx-chat-ui
helm upgrade --install --force onecx-chat-ui -n genai --create-namespace ./onecx-chat-ui


#update route 53 to loadbalancers for qdrant and ollama if required
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

#set right clusterName in code of both (genaiScaleUp and genaiScaleDown Lambdas)


#set permission to access s3 bucket for document embedding
add AmazonS3ReadOnlyAccess (or AmazonS3FullAccess) and AmazonRoute53FullAccess to genai-dev-eks-nodegroup-role role


#optional install metrics to use kubectl top node/pod
>kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml



#check gpu utilization
connect to node instance and run
> nvidia-smi

# running a gpu job to check kubernetes configuration
https://github.com/NVIDIA/k8s-device-plugin#running-gpu-jobs


# in case nvidia container toolkit needs to be installed only!
#option install  nvidia-container-toolkit for gpu support not required
#sudo yum-config-manager --disable amzn2-nvidia
#sudo yum remove -y libnvidia-container-1.4.0-1.amzn2.x86_64

#curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo | \
#  sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo

#sudo yum install -y nvidia-container-toolkit
#???sudo yum-config-manager --enable amzn2-nvidia????

#sudo nvidia-ctk runtime configure --runtime=containerd
#sudo systemctl restart containerd



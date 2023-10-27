#create two ebs volumes and update pv.yaml´s -> volumeID: 
#llama2
aws ec2 create-volume --availability-zone us-east-1a --size 24
#qdrant
aws ec2 create-volume --availability-zone us-east-1a --size 10


#install storage-class
kubectl apply -f storageclass.yaml

#install llama2
helm install llama2 -n genai ./llama2

#install qdrant
helm install qdrant -n genai ./qdrant


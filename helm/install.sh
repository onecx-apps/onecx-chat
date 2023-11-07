#create two ebs volumes and update pv.yaml´s -> volumeID: 
#llama2
aws ec2 create-volume --availability-zone us-east-1a --size 24
#qdrant
aws ec2 create-volume --availability-zone us-east-1a --size 10


#take volume id and set it in pv.yaml files of llama2 and qdrant

#install storage-class
kubectl apply -f storageclass.yaml

#install llama2
helm install llama2 -n genai --create-namespace ./llama2

#install qdrant
helm install qdrant -n genai --create-namespace ./qdrant

#update route 53 to loadbalancers 

#check connection
http://llama2.one-cx.org:8000/

http://qdrant.one-cx.org:6333/

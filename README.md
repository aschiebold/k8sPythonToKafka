# k8sPythonToKafka

docker build -t python-kafka-app:latest .

kubectl apply -f kafka-zookeeper.yaml

kubectl apply -f python-app.yaml

kubectl exec -it $(kubectl get pods -l app=kafka -o jsonpath="{.items[0].metadata.name}") -- kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

kubectl exec -it $(kubectl get pods -l app=python-app -o jsonpath="{.items[0].metadata.name}") -- bash

kubectl delete -f python-app.yaml
kubectl delete -f kafka-zookeeper.yaml

TAG=greenlytics/ai4eu:model-0.4
docker buildx build --platform=linux/amd64 -t $TAG .
docker push $TAG
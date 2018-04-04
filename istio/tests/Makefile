tag = gcr.io/nginsako/bookinfo_testing:latest

build:
	docker build --build-arg KUBE_VERSION="v1.9.4"  --build-arg NGINMESH_VERSION="0.6.0"  --build-arg WRK_VERSION="3.1.0" -t $(tag) -f src/Dockerfile .
	gcloud docker -- push $(tag)

gpush:
	gcloud docker -- push $(tag)

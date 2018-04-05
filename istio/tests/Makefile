KUBE_VERSION=v1.9.4
NGINMESH_VERSION=0.6.0
WRK_VERSION=3.1.0
GIT_COMMIT=$(shell git rev-parse --short HEAD)
TEST_IMAGE_NAME=bookinfo_testing
REPO=gcr.io/$(GCLOUD_PROJECT)
TAG=-$(NGINMESH_VERSION)-$(GIT_COMMIT)
TAG_LATEST=$(NGINMESH_VERSION)
DOCKER_PUSH = gcloud docker -- push

build:
	docker build --build-arg KUBE_VERSION=$(KUBE_VERSION)  --build-arg NGINMESH_VERSION=$(NGINMESH_VERSION)  --build-arg WRK_VERSION=$(WRK_VERSION) -t $(REPO)/$(TEST_IMAGE_NAME):$(TAG_LATEST) -f src/Dockerfile .

build-clean:
	docker build --no-cache --build-arg KUBE_VERSION=$(KUBE_VERSION)  --build-arg NGINMESH_VERSION=$(NGINMESH_VERSION)  --build-arg WRK_VERSION=$(WRK_VERSION) -t $(REPO)/$(TEST_IMAGE_NAME):$(TAG_LATEST) -f src/Dockerfile .

push-gcp:
	$(DOCKER_PUSH)  $(REPO)/$(TEST_IMAGE_NAME):$(TAG_LATEST)

clean-docker:
	docker rmi $(REPO)/$(TEST_IMAGE_NAME):$(TAG_LATEST)

clean-gcp:
	gcloud container images delete $(REPO)/$(TEST_IMAGE_NAME):$(TAG_LATEST) --force-delete-tags




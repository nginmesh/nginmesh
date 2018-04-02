tag = gcr.io/nginsako/bookinfo_test:latest

build:
	docker build -t $(tag) .
	gcloud docker -- push $(tag)

gpush:
	gcloud docker -- push $(tag)

VERSION=TEST-RELEASE
REPO=nginmesh
USER=nginmesh


update-install:
	./updateVersion.sh


release:	create_release

clean_release:  rm -rf target

release_tar:    clean_release
	mkdir -p target
	cp -r samples target
            

create_release:
	github-release release \
    --user ${USER} \
    --repo ${REPO} \
    --tag ${VERSION} \
    --name "${VERSION}" \
    --pre-release



delete_release:
	github-release delete \
    --user ${USER} \
    --repo ${REPO} \
    --tag ${VERSION}

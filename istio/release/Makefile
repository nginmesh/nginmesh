VERSION=TEST-RELEASE
REPO=nginmesh
USER=nginmesh


update-install:
	./updateVersion.sh

release:	create_release

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

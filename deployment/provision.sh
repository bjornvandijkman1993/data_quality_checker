#usage: bash deployment/provision.sh
cd app
eb init -r eu-west-3 -p docker capstone
eb create -s develop

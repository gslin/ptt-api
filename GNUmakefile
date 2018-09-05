#
APPLICATION_NAME?=	ptt-api
AWS_PROFILE?=		default
AWS_REGION?=		us-east-1
S3_BUCKET?=		"gslin-codedeploy-us-east-1-${APPLICATION_NAME}"

#
.DEFAULT_GOAL:=		test
.PHONY:			push test

#
push:
	git push -v origin master

test:
	rm -f .coverage
	nosetests --cover-package ptt_api --no-byte-compile --with-coverage

-include codedeploy-makefile/codedeploy.gnumakefile

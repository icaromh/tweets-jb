setup:
	pip install -r requirements.txt

run:
	python -m tweetsjb

docker-build:
	docker build -t tweetsjb .

docker-run:
	docker run --rm -d \
	-v `pwd`/data:/app/data \
	--name jbsync
	tweetsjb

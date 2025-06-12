build:
	docker build -t gogostats_app .
run:
	docker run -d -p 80:3001 --name gogostats_app gogostats_app
restart:
	docker stop gogostats_app
	docker rm gogostats_app
	docker run -d -p 80:3001 --name gogostats_app gogostats_app	
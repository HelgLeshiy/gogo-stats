build:
	docker build -t gogostats_app .
run:
	docker run -d -p 3040:3040 --name gogostats_app gogostats_app
restart:
	docker stop gogostats_app
	docker rm gogostats_app
	docker run -d -p 3040:3040 --name gogostats_app gogostats_app	
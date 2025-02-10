start_project:
	cd ./meltano && docker build -t meltano .
	cd ./Airflow && docker-compose up -d

run_project:
	cd ./Airflow && docker-compose up -d

stop_project:
	cd ./Airflow && docker-compose down

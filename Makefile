.PHONY: run

run:
	docker-compose run --rm object_fit_images python main.py ${dir}
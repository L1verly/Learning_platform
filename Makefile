up:
	docker compose -f docker-compose-local.yaml up -d

down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force

up_ci:
	docker compose -f docker-compose-ci.yaml up -d

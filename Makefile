# Global variables
APP_NAME = better_ais
APP_PATH = ./better_ais
APP_VERSION = 0.0.1
APP_DOCKER_FILE = ./ci/build/Dockerfile
APP_DOCKER_IMAGE = better-ais
APP_DOTENV_FILE = './ci/build/.env'

DATE = $(shell date "+%Y-%m-%d %H:%M:%S")
COMMIT_SHA = $(shell git rev-parse HEAD)
BRANCH = $(shell git rev-parse --abbrev-ref HEAD)

DOCKER_COMPOSE_FILE = ./ci/build/docker-compose.yml
DOCKER_COMPOSE_ARGS = -f $(DOCKER_COMPOSE_FILE) --env-file $(APP_DOTENV_FILE)

# COLORED OUTPUT XD
ccinfo 	= $(shell tput setaf 6)
ccwarn 	= $(shell tput setaf 3)
ccerror = $(shell tput setaf 1)
ccok 	= $(shell tput setaf 2)
ccreset = $(shell tput sgr0)
INFO 	= $(ccinfo)[INFO] |$(ccreset)
WARN 	= $(ccwarn)[WARN] |$(ccreset)
ERROR 	= $(ccerror)[ERROR]|$(ccreset)
OK 		= $(ccok)[OK]   |$(ccreset)



clean:
	@echo "${INFO} Cleaning..."
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -exec rm -rf {} \;
	@rm -rf build
	@rm -rf dist
	
	@echo "${OK} Cleaned! (removed .pyc, __pycache__, build, dist)"

db_up:
	@echo "${INFO} Running database..."
	@docker-compose $(DOCKER_COMPOSE_ARGS) up -d db
	@echo "${OK} Database running!"

app_gen_build_info:
	@echo "${INFO} Generating build info..."

	@echo "# AUTOGENERATED FILE. DO NOT EDIT!"			> $(APP_PATH)/__build_info__.py
	@echo "" 								 		   >> $(APP_PATH)/__build_info__.py
	@echo "__version__ = \"$(APP_VERSION)\"" 		   >> $(APP_PATH)/__build_info__.py
	@echo "__built_at__ = \"$(DATE)\"" 		 		   >> $(APP_PATH)/__build_info__.py
	@echo "__commit_sha__ = \"$(COMMIT_SHA)\""	  	   >> $(APP_PATH)/__build_info__.py
	@echo "__branch__ = \"$(BRANCH)\"" 		 		   >> $(APP_PATH)/__build_info__.py
	@echo "${OK} Build info generated!"


app_build: clean
	@echo "${INFO} Building app..."

	@echo "${INFO} Building docker image $(APP_DOCKER_IMAGE):$(APP_VERSION)..."
	@docker build -t $(APP_DOCKER_IMAGE) -f $(APP_DOCKER_FILE) .
	@echo "${OK} Docker image $(APP_DOCKER_IMAGE):$(APP_VERSION) built!"

app_up:
	@echo "${INFO} Running app..."
	@docker-compose $(DOCKER_COMPOSE_ARGS) up -d $(APP_NAME)
	@echo "${OK} App running!"

app_stop:
	@echo "${INFO} Stopping app..."
	@docker-compose $(DOCKER_COMPOSE_ARGS) stop $(APP_NAME)
	@echo "${OK} App stopped!"

app_logs:
	@echo "${INFO} Showing app logs..."
	@docker-compose $(DOCKER_COMPOSE_ARGS) logs -f $(APP_NAME)

app_all: app_build app_up app_logs

app_down:
	@read -p "Are you sure you want to remove all containers? [y/N] " -n 1 -r; echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "${INFO} Removing all containers..."; \
		docker-compose $(DOCKER_COMPOSE_ARGS) down; \
		echo "${OK} All containers removed!"; \
	else \
		echo "${WARN} Aborted!"; \
	fi

cluster_up:
	@echo "${INFO} Running cluster..."
	@docker-compose $(DOCKER_COMPOSE_ARGS) up -d
	@echo "${OK} Cluster running!"

cluster_stop:
	@echo "${INFO} Stopping cluster..."
	@docker-compose $(DOCKER_COMPOSE_ARGS) stop
	@echo "${OK} Cluster stopped!"

cluster_logs:
	@echo "${INFO} Showing cluster logs..."
	@docker-compose $(DOCKER_COMPOSE_ARGS) logs -f

cluster_all: cluster_up cluster_logs
help:
	@echo
	@echo
	@echo "  ----------------------------------------------------------------"
	@echo "  CBOE Pitch Upload Makefile"
	@echo "  ----------------------------------------------------------------"
	@echo "  demo      Build the development Docker images and run containers"
	@echo
	@echo

demo:
	docker-compose up --build -d

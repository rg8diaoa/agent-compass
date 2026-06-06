# agent-compass Makefile

.PHONY: init audit check-naming todo-api-test todo-api-run

PROJECT ?= .

init:
	@bash scripts/init.sh $(PROJECT)

audit:
	python scripts/audit.py templates/

check-naming:
	python scripts/check-naming.py templates/

todo-api-test:
	cd examples/todo-api && pip install -r requirements.txt -q && pytest tests/ -v

todo-api-run:
	cd examples/todo-api && uvicorn src.main:app --reload

all: check-naming audit
	@echo "✅ 全部检查通过"


dev:
	# Create virtualenv
	python3.10 -m venv .venv --upgrade-deps
	# Install requirements
	.venv/bin/pip3 install -r requirements.txt

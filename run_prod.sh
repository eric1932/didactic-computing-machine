if [[ -f ./venv/bin/activate ]]; then
  source ./venv/bin/activate
fi
uvicorn main:app --host 0.0.0.0 --port 8888
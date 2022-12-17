# Flask Async POC

Probar cuanto se la banca Flask con su _async_

Inspiración: https://youtu.be/0KU67snMjtQ?t=922

## Requisitos

-   [Poetry](https://python-poetry.org/docs/)
-   [https://github.com/rakyll/hey](https://github.com/rakyll/hey) o Apache Benchmark

## Pruebas

-   Flask 2.2.2 [async]
    -   gunicorn 20.1.0
    -   gunicorn - 1 worker[sync] - https://docs.gunicorn.org/en/stable/design.html#sync-workers
    -   gunicorn - 4 workers[gevent] - https://docs.gunicorn.org/en/stable/design.html#async-workers
    -   gunicorn - 4 workers[uvicorn]
-   Quart 0.18.3
    -   hypercorn - 1 worker
    -   hypercorn - 4 workers
    -   hypercorn - 1 worker[uvloop]

## Setup

```bash
poetry install

poetry shell
```

## Pruebas

```bash
# Servir app en :8000 con 1 worker
gunicorn app:app
[2022-12-17 04:45:44 -0300] [8579] [INFO] Starting gunicorn 20.1.0
[2022-12-17 04:45:44 -0300] [8579] [INFO] Listening at: http://127.0.0.1:8000 (8579)
[2022-12-17 04:45:44 -0300] [8579] [INFO] Using worker: sync
[2022-12-17 04:45:44 -0300] [8580] [INFO] Booting worker with pid: 8580

# 10 requests con 5 clientes concurrentes (2 requests c/u)
hey -n 10 -c 5 http://localhost:8000

  Total:        2.5331 secs
  Slowest:      1.2664 secs
  Fastest:      0.2550 secs
  Average:      1.0131 secs
  Requests/sec: 3.9477 # 1 worker atiende aprox 4 req/sec (0.25s cada una)


# Duplicamos cant de requests y clientes
hey -n 20 -c 10 http://localhost:8000

Summary:
  Total:        5.0720 secs # Se duplica la duración
  Slowest:      2.5363 secs
  Fastest:      0.2543 secs
  Average:      1.9652 secs
  Requests/sec: 3.9432 # Capacidad del server es la misma


hey -n 50 -c 10 http://localhost:8000

Summary:
  Total:        12.6760 secs
  Slowest:      2.5411 secs
  Fastest:      0.2595 secs
  Average:      2.3071 secs
  Requests/sec: 3.9445 # Same

```

### Gunicorn con 4 workers

```bash
gunicorn --workers=4 app:app
[2022-12-17 04:45:09 -0300] [8415] [INFO] Starting gunicorn 20.1.0
[2022-12-17 04:45:09 -0300] [8415] [INFO] Listening at: http://127.0.0.1:8000 (8415)
[2022-12-17 04:45:09 -0300] [8415] [INFO] Using worker: sync
[2022-12-17 04:45:09 -0300] [8417] [INFO] Booting worker with pid: 8417
[2022-12-17 04:45:09 -0300] [8418] [INFO] Booting worker with pid: 8418
[2022-12-17 04:45:09 -0300] [8419] [INFO] Booting worker with pid: 8419
[2022-12-17 04:45:09 -0300] [8420] [INFO] Booting worker with pid: 8420

# 50 requests con 10 clientes concurrentes (5 requests c/u)
hey -n 50 -c 10 http://localhost:8000

Summary:
  Total:        3.3011 secs
  Slowest:      0.7626 secs
  Fastest:      0.2556 secs
  Average:      0.5891 secs
  Requests/sec: 15.1464 # Cada worker responde 4 req/sec
```

### Gunicorn - 4 workers - 2 threads

-   Cada worker tiene 2 threads
-   La cantidad máxima de requests debiera ser 8 (workers \* threads)
-   La cantidad sugerida por gunicorn es (2\*CPU) + 1

```bash
gunicorn --workers=4 --threads=2 app:app
[2022-12-17 04:43:03 -0300] [8121] [INFO] Starting gunicorn 20.1.0
[2022-12-17 04:43:03 -0300] [8121] [INFO] Listening at: http://127.0.0.1:8000 (8121)
[2022-12-17 04:43:03 -0300] [8121] [INFO] Using worker: gthread
[2022-12-17 04:43:03 -0300] [8122] [INFO] Booting worker with pid: 8122
[2022-12-17 04:43:03 -0300] [8123] [INFO] Booting worker with pid: 8123
[2022-12-17 04:43:03 -0300] [8124] [INFO] Booting worker with pid: 8124
[2022-12-17 04:43:03 -0300] [8125] [INFO] Booting worker with pid: 8125

hey -n 50 -c 10 http://localhost:8000

Summary:
  Total:        2.0377 secs
  Slowest:      0.5171 secs
  Fastest:      0.2529 secs
  Average:      0.3268 secs
  Requests/sec: 24.5377 # Cada worker responde ~8 req/sec
```

### Quart - Hypercorn - 1 worker

```bash
hypercorn app-quart:app --workers=1

hey -n 50 -c 10 http://localhost:8000

Summary:
  Total:        1.4794 secs
  Slowest:      0.3086 secs
  Fastest:      0.2665 secs
  Average:      0.2950 secs
  Requests/sec: 33.7972 # 1 worker - 33 req/sec!
```

#### 4 workers

```bash
hypercorn app-quart:app --workers=4

hey -n 50 -c 10 http://localhost:8000

Summary:
  Total:        1.4568 secs
  Slowest:      0.3000 secs
  Fastest:      0.2596 secs
  Average:      0.2902 secs
  Requests/sec: 34.3206 # El mismo resultado que con 1 solo worker
```

#### 4 uvloop workers

```bash
hypercorn app-quart:app --workers=1 --worker-class=uvloop

hey -n 50 -c 10 http://localhost:8000

Summary:
  Total:        1.2907 secs
  Slowest:      0.2624 secs
  Fastest:      0.2522 secs
  Average:      0.2562 secs
  Requests/sec: 38.7390 # Un poco más rápido

```

## Recursos

-   [Gunicorn Workers vs Threads](https://www.notion.so/Gunicorn-Workers-vs-Threads-0cd8fab65be745abac24ef52d6e00d85)
-   [https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads#41696500](https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads#41696500)
-   [https://medium.com/@nhudinhtuan/gunicorn-worker-types-practice-advice-for-better-performance-7a299bb8f929](https://medium.com/@nhudinhtuan/gunicorn-worker-types-practice-advice-for-better-performance-7a299bb8f929)
-   https://github.com/miguelgrinberg/aioflask/

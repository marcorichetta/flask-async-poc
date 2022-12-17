# Flask Async POC

Probar cuanto se la banca Flask con su _async_

Inspiración: https://www.youtube.com/watch?v=0KU67snMjtQ

## Requisitos

-   [Poetry](https://python-poetry.org/docs/)
-   [https://github.com/rakyll/hey](https://github.com/rakyll/hey) o Apache Benchmark

## Pruebas

-   Flask 2.2.2 {async}
-   gunicorn 20.1.0
-   gunicorn - 1 worker[sync] - https://docs.gunicorn.org/en/stable/design.html#sync-workers
-   gunicorn - 4 workers[sync] - https://docs.gunicorn.org/en/stable/design.html#async-workers
-   gunicorn - 4 workers[gevent]
-   gunicorn - 4 workers[eventlet]
-   gunicorn - 4 workers[uvicorn]

## Setup

```bash
poetry install

# Servir app en :8000 con 1 worker
gunicorn app:app

# 10 requests con 5 clientes concurrentes (2 requests c/u)
hey -n 10 -c 5 http://localhost:8000

  Total:        2.5331 secs
  Slowest:      1.2664 secs
  Fastest:      0.2550 secs
  Average:      1.0131 secs
  Requests/sec: 3.9477

```

## Recursos

[Gunicorn Workers vs Threads](https://www.notion.so/Gunicorn-Workers-vs-Threads-0cd8fab65be745abac24ef52d6e00d85)

[https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads#41696500](https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads#41696500)

[https://medium.com/@nhudinhtuan/gunicorn-worker-types-practice-advice-for-better-performance-7a299bb8f929](https://medium.com/@nhudinhtuan/gunicorn-worker-types-practice-advice-for-better-performance-7a299bb8f929)

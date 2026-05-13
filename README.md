
# Flight Delay Predictor API

> Микросервис для прогнозирования задержек авиарейсов


## Описание

REST API для прогнозирования задержек рейсов на основе:
- IATA-кода авиакомпании, аэропортов вылета/прилёта
- Планируемого времени вылета
- Погодных условий

Сервис использует предобученную модель классификации (в режиме разработки предусмотрен fallback на mock-ответы).

---

## Быстрый старт

```bash
docker compose up -d --build
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"airline":"AF","origin":"CDG","destination":"JFK","scheduled_departure":"2026-06-15T14:30:00Z","weather":"rainy"}'
docker compose down
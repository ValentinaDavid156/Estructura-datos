# Plan del Proyecto — CDA

## 1. Fases del proyecto

```text
  FASE 1              FASE 2               FASE 3          FASE 4
  cola.py     →    main.py (API)    →     Pruebas    →    Entrega
  (dominio         (expone cola.py
  puro, sin         por HTTP)
  internet)
```

- **Fase 1** se prueba en la terminal, sin servidor, sin internet, sin Postman. Es la prioridad real del proyecto.
- **Fase 2** no reescribe nada de la lógica: solo abre una "puerta" HTTP hacia lo que ya existe en `cola.py`.
- No se empieza el API (Fase 2) sin que `cola.py` esté terminado y probado (Fase 1).

---

## 2. Arquitectura general

```text
        ┌────────────────────┐
        │      Cliente       │
        └─────────┬──────────┘
                  │  HTTP / JSON          ← Fase 2
        ┌─────────▼──────────────┐
        │    main.py (API)       │   Solo recibe y responde.
        │                        │   Traduce peticiones en llamadas
        │                        │   a ColaAtencion.
        └─────────┬──────────────┘
                  │  llama a métodos
        ┌─────────▼──────────────────────┐
        │    cola.py (dominio)           │   ← Fase 1
        │    clase ColaAtencion          │
        │    lista ordenada por prioridad│
        │    + motor de aceleración      │
        └────────────────────────────────┘
```
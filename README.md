# Muiscas RC - Gestión de deportistas

Web app construida con **Python** y **Flet** para gestionar los registros de los deportistas de Muiscas RC.

## Requisitos

- Python 3.10+

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

La aplicación abrirá una ventana o pestaña del navegador con el panel de gestión.

## Landing page (GitHub Pages)

La carpeta `docs/` contiene la landing page pública del club y está lista para ser publicada en GitHub Pages.

1. En GitHub, ve a **Settings > Pages** del repositorio.
2. Selecciona la rama principal y la carpeta `/docs` como fuente.
3. Guarda los cambios y espera a que se publique la URL.

Si deseas previsualizar la landing en local:

```bash
python -m http.server --directory docs 8000
```

Luego visita `http://localhost:8000`.

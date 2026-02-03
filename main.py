import sqlite3
from dataclasses import dataclass
from pathlib import Path

import flet as ft

DB_PATH = Path(__file__).with_name("muiscas_rc.db")


@dataclass
class Athlete:
    id: int
    nombre: str
    apellido: str
    documento: str
    categoria: str
    fecha_nacimiento: str
    telefono: str
    correo: str
    estado: str


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS atletas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                documento TEXT NOT NULL,
                categoria TEXT NOT NULL,
                fecha_nacimiento TEXT NOT NULL,
                telefono TEXT NOT NULL,
                correo TEXT NOT NULL,
                estado TEXT NOT NULL
            )
            """
        )
        conn.commit()


def fetch_athletes() -> list[Athlete]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT id, nombre, apellido, documento, categoria, fecha_nacimiento, telefono, correo, estado
            FROM atletas
            ORDER BY apellido, nombre
            """
        ).fetchall()
    return [Athlete(*row) for row in rows]


def insert_athlete(athlete: Athlete) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO atletas (nombre, apellido, documento, categoria, fecha_nacimiento, telefono, correo, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                athlete.nombre,
                athlete.apellido,
                athlete.documento,
                athlete.categoria,
                athlete.fecha_nacimiento,
                athlete.telefono,
                athlete.correo,
                athlete.estado,
            ),
        )
        conn.commit()


def update_athlete(athlete: Athlete) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            UPDATE atletas
            SET nombre = ?, apellido = ?, documento = ?, categoria = ?, fecha_nacimiento = ?,
                telefono = ?, correo = ?, estado = ?
            WHERE id = ?
            """,
            (
                athlete.nombre,
                athlete.apellido,
                athlete.documento,
                athlete.categoria,
                athlete.fecha_nacimiento,
                athlete.telefono,
                athlete.correo,
                athlete.estado,
                athlete.id,
            ),
        )
        conn.commit()


def delete_athlete(athlete_id: int) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM atletas WHERE id = ?", (athlete_id,))
        conn.commit()


def main(page: ft.Page) -> None:
    init_db()

    page.title = "Muiscas RC | Registro de deportistas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 24

    selected_id: list[int | None] = [None]

    nombre = ft.TextField(label="Nombre", width=280)
    apellido = ft.TextField(label="Apellido", width=280)
    documento = ft.TextField(label="Documento", width=280)
    categoria = ft.TextField(label="Categoría", width=280)
    fecha_nacimiento = ft.TextField(label="Fecha de nacimiento (YYYY-MM-DD)", width=280)
    telefono = ft.TextField(label="Teléfono", width=280)
    correo = ft.TextField(label="Correo", width=280)
    estado = ft.Dropdown(
        label="Estado",
        width=280,
        options=[
            ft.dropdown.Option("Activo"),
            ft.dropdown.Option("Inactivo"),
            ft.dropdown.Option("Suspendido"),
        ],
        value="Activo",
    )

    feedback = ft.Text(color=ft.colors.RED_600)

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellido")),
            ft.DataColumn(ft.Text("Documento")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Nacimiento")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        expand=True,
    )

    def clear_form() -> None:
        selected_id[0] = None
        nombre.value = ""
        apellido.value = ""
        documento.value = ""
        categoria.value = ""
        fecha_nacimiento.value = ""
        telefono.value = ""
        correo.value = ""
        estado.value = "Activo"
        feedback.value = ""

    def validate_form() -> bool:
        fields = [
            nombre,
            apellido,
            documento,
            categoria,
            fecha_nacimiento,
            telefono,
            correo,
        ]
        missing = [field.label for field in fields if not field.value.strip()]
        if missing:
            feedback.value = f"Completa los campos obligatorios: {', '.join(missing)}"
            return False
        feedback.value = ""
        return True

    def load_table() -> None:
        table.rows = []
        for athlete in fetch_athletes():
            def on_edit(event: ft.ControlEvent, athlete=athlete) -> None:
                selected_id[0] = athlete.id
                nombre.value = athlete.nombre
                apellido.value = athlete.apellido
                documento.value = athlete.documento
                categoria.value = athlete.categoria
                fecha_nacimiento.value = athlete.fecha_nacimiento
                telefono.value = athlete.telefono
                correo.value = athlete.correo
                estado.value = athlete.estado
                feedback.value = ""
                page.update()

            def on_delete(event: ft.ControlEvent, athlete_id=athlete.id) -> None:
                delete_athlete(athlete_id)
                clear_form()
                load_table()
                page.update()

            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(athlete.nombre)),
                        ft.DataCell(ft.Text(athlete.apellido)),
                        ft.DataCell(ft.Text(athlete.documento)),
                        ft.DataCell(ft.Text(athlete.categoria)),
                        ft.DataCell(ft.Text(athlete.fecha_nacimiento)),
                        ft.DataCell(ft.Text(athlete.telefono)),
                        ft.DataCell(ft.Text(athlete.correo)),
                        ft.DataCell(ft.Text(athlete.estado)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        tooltip="Editar",
                                        on_click=on_edit,
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        tooltip="Eliminar",
                                        icon_color=ft.colors.RED_600,
                                        on_click=on_delete,
                                    ),
                                ],
                                spacing=8,
                            )
                        ),
                    ]
                )
            )

    def on_save(event: ft.ControlEvent) -> None:
        if not validate_form():
            page.update()
            return

        athlete = Athlete(
            id=selected_id[0] or 0,
            nombre=nombre.value.strip(),
            apellido=apellido.value.strip(),
            documento=documento.value.strip(),
            categoria=categoria.value.strip(),
            fecha_nacimiento=fecha_nacimiento.value.strip(),
            telefono=telefono.value.strip(),
            correo=correo.value.strip(),
            estado=estado.value,
        )

        if selected_id[0] is None:
            insert_athlete(athlete)
        else:
            update_athlete(athlete)

        clear_form()
        load_table()
        page.update()

    def on_clear(event: ft.ControlEvent) -> None:
        clear_form()
        page.update()

    load_table()

    form = ft.Container(
        content=ft.Column(
            [
                ft.Text("Registro de deportistas", style=ft.TextThemeStyle.TITLE_LARGE),
                ft.Text(
                    "Gestiona los datos principales de los deportistas de Muiscas RC.",
                    color=ft.colors.GREY_700,
                ),
                ft.Divider(),
                nombre,
                apellido,
                documento,
                categoria,
                fecha_nacimiento,
                telefono,
                correo,
                estado,
                feedback,
                ft.Row(
                    [
                        ft.ElevatedButton("Guardar", on_click=on_save),
                        ft.OutlinedButton("Limpiar", on_click=on_clear),
                    ],
                    spacing=12,
                ),
            ],
            spacing=12,
        ),
        padding=16,
        width=320,
        bgcolor=ft.colors.BLUE_GREY_50,
        border_radius=12,
    )

    page.add(
        ft.ResponsiveRow(
            [
                ft.Container(form, col={"xs": 12, "md": 4}),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Listado de deportistas", style=ft.TextThemeStyle.TITLE_MEDIUM),
                            ft.Container(table, expand=True),
                        ],
                        expand=True,
                    ),
                    col={"xs": 12, "md": 8},
                ),
            ],
            spacing=24,
        )
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8550)

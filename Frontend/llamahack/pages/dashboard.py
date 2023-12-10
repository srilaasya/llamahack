"""The dashboard page."""
from llamahack.templates import template

import reflex as rx
from llamahack.components.meeting import meeting

@template(route="/dashboard", title="Dashboard")
def dashboard() -> rx.Component:

    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.heading("Dashboard", font_size="3em"),
        meeting(),  # This should include the modal as part of its component tree
        rx.text("Welcome to Reflex!"),
        rx.text(
            "You can edit this page in ",
            rx.code("{your_app}/pages/dashboard.py"),
        ),
    )

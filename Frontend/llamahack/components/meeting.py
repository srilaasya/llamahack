from llamahack import styles
import reflex as rx

# Define a ModalState class to control the modal's visibility


class ModalState(rx.State):
    show: bool = False

    def change(self):
        self.show = not self.show


def meeting() -> rx.Component:
    """Navbar header with a modal opener button.

    Returns:
        The navbar header component.
    """

    # Define the modal component
    modal = rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header("Confirm"),
                rx.modal_body("Your modal content here"),
                rx.modal_footer(
                    rx.button("Close", on_click=ModalState.change)
                ),
            )
        ),
        is_open=ModalState.show,
    )

    return rx.hstack(
        # Button to open the modal
        rx.button(
            "Open Modal",
            on_click=ModalState.change,
            style={
                "margin_right": "1em",
                # Add additional styling as needed
            }
        ),
        rx.spacer(),
        position="fixed",
        left="0",
        top="0",
        width="100%",
        padding="1em",
    ), modal  # include the modal component in the return statement

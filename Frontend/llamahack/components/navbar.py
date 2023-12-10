from llamahack import styles
import reflex as rx

# def navbar_header() -> rx.Component:
#     """Navbar header.

#     Returns:
#         The navbar header component.
#     """
#     return rx.hstack(
#         # The logo.
#         rx.image(
#             src="/icon.svg",
#             height="2em",
#         ),
#         rx.spacer(),
#         # Link to Reflex GitHub repo.
#         rx.link(
#             rx.center(
#                 rx.image(
#                     src="/github.svg",
#                     height="3em",
#                     padding="0.5em",
#                 ),
#                 box_shadow=styles.box_shadow,
#                 bg="transparent",
#                 border_radius=styles.border_radius,
#                 _hover={
#                     "bg": styles.accent_color,
#                 },
#             ),
#             href="https://github.com/reflex-dev/reflex",
#         ),

#         width="100%",
#         padding="1em",
#     )

def navbar_footer() -> rx.Component:
    """Navbar footer.

    Returns:
        The navbar footer component.
    """
    return rx.hstack(
        rx.spacer(),
        rx.link(
            rx.text("Docs"),
            href="https://reflex.dev/docs/getting-started/introduction/",
        ),
        rx.link(
            rx.text("Blog"),
            href="https://reflex.dev/blog/",
        ),
        width="100%",
        padding="1em",
    )

def navbar_item(text: str, icon: str, url: str) -> rx.Component:
    """Navbar item.

    Args:
        text: The text of the item.
        icon: The icon of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The navbar item component.
    """
    active = (rx.State.router.page.path == f"/{text.lower()}") | (
        (rx.State.router.page.path == "/") & text == "Home"
    )

    return rx.link(
        rx.hstack(
            rx.image(
                src=icon,
                height="2.5em",
                padding="0.5em",
            ),
            rx.text(
                text,
            ),
            bg=rx.cond(
                active,
                styles.accent_color,
                "transparent",
            ),
            color=rx.cond(
                active,
                styles.accent_text_color,
                styles.text_color,
            ),
            border_radius=styles.border_radius,
            box_shadow=styles.box_shadow,
            padding_x="1em",
        ),
        href=url,
    )

def navbar() -> rx.Component:
    """The navbar.

    Returns:
        The navbar component.
    """
    from reflex.page import get_decorated_pages

    return rx.box(
        rx.hstack(
            # navbar_header(),
            rx.hstack(
                *[
                    navbar_item(
                        text=page.get("title", page["route"].strip("/").capitalize()),
                        icon=page.get("image", "/github.svg"),
                        url=page["route"],
                    )
                    for page in get_decorated_pages()
                ],
                align_items="center",
                padding="1em",
                justify_content="space-between",
                width="100%",
            ),
            navbar_footer(),
            height="100vh",
        ),
        position="fixed",
        top="10px",
        border_bottom=styles.border,
    )

from rich_toolkit import RichToolkit, RichToolkitTheme
from rich_toolkit.styles import TaggedStyle


class PixeltableStyle(TaggedStyle):
    def __init__(self, tag_width: int = 11) -> None:
        super().__init__(tag_width=tag_width)


def get_rich_toolkit() -> RichToolkit:
    theme = RichToolkitTheme(
        style=PixeltableStyle(tag_width=11),
        theme={
            "tag.title": "white on #6C3FC5",
            "tag": "white on #5533A0",
            "placeholder": "grey85",
            "text": "white",
            "selected": "#5533A0",
            "result": "grey85",
            "progress": "on #5533A0",
            "error": "red",
        },
    )
    return RichToolkit(theme=theme)

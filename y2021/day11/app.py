import itertools
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Tuple

from rich.align import Align
from rich.text import Text
from textual.app import App
from textual.widget import Widget


INPUTS_FILE = Path(__file__).parent / "input.txt"


class Lightboard(Widget):
    def __init__(self, *args: Any, data: Dict[Tuple[int, int], int], **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._data = data
        self._iteration = 0
        self.use_emoji = True

    def on_mount(self) -> None:
        self.set_interval(1, self.refresh)

    def render(self) -> None:
        take_step(self._data)
        self._iteration += 1

        lines = [
            f"Iteration {self._iteration}",
            "",
        ]
        for i in range(10):
            chars = []
            for j in range(10):
                value = self._data[i, j]
                if value == 0:
                    if self.use_emoji:
                        value_str = "🟡"
                    else:
                        value_str = f"[yellow]{value}[/yellow]"
                else:
                    if self.use_emoji:
                        value_str = "⚫"
                    else:
                        value_str = f"[white]{value}[/white]"
                chars.append(value_str)
            line = "".join(chars)
            lines.append(line)
        time = "\n".join(lines)
        time = Text.from_markup(time)

        return Align.center(time, vertical="middle")


class SimpleApp(App):
    async def on_load(self) -> None:
        await self.bind("q", "quit")
        await self.bind("e", "toggle_emoji")

    async def on_mount(self) -> None:
        self.lightboard = Lightboard(data=load_data())
        await self.view.dock(self.lightboard)

    async def action_toggle_emoji(self) -> None:
        self.lightboard.use_emoji = not self.lightboard.use_emoji


def parse(input_str: str) -> Dict[Tuple[int, int], int]:
    data = {}
    for i, line in enumerate(input_str.strip().split()):
        for j, char in enumerate(line.strip()):
            data[i, j] = int(char)

    return data


def load_data() -> Dict[Tuple[int, int], int]:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        return parse(input_str)


def take_step(data: Dict[Tuple[int, int], int]) -> int:
    for pos in data:
        data[pos] += 1
    blinked = set()
    while any(i > 9 for i in data.values()):
        for pos in dict(data):
            if data[pos] > 9 and pos not in blinked:
                blinked.add(pos)
                data.pop(pos)
                for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1]):
                    new_pos = (pos[0] + dx, pos[1] + dy)
                    if new_pos in data:
                        data[new_pos] += 1
    for pos in blinked:
        data[pos] = 0
    return len(blinked)


SimpleApp.run(log="textual.log")

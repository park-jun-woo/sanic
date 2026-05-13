# ff:type feature=cli type=model
# ff:what Rich TTY MOTD display with box drawing, logo, and formatted key-value

from shutil import get_terminal_size
from textwrap import indent, wrap

from sanic import __version__
from sanic.application.motd_base import MOTD
from sanic.log import logger


class MOTDTTY(MOTD):
    """A MOTD display for terminals that support ANSI escape codes."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_variables()

    def set_variables(self):  # no  cov
        """Set the variables used for display."""
        fallback = (108, 24)
        terminal_width = max(
            get_terminal_size(fallback=fallback).columns, fallback[0]
        )
        self.max_value_width = terminal_width - fallback[0] + 36

        self.key_width = 4
        self.value_width = self.max_value_width
        if self.data:
            self.key_width = max(map(len, self.data.keys()))
            self.value_width = min(
                max(map(len, self.data.values())), self.max_value_width
            )
        if self.extra:
            self.key_width = max(
                self.key_width, max(map(len, self.extra.keys()))
            )
            self.value_width = min(
                max((*map(len, self.extra.values()), self.value_width)),
                self.max_value_width,
            )
        self.logo_lines = self.logo.split("\n") if self.logo else []
        self.logo_line_length = 24
        self.centering_length = (
            self.key_width + self.value_width + 2 + self.logo_line_length
        )
        self.display_length = self.key_width + self.value_width + 2

    def display(self, version=True, action="Goin' Fast", out=None):
        """Display the MOTD.

        Args:
            version (bool, optional): Display the version. Defaults to `True`.
            action (str, optional): Action to display. Defaults to
                `"Goin' Fast"`.
            out (Optional[Callable], optional): Output function. Defaults to
                `None`.
        """
        if not out:
            out = logger.info
        header = "Sanic"
        if version:
            header += f" v{__version__}"
        header = header.center(self.centering_length)
        running = (
            f"{action} @ {self.serve_location}" if self.serve_location else ""
        ).center(self.centering_length)
        length = len(header) + 2 - self.logo_line_length
        first_filler = "─" * (self.logo_line_length - 1)
        second_filler = "─" * length
        display_filler = "─" * (self.display_length + 2)
        lines = [
            f"\n┌{first_filler}─{second_filler}┐",
            f"│ {header} │",
            f"│ {running} │",
            f"├{first_filler}┬{second_filler}┤",
        ]

        self._render_data(lines, self.data, 0)
        if self.extra:
            logo_part = self._get_logo_part(len(lines) - 4)
            lines.append(f"│ {logo_part} ├{display_filler}┤")
            self._render_data(lines, self.extra, len(lines) - 4)

        self._render_fill(lines)

        lines.append(f"└{first_filler}┴{second_filler}┘\n")
        out(indent("\n".join(lines), "  "))

    def _render_wrapped_value(self, lines, key, wrapped, start_idx):
        offset = 0
        for wrap_index, part in enumerate(wrapped):
            part = part.ljust(self.value_width)
            logo_part = self._get_logo_part(start_idx + offset + wrap_index)
            display = (
                f"{key}: {part}"
                if wrap_index == 0
                else (" " * len(key) + f"  {part}")
            )
            lines.append(f"│ {logo_part} │ {display} │")
            if wrap_index:
                offset += 1
        return offset

    def _render_data(self, lines, data, start):
        offset = 0
        for idx, (key, value) in enumerate(data.items(), start=start):
            key = key.rjust(self.key_width)
            wrapped = wrap(value, self.max_value_width, break_on_hyphens=False)
            offset += self._render_wrapped_value(
                lines,
                key,
                wrapped,
                idx + offset,
            )

    def _render_fill(self, lines):
        filler = " " * self.display_length
        idx = len(lines) - 5
        for i in range(1, len(self.logo_lines) - idx):
            logo_part = self.logo_lines[idx + i]
            lines.append(f"│ {logo_part} │ {filler} │")

    def _get_logo_part(self, idx):
        try:
            logo_part = self.logo_lines[idx]
        except IndexError:
            logo_part = " " * (self.logo_line_length - 3)
        return logo_part

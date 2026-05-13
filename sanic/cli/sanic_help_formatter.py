# ff:type feature=cli type=formatter
# ff:what Custom help formatter that suppresses usage line and adjusts spacing
from argparse import SUPPRESS, RawTextHelpFormatter


class SanicHelpFormatter(RawTextHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if not usage:
            usage = SUPPRESS
            # Add one linebreak, but not two
            self.add_text("\x1b[1A")
        super().add_usage(usage, actions, groups, prefix)

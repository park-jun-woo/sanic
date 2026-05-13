# ff:type feature=cli type=model
# ff:what TLS certificate CLI argument group for cert, key, and tls directory o
from sanic.cli.group import Group


class TLSGroup(Group):
    name = "TLS certificate"

    def attach(self, short: bool = False):
        if short:
            return

        self.container.add_argument(
            "--cert",
            dest="cert",
            type=str,
            help="Location of fullchain.pem, bundle.crt or equivalent",
        )
        self.container.add_argument(
            "--key",
            dest="key",
            type=str,
            help="Location of privkey.pem or equivalent .key file",
        )
        self.container.add_argument(
            "--tls",
            metavar="DIR",
            type=str,
            action="append",
            help=(
                "TLS certificate folder with fullchain.pem and privkey.pem\n"
                "May be specified multiple times to choose multiple "
                "certificates"
            ),
        )
        self.container.add_argument(
            "--tls-strict-host",
            dest="tlshost",
            action="store_true",
            help="Only allow clients that send an SNI matching server certs",
        )

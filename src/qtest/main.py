import click

from qtest.commands.test1 import test1


@click.group()
def main() -> None:
    pass


main.add_command(test1)

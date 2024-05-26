import click
import qiskit  # type: ignore


@click.group()
def test1() -> None:
    pass


@test1.command()
def run() -> None:
    click.echo(f"Hi!")

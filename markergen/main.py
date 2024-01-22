import click

from .marker import Marker


def fmt_triplet(v):
    return f"({v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f})"


@click.group()
def cli():
    pass


@cli.command(help="Read marker ROM file and show a summary of its attributes")
@click.argument("filename")
def inspect(filename: str):
    marker = Marker.read_ROM(filename)
    print(f"marker serial number: {marker.serial}")
    print(f"A: {fmt_triplet(marker.A)}")
    print(f"B: {fmt_triplet(marker.B)}")
    print(f"C: {fmt_triplet(marker.C)}")
    print(f"D: {fmt_triplet(marker.D)}")


@cli.command(help="Export marker ROM to OpenSCAD file")
@click.argument("filename")
@click.option("--output", "-o", help="output filename", required=False)
def export(filename: str, output: str):
    marker = Marker.read_ROM(filename)
    scad = marker.to_scad()
    if not output:
        click.secho(scad)
    else:
        with open(output, "w") as f:
            f.write(scad)

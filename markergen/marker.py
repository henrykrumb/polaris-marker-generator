#!/usr/bin/env python3
import struct

import numpy as np

from markergen import scad


class Marker:
    serial: str
    A: np.array
    B: np.array
    C: np.array
    D: np.array
    MA: np.array
    MB: np.array
    MC: np.array
    MD: np.array

    def to_dict(self) -> dict:
        D = {}
        for key in (
            'A', 'B', 'C', 'D',
            'MA', 'MB', 'MC', 'MD',
            'serial'
        ):
            D[key] = getattr(self, key)
        return D

    @classmethod
    def from_dict(cls, D):
        marker = cls()
        for key in (
            'A', 'B', 'C', 'D',
            'MA', 'MB', 'MC', 'MD',
            'serial'
        ):
            value = D[key]
            setattr(marker, key, value)
        return marker

    def write_ROM(self, filename):
        def pack_triplet(triplet):
            return struct.pack('fff', *triplet)
        # experimental!
        with open(filename, 'wb') as f:
            f.write('NDI'.encode('ASCII'))
            f.write(struct.pack('69I', [0] * 69))
            f.write(pack_triplet(self.A))
            f.write(pack_triplet(self.B))
            f.write(pack_triplet(self.C))
            f.write(pack_triplet(self.D))

    @classmethod
    def read_ROM(cls, filename):
        marker = cls()

        rom = None
        with open(filename, 'rb') as f:
            rom = f.read()
        magic = rom[:3]
        if magic.decode('ASCII') != 'NDI':
            click.secho('[err] Not an NDI ROM file.')
            exit(1)
        N_bytes = len(rom)
        if N_bytes > 752:
            click.secho('[warn] ROM file longer than expected.')
        elif N_bytes < 752:
            click.secho('[err] ROM file shorter than expected.')
            exit(1)

        def unpack_triplet(pos):
            arr = np.array(struct.unpack('fff', rom[pos:pos+12]))
            return np.array([arr[2], arr[1], arr[0]])

        marker.A = unpack_triplet(72)
        marker.B = unpack_triplet(84)
        marker.C = unpack_triplet(96)
        marker.D = unpack_triplet(108)

        #print(rom[120:312])

        marker.MA = unpack_triplet(312)
        marker.MB = unpack_triplet(324)
        marker.MC = unpack_triplet(336)
        marker.MD = unpack_triplet(348)

        #print(rom[360:580])
        
        marker.serial = rom[580:599].decode('ASCII')

        return marker

    def to_scad(self):
        text = scad.union([
            scad.hull([
                scad.translate(*self.A, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ]),
                scad.translate(*self.B, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ])
            ]),
            scad.hull([
                scad.translate(*self.A, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ]),
                scad.translate(*self.C, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ])
            ]),
            scad.hull([
                scad.translate(*self.A, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ]),
                scad.translate(*self.D, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ])
            ]),
            scad.hull([
                scad.translate(*self.B, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ]),
                scad.translate(*self.C, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ])
            ]),
            scad.hull([
                scad.translate(*self.B, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ]),
                scad.translate(*self.D, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ])
            ]),
            scad.hull([
                scad.translate(*self.C, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ]),
                scad.translate(*self.D, [
                    scad.chamfered_cylinder(6.5, 9.4 / 2)
                ])
            ])
        ])
        return text

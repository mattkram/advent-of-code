import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

INPUTS_FILE = Path(__file__).parent / "input.txt"


@dataclass
class Packet:
    version: int
    type_id: int
    literal_value: Optional[int] = None
    subpackets: List["Packet"] = field(default_factory=list)

    def version_sum(self) -> int:
        return self.version + sum(p.version_sum() for p in self.subpackets)

    def evaluate(self) -> int:
        if self.type_id == 4:
            assert self.literal_value is not None
            return self.literal_value

        values = tuple(packet.evaluate() for packet in self.subpackets)
        if self.type_id == 0:
            return sum(values)
        if self.type_id == 1:
            return math.prod(values)
        if self.type_id == 2:
            return min(values)
        if self.type_id == 3:
            return max(values)
        if self.type_id == 5:
            return int(values[0] > values[1])
        if self.type_id == 6:
            return int(values[0] < values[1])
        if self.type_id == 7:
            return int(values[0] == values[1])
        raise ValueError("Unreachable")


class BitStream:
    def __init__(self, hex_string: str):
        self.bit_string = "".join(
            f"{int(char, 16):04b}" for char in hex_string.lower().strip()
        )
        self.pos = 0

    def read(self, num_bits: int) -> int:
        substring = self.bit_string[self.pos : self.pos + num_bits]
        value = int(substring, 2)
        self.pos += num_bits
        return value

    def read_packet(self) -> Packet:
        packet = Packet(version=self.read(3), type_id=self.read(3))
        if packet.type_id == 4:  # Literal value
            packet.literal_value = 0
            while True:
                continuation = self.read(1)
                packet.literal_value = (packet.literal_value << 4) | self.read(4)
                if not continuation:
                    break
        else:  # Operator packet
            length_type_id = self.read(1)
            if length_type_id == 0:
                num_bits_in_packet = self.read(15)
                start_pos = self.pos
                while self.pos - start_pos < num_bits_in_packet:
                    subpacket = self.read_packet()
                    packet.subpackets.append(subpacket)
            elif length_type_id == 1:
                num_subpackets = self.read(11)
                for _ in range(num_subpackets):
                    subpacket = self.read_packet()
                    packet.subpackets.append(subpacket)
        return packet


def calculate_part1(input_str: str) -> int:
    stream = BitStream(input_str)
    packet = stream.read_packet()
    return packet.version_sum()


def calculate_part2(input_str: str) -> int:
    stream = BitStream(input_str)
    packet = stream.read_packet()
    return packet.evaluate()


def main() -> None:
    with INPUTS_FILE.open() as fp:
        input_str = fp.read()
        print(f"The answer to part 1 is {calculate_part1(input_str)}")
        print(f"The answer to part 2 is {calculate_part2(input_str)}")


if __name__ == "__main__":
    main()

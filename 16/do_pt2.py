import argparse
from enum import Enum

class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GREATER = 5
    LESS = 6
    EQUAL = 7


class Packet:
    def __init__(self, hex_data=None, bit_data=None, packet_list=[], test=False):
        self.test = test

        if hex_data is not None:
            self.payload = self.hex2bin(hex_data)
        elif bit_data is not None:
            self.payload = bit_data

        self.payload_length = len(self.payload)
        self.num_bits_parsed = 0
        self.num_sub_packets = 0
        self.len_sub_packets = 0
        self.value = None
        self.sub_packets = []
        self.version = None
        self.type = None
        self.packet_list = packet_list

    def get_header(self):
        ret = {}
        for field in "version", "type_id":
            ret[field] = self.get_value(3)
        return tuple(ret.values())

    def parse(self):
        if self.test:
            print(f"\npayload: {self}")
        self.version, type_id = self.get_header()
        self.type = PacketType(type_id)
        if self.test:
            print(f"version: {self.version}")
            print(f"type: {self.type._name_}")

        if self.type == PacketType.LITERAL:
            self.parse_literal()
            if self.test:
                print(f"value: {self.value}")
        else:
            self.parse_operator()

    def get_value(self, num_bits):
        bin_str = ""
        for i in range(num_bits):
            bin_str += self.payload.pop(0)
            self.num_bits_parsed += 1
        return int(bin_str, 2)

    def parse_literal(self):
        is_final = False
        hex_val = ""
        while not is_final:
            raw_nibble = self.get_value(5)
            is_final = (raw_nibble & 0b10000) == 0
            nibble = raw_nibble & 0b01111
            hex_val += f"{nibble:X}"

        self.value = int(hex_val, 16)

    def hex2bin(self, hex_val):
        bit_str = "".join([f"{int(c,16):04b}" for c in hex_val])
        bit_list = [bit for bit in bit_str]
        return bit_list

    def calculate(self, subpackets):
        if self.type == PacketType.SUM:
            value = 0
            for packet in subpackets:
                value += packet.value
        elif self.type == PacketType.PRODUCT:
            value = 1
            for packet in subpackets:
                value *= packet.value
        elif self.type == PacketType.MIN:
            value = None
            for packet in subpackets:
                if value is None or packet.value < value:
                    value = packet.value
        elif self.type == PacketType.MAX:
            value = None
            for packet in subpackets:
                if value is None or packet.value > value:
                    value = packet.value
        elif self.type == PacketType.GREATER:
            value = int(subpackets[0].value > subpackets[1].value)
        elif self.type == PacketType.LESS:
            value = int(subpackets[0].value < subpackets[1].value)
        elif self.type == PacketType.EQUAL:
            value = int(subpackets[0].value == subpackets[1].value)

        self.value = value

    def parse_operator(self):
        length_type = self.get_value(1)
        subpackets = []
        if length_type == 0:
            self.len_sub_packets = self.get_value(15)
            if self.test:
                print(f"sub packets size: {self.len_sub_packets}")
            subpackets.extend(self.parse_subpackets_by_length())
        else:
            self.num_sub_packets = self.get_value(11)
            if self.test:
                print(f"num sub packets: {self.num_sub_packets}")
            subpackets.extend(self.parse_subpackets_by_count())

        self.calculate(subpackets)

        self.packet_list.extend(subpackets)

    def parse_subpackets_by_length(self):
        subpackets = []
        rest_of_data = self.payload.copy()
        while self.len_sub_packets > 0:
            if self.test:
                print(f"\nParsing subpacket: {''.join(rest_of_data)}")
            subpacket = Packet(
                bit_data=rest_of_data, packet_list=self.packet_list, test=self.test
            )
            subpacket.parse()
            bits_consumed = subpacket.num_bits_parsed
            # burn off the payload consumed by this subpacket
            self.get_value(bits_consumed)
            subpackets.append(subpacket)
            self.len_sub_packets -= bits_consumed
        return subpackets

    def parse_subpackets_by_count(self):
        subpackets = []
        rest_of_data = self.payload.copy()
        while self.num_sub_packets > 0:
            subpacket = Packet(
                bit_data=rest_of_data, packet_list=self.packet_list, test=self.test
            )
            subpacket.parse()
            bits_consumed = subpacket.num_bits_parsed
            # burn off the payload consumed by this subpacket
            self.get_value(bits_consumed)
            subpackets.append(subpacket)
            self.num_sub_packets -= 1
            rest_of_data = subpacket.payload
        return subpackets

    def __str__(self):
        return "".join(self.payload)

    def __repr__(self):
        return str(self)


class Runner:
    def __init__(self, input_file=None, data=None, test=False):
        self.test = test
        self.summary = {}
        self.input_file = input_file
        if data is None:
            self.data = self.read_input()
        else:
            self.data = data

    def read_input(self):
        with open(self.input_file, "r") as f:
            data = f.read().strip()
        return data

    def process_data(self):
        data = self.data
        versions_sum = 0
        packets = []
        main_packet = Packet(hex_data=data, packet_list=packets, test=self.test)
        main_packet.parse()
        value = main_packet.value
        packets.insert(0, main_packet)
        for packet in packets:
            versions_sum += packet.version
        return versions_sum, value


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Day 16: Packet Parsing")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--input_file")
    parser.add_argument("data", nargs="?")

    args = parser.parse_args()

    if args.data:
        input_file = None
        data = args.data
    elif args.input_file:
        input_file = args.input_file
        data = None
    elif args.test:
        input_file = "test_input.txt"
        data = None
    else:
        input_file = "input.txt"
        data = None

    runner = Runner(input_file=input_file, data=data, test=args.test)

    print(f"{runner.process_data()}")

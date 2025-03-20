import random
from collections import defaultdict, namedtuple
from itertools import chain
from math import ceil
from operator import attrgetter

from readfile import read


# file_name = '09_example.txt'
file_name = '09_input.txt'


FileBlock = namedtuple('FileBlock', ('start', 'size', 'id', 'display', 'type'))
SpaceBlock = namedtuple('SpaceBlock', ('start', 'size', 'display', 'type'))

def get_file_display():
    return random.sample(set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'), 1)

def make_file_block(start, size, id, display=None):
    if display is None:
        display = get_file_display()[0] * size

    return FileBlock(
        id=id,
        start=start,
        size=size,
        display=display,
        type='file'
    )


def make_space_block(start, size):
    return SpaceBlock(
        start=start,
        size=size,
        display='.' * size,
        type='space'
    )


class Solution:
    disk_size = 0
    free_size = 0

    disk = None
    disk_map = None
    spaces = None

    file_blocks = None  # file_id: block
    space_blocks = None  # start: block

    def __init__(self):
        self.disk = []
        self.spaces = []
        self.space_blocks = {}
        self.file_blocks = {}

        for line in read(file_name):
            self.disk_map = line

        if len(self.disk_map) % 2 == 1:
            # odd number of instructions
            # add 0 free blocks after last file-id
            self.disk_map += '0'

        file_id = 0
        map_size = len(self.disk_map)

        for index_pointer in range(0, map_size, 2):

            file_length = int(self.disk_map[index_pointer])
            starting_index = len(self.disk)

            # append to disk array
            for f in range(file_length):
                self.disk.append(file_id)

            # store file block
            fb = make_file_block(
                id=file_id,
                start=starting_index,
                size=file_length,
            )
            self.file_blocks[file_id] = fb

            file_id += 1
            free_index = len(self.disk)

            free_length = int(self.disk_map[index_pointer + 1])

            if free_length:
                self.space_blocks[free_index] = make_space_block(
                    start=free_index,
                    size=free_length,
                )

            for i in range(free_length):
                self.spaces.append(free_index + i)
                self.disk.append('.')

            # print(f'added {file_length} blocks, ({free_length} spaces) for ID:{file_id - 1}')

        self.disk_size = len(self.disk)
        self.free_size = len(self.spaces)

    def print(self):
        # print(''.join(str(block_content) for block_content in self.disk), self.disk_map, self.spaces)

        d = ''
        for block in self.get_ordered_blocks():
            d += block.display

        section_size = 120
        sections = len(d) // section_size
        for i in range(sections):
            print(i, d[i * section_size:(i+1) * section_size])

    def get_ordered_blocks(self, reverse=False):
        return sorted(
            chain(self.file_blocks.values(), self.space_blocks.values()),
            key=lambda x: x.start,
            reverse=reverse
        )

    def show_blocks(self):
        for block in self.get_ordered_blocks():
            print(block)

    def part11(self):
        # gather up N final file blocks,
        # N is blocks *after* most compacted form of disk

        # put each gathered file in an earlier block

        # convert former locations to spaces
        # compute the hashcode

        # full disk blocks
        compact_size = self.disk_size - self.free_size

        full_disk_blocks = set(
            i for i in range(len(self.disk))
        ) - set(self.spaces)

        # get the occupied blocks with the greatest index, 
        # at positions greater than the compact_size
        blocks_to_move = [
            block for block in full_disk_blocks
            if block > (compact_size - 1)
        ]
        migrate_blocks = sorted(blocks_to_move, reverse=True)

        for file_block, free in zip(migrate_blocks, self.spaces):
            self.disk[free] = self.disk[file_block]
            self.disk[file_block] = '-'

        self.print()


    @property
    def checksum(self):
        check = 0

        for i in range(self.disk_size):
            char = self.disk[i]
            if str(char) not in '.-':
                # print(f'looking at {char}')
                check += self.disk[i] * i

        return check

    @property
    def check2(self):
        all_blocks = self.get_ordered_blocks()
        disk_counter = 0
        chk = 0

        for block in all_blocks:
            for i in range(block.size):
                if block.type == 'file':
                    partial = disk_counter * block.id
                    chk += partial
                    # print(f'{disk_counter} * {block.id} = {partial} ({chk})')
                disk_counter += 1

        return chk

    def part2(self):
        # new data structures
        # file_blocks: id, position-on-disk, size-in-blocks
        # space_blocks: position-on-disk, size-in-blocks

        # iterate over each file_id in descending order
        for block in self.get_ordered_blocks(reverse=True):
            if block.type == 'file':
                file_block = block
            else:
                continue

            # sort spaces by position-on-disk
            # filter spaces to those bigger than file-size
            open_spaces = [
                block
                for block in self.get_ordered_blocks()
                if block.size >= file_block.size and
                block.start < file_block.start and
                block.type == 'space'
            ]

            # (if available) move file-block
            if open_spaces:

                new_location = open_spaces[0]

                del self.file_blocks[file_block.id]
                del self.space_blocks[new_location.start]

                self.file_blocks[file_block.id] = make_file_block(
                    id=file_block.id,
                    start=new_location.start,
                    size=file_block.size,
                    display=file_block.display,
                )

                # recalculate any left over space after moving file
                remaining_space = new_location.size - file_block.size
                if remaining_space:
                    new_space_start = new_location.start + file_block.size

                    self.space_blocks[new_space_start] = make_space_block(
                        start=new_space_start,
                        size=remaining_space,
                    )

                # make the vacated block free
                self.space_blocks[file_block.start] = make_space_block(
                    start=file_block.start,
                    size=file_block.size,
                )

                # recalculate vacated space by combining
                self.combine_space()

        self.print()
        print(self.check2)

    def combine_space(self):
        combinable_blocks = self.get_combinable_blocks()

        if combinable_blocks:
            for combinable in combinable_blocks:
                new_space = make_space_block(
                    start=combinable[0].start,
                    size=sum(b.size for b in combinable),
                )
                for b in combinable:
                    del self.space_blocks[b.start]
                self.space_blocks[new_space.start] = new_space


    def get_combinable_blocks(self):
        combinable_blocks = []

        in_progress_block = []

        for block in self.get_ordered_blocks():
            if block.type == 'space':
                in_progress_block.append(block)
            else:
                if len(in_progress_block) > 1:
                    combinable_blocks.append(in_progress_block)

                in_progress_block = []

        return combinable_blocks


if __name__ == '__main__':
    s = Solution()
    s.print()
    print()

    s.part11()

    print(f'checksum: {s.checksum}')
    print()

    s.part2()
    # too high: 6508830920214


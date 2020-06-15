# 使用方法
# $ python read_box.py [引数1]
#
# 引数1: ファイル名

import os
import sys

leaf_list = ['fiel', 'mdat', 'rdrf', 'rmcd', 'rmcs', 'rmdr', 'rmqu', 'rmvc', 'wfex', 'cmvd', 'co64', 'dcom', 'elst', 'gmhd', 'hdlr', 'mdhd', 'smhd', 'stco', 'stsc', 'stsd', 'stss', 'stsz', 'stts', 'tkhd', 'vmhd']
parent_list = ['cmov', 'ctts', 'edts', 'esds', 'free', 'ftyp', 'iods', 'junk', 'mdia', 'minf', 'moov', 'mvhd', 'pict', 'pnot', 'rmda', 'rmra', 'skip', 'stbl', 'trak', 'uuid', 'wide']
unknown_list = ['dinf', 'dref']

def read_box(file, indent, fsize):
    file_pos = file.tell()

    # read container size
    data = file.read(4)
    size = int.from_bytes(data, byteorder='big')
    if size == 0:
        #print('\t'*indent, 'size 0')
        return 0

    # read container type
    data = file.read(4)
    try:
        box_type = data.decode("utf-8") 
    except UnicodeDecodeError:
        #print('\t'*indent, 'decode error', data)
        return 0

    if box_type not in leaf_list and box_type not in parent_list and box_type not in unknown_list:
        #print('\t'*indent, 'unknown type', box_type)
        return 0

    #sum_size = 8 # size & type
    # when container size exceeds 2147483647
    if size == 1:
        data = file.read(8)
        size = int.from_bytes(data, byteorder='big')
        #sum_size += 8

    end = file_pos + size

    if fsize < end:
        print('invalid box size.', 'fsize = ', fsize, ', end = ', end)
        return 0

    out_text = '\t'*indent
    out_text += box_type
    out_text += '  :  '
    out_text += str(size)
    print(out_text)

    while file.tell() < end:
        rsize = read_box(file, indent + 1, fsize)
        if rsize > 0:
            #sum_size += rsize
            pass
        else:
            file.seek(end, os.SEEK_SET)
            #sum_size = size

    # if size == sum_size:
    #     print('match!!', 'size = ', size, ', sum_size = ', sum_size)
    # else:
    #     print('unmatch!!', 'size = ', size, ', sum_size = ', sum_size)

    return size

if __name__ == '__main__':
    with open(sys.argv[1],'r+b') as file:
        fsize = file.seek(0, os.SEEK_END)
        file.seek(0, os.SEEK_SET)
        sum_size = 0
        while file.tell() < fsize:
            rsize = read_box(file, 0, fsize)
            if rsize > 0:
                sum_size += rsize
            else:
                break

    print('file size = ', fsize, ', sum size = ', sum_size)

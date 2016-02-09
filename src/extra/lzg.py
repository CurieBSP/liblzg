# liblzg python wrapper
#
# Copyright(c) 2016 Intel Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import ctypes

liblzg = ctypes.CDLL('liblzg.so')

class LZGConfig(ctypes.Structure):
    _fields = [
        ('level', ctypes.c_int32),
        ('fast', ctypes.c_int),
    ]

class LZG:

    def __init__(self, level=9, fast=False):
        self.lzg_config = LZGConfig(level=level, fast=False)

    def decompress(self, c_buffer):
        assert (c_buffer != None)
        c_buffer_out = ctypes.create_string_buffer(liblzg.LZG_DecodedSize(c_buffer, len(c_buffer)))
        decoded_size = liblzg.LZG_Decode(c_buffer, len(c_buffer), c_buffer_out, len(c_buffer_out))
        return ctypes.string_at(c_buffer_out, decoded_size)

    def compress(self, c_buffer):
        assert (c_buffer != None)
        c_buffer_out_len = liblzg.LZG_MaxEncodedSize(len(c_buffer))
        assert (c_buffer_out_len > 0)
        c_buffer_out = ctypes.create_string_buffer(c_buffer_out_len)
        encoded_size = liblzg.LZG_Encode(c_buffer, len(c_buffer), c_buffer_out,
                                        len(c_buffer_out), ctypes.byref(self.lzg_config))
        return ctypes.string_at(c_buffer_out, encoded_size)

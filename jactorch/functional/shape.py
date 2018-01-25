# -*- coding: utf-8 -*-
# File   : shape.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 25/01/2018
# 
# This file is part of Jacinle.

import collections
import torch


def concat_shape(*shapes):
    output = []
    for s in shapes:
        if isinstance(s, collections.Sequence):
            output.extend(s)
        else:
            output.append(int(s))
    return tuple(output)


def broadcast(tensor, dim, size):
    assert tensor.size(dim) == 1
    shape = tensor.size()
    return tensor.expand(concat_shape(shape[:dim], size + shape[dim+1:]))


def repeat(tensor, dim, count):
    tensor_shape = tensor.size()
    value = broadcast(tensor.unsqueeze(dim + 1), dim + 1, count)
    return value.view(concat_shape(tensor_shape[:dim], -1, tensor_shape[dim + 1:]))


def repeat_times(tensor, dim, repeats):
    repeats = repeats.data.cpu().numpy()
    outputs = []
    for i in range(tensor.size(dim)):
        outputs.append(broadcast(tensor.narrow(dim, i, 1), dim, int(repeats[i])))
    return torch.cat(outputs, dim=dim)
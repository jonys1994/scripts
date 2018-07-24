# -*- coding:UTF-8 -*-

#! /bin/env python3

import difflib

text1 = """text1:
This module provides classes and functions for comparing sequences,
including HTML, and context and unified diffs.
difflib document v7.4
add string
"""
text1_lines = text1.splitlines()
text2 = """text2:
This module provides classes and functions for comparing sequence,
including HTML, and context and unified diffs.
defflib document v7.5"""
text2_lines = text2.splitlines()
# HtmlDiff是生成美观的html页面比对结果
d = difflib.HtmlDiff()
print(d.make_file(text1_lines, text2_lines))

# Differ是普通的比对结果
#d = difflib.Differ()
#diff = d.compare(text1_lines, text2_lines)
#print('\n'.join(list(diff)))
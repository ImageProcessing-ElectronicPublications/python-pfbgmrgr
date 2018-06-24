#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------
# Copyright 2012, Ulf Röttger
# This file is part of pyBgMrgr.py.
# pyBgMrgr.py is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# pyBgMrgr.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with pyBgMrgr.py. If not, see http://www.gnu.org/licenses/.
#-------------------------------------------------------------------

import sys
import os
from optparse import OptionParser
# checking the pyPDF Module to catch the error, that might occur.
try:
    from pyPdf import PdfFileWriter, PdfFileReader
except NameError:
    print 'Python module pyPdf not installed or in PATH.'
    sys.exit(1)


class Merge:
    def __init__(self, args, opts, parent=None):
        """Parse the args for two or three given paths, initiate the walk
        through the main doc, merging it and saving it to a new file and
        printing thas out."""
        self.verbose = opts.verbose
        if self.verbose:
            print 'Initiated merging the files.'
        if len(args) == 3:
            inDocPath = args[0]
            firstBgPath = args[1]
            secondBgPath = args[2]
            outDoc = self.pagewalker(inDocPath, firstBgPath, secondBgPath)
        else:
            inDocPath = args[0]
            firstBgPath = args[1]
            outDoc = self.pagewalker(inDocPath, firstBgPath)
        outDocPath = self.write(outDoc, inDocPath)
        if self.verbose:
            print '''The resulting file has been saved at:
%s''' % outDocPath
        sys.exit(0)

    def pagewalker(self, inDocPath, firstBgPath, secondBgPath=False):
        """take the main doc and the background paths, check, wether there is a
        second one given or not and walk through the pages of the main document
        and initiate the merging page by page."""
        useSecond = False
        outDoc = PdfFileWriter()
        inDoc = PdfFileReader(file(inDocPath, 'rb'))
        bgDoc0 = PdfFileReader(file(firstBgPath, 'rb'))
        if secondBgPath:
            if self.verbose:
                print 'Using different backgrounds for first and following pages.'
            bgDoc1 = PdfFileReader(file(secondBgPath, 'rb'))
            useSecond = True
        numPages = inDoc.getNumPages()
        for i in range(numPages):
            if useSecond:
                if i == 0:
                    outDoc = self.merge(i, outDoc, inDoc, bgDoc0)
                else:
                    outDoc = self.merge(i, outDoc, inDoc, bgDoc1)
            else:
                outDoc = self.merge(i, outDoc, inDoc, bgDoc0)
            if self.verbose:
                print '.',
        if self.verbose:
            print '''
%i pages have been processed.''' % numPages
        return outDoc

    def merge(self, i, outDoc, inDoc, bgDoc):
        """merge the main doc\'s given page number with the given background
        pdf and add the merged file to the growing new pdf doc."""
        page = inDoc.getPage(i)
        newPage = bgDoc.getPage(0)
        newPage.mergePage(page)
        outDoc.addPage(newPage)
        return outDoc

    def write(self, outDoc, inDocPath):
        """frag the path of the main doc, insert the "_mrgd" marker and puzzle
        it together to write the new merged doc to this new path."""
        filePath, fileNameExt = os.path.split(inDocPath)
        fileName, fileExtension = os.path.splitext(fileNameExt)
        outDocPath = os.path.join(filePath, fileName + '_mrgd' + fileExtension)
        outDocStream = file(outDocPath, 'wb')
        outDoc.write(outDocStream)
        outDocStream.close()
        return outDocPath


pfBgMrgr_manual = '''# Introduction

pfBgMrgr is a CLI tool to merge a multipage document with one or two background files as a digital substitute for preprinted letter paper.
It is designed to be used with the profacto ERP-software from extragroup GmbH (extragroup.de) on the OS X and Windows Version 6.1 or 6.2 platform.

## Requirements

In order to use it Python 2.7 is required, other versions of Python may work as well but are not tested or supported.
In addition the pyPdf module is needed as well. Just place the module filder beside the pfBgMrgr.py file.

Download from here: "https://github.com/mfenniak/pyPdf" or search on the web.

# Usage

python pfBgMrgr.py [Options] Args

Use "python pfBgMrgr.py --help" to show the availabale options. The options "--help" and "--version" will not process any given arguments, but print their information and exit.

You need to provide pfBgMrgr.py with at least two but at most three arguments, otherwise it will exit with an error.

* The first argument is the pdf-file without the background. Take care that it has a completely transparent background otherwise it will hide the background file, avoid fully coloured text fields or tables if the will overlap graphical or textual content of your backgrounds.

* The second argument is the first pdf file for your background. If only this is given it will be used for the entire document.
* The third argument is the optional pdf file to use as background for all pages from second to last. This allows you to use a different Design for the first page than for the following ones.

The backgroundfiles may have more than one page, nonetheless only the first page of both pdf will be used only.

## Pathes

The path to the three files need to be fully qualified paths, or relative to the path where pfBgMrgr.py is executed from.

## Pagesize

You may use a different size for all three files though this is not recommended, there is no scaling automatism or rotation whatsoever implemented and will never be. So for best results use for all three pdfs the same pagesize and layout.

## Performance

Reading, merging and recompiling, and writing a PDF of many pages with possibly high resolution content may take some time depending on your hardware.
'''


def main():
    """parse through the options given, check for enough arguments given and
    initiate the main job with the Merge class above if everything looks ok at
    first glance."""
    usage = 'python pfBgMrgr.py [Options] PathToForeground.pdf PathToFirstPageBackground.pdf PathToSecondPageBAckground'
    version = 'Version 1.1'
    parser = OptionParser(usage=usage)
    parser.add_option(
        '-v',
        '--verbose',
        action='store_true',
        dest='verbose',
        help='pfBgMrgr.py becomes verbose.')
    parser.add_option(
        '--version',
        action='store_true',
        dest='version',
        help='Print version of pfBgMrgr.py')
    parser.add_option(
        '-m',
        '--manual',
        action='store_true',
        dest='manual',
        help='Show manual for usage.')
    (opts, args) = parser.parse_args()
    if opts.version:
        print version
        sys.exit(0)
    if opts.manual:
        print pfBgMrgr_manual
        sys.exit(0)
    if len(args) <= 1:
        parser.error(
            'No documents and/or background files given, please read the manual.')
        sys.exit(1)
    elif len(args) > 4:
        parser.error('Too many arguments given, please read the manual.')
        sys.exit(1)
    else:
        Merge(args, opts)


if __name__ == '__main__':
    main()

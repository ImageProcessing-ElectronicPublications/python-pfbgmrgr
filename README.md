# Introduction

pfBgMrgr is a CLI tool to merge a multipage document with one or two background files as a digital substitute for preprinted letter paper.

It has been designed with profacto CRM|ERP|PPS-software from extragroup GmbH (http://www.extragroup.de/profacto) in mind for OS X. 

A typical scenario is sending a quote or invoice as a pdf file via email instead of hardcopy and have the same appearance as on the typical preprinted letter paper of 1-30 pages. The actual limit of possible pages is set by your hardware.

# Requirements

In order to use it Python 2.7 is required, other versions of Python may work as well but are not tested or supported.

In addition the pyPdf-module is needed, which can easily be installed using "sudo easy_install pyPdf“ from the OS X Terminal or simply put the folder pyPdf into the same path as this script itself for distribution it is the most easy way.

Take a look at https://github.com/mfenniak/pyPdf.

It should work on other Unix flavours and Windows as well if the requirements are met. The whole code has no special OS specific dependencies, but has not been tested on other platforms than OS X 10.7.4.

# Usage

python pfbgmrgr.py [Options] Args

Use "python pfBgMrgr.py --help" to show the availabale options. The options "--help" and "--version" will not process any given arguments, but print their information and exit.

You need to provide pfBgMrgr.py with at least two but at most three arguments, otherwise it will exit with an error. 

* The first argument is the pdf-file without the background. Take care that it has a completely **transparent background** otherwise it will hide the background file, avoid fully coloured text fields or tables if the will overlap graphical or textual content of your backgrounds.

* The second argument is the first pdf file for your background. If only this is given it will be used for the entire document. 
* The third argument is the optional pdf file to use as background for all pages from second to last. This allows you to use a different Design for the first page than for the following ones.

The backgroundfiles may have more than one page, nonetheless the first page of both pdf will be used only.

## Pathes

The paths to the three files need to be fully qualified paths, or relative to the path where pfBgMrgr.py is executed from.

## Pagesize

You may use a different size for all three files though this is not recommended, there is no scaling automatism or rotation whatsoever implemented and will never be. So for best results use for all three PDFs the same pagesize and layout.

## Performance

Reading, merging, recompiling, and writing a pdf file of many pages with possibly high resolution content may take some time depending on your hardware, use the verbose option to see where there might be a bottleneck. 
In general the reading of the files takes most of the time, the merging itself is pretty fast, in fact it does not do much more than concatinating backgroundpage + foregroundpage.
There is no handling of files that outgrow the available RAM.

## What does it not do?

pfBgMrgr.py
* does not do any email magic. 
* does not tidy up the files used and created.
* does not check whether you provide valid PDFs, it will possibly crash or produce more or less funny results.
* cannot write the pdf file to standard out for piping - feel free to implement, can't be too hard ;)
* does not understand if you mix up the order of the two or three files, expect funny results.
* does not irrevocably merge a watermark, if you want to create something like that use other ways of pdf manipulating. The reversion of what pfBgMrgr.py does should be pretty easy for one familiar with pdf.

# What still has to be done ...
 
* switch from optparse to argparse, as optparse is deprecated with Python 2.7
* allow different base path for the doc
* allow custom name for returned file

# Known Issues

None :)

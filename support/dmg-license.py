#! /usr/bin/env python
"""
This script adds a license file to a DMG. Requires Xcode and a plain ascii text
license file.
Obviously only runs on a Mac.

Copyright (C) 2011 Jared Hobbs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import os
import sys
import tempfile
import optparse


class Path(str):
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        os.unlink(self)


def mktemp(dir=None, suffix=''):
    (fd, filename) = tempfile.mkstemp(dir=dir, suffix=suffix)
    os.close(fd)
    return Path(filename)


def main(options, args):
    dmgFile, license_en, license_ja = args
    with mktemp('.') as tmpFile:
        with open(tmpFile, 'w') as f:
            f.write("""data 'LPic' (5000) {
    $"0000 0002 0000 0000 0000 000E 0006 0001"
};\n\n""")
            with open(license_en, 'r') as l:
                f.write('data \'TEXT\' (5002, "English") {\n')
                for line in l:
                    if len(line) < 1000:
                        f.write('    "' + line.strip().replace('"', '\\"') +
                                '\\n"\n')
                    else:
                        for liner in line.split('.'):
                            f.write('    "' +
                                    liner.strip().replace('"', '\\"') +
                                    '. \\n"\n')
                f.write('};\n\n')
            f.write("""data 'STR#' (5002, "English") {
    $"0006 0745 6E67 6C69 7368 0541 6772 6565"
    $"0844 6973 6167 7265 6505 5072 696E 7407"
    $"5361 7665 2E2E 2E7B 4966 2079 6F75 2061"
    $"6772 6565 2077 6974 6820 7468 6520 7465"
    $"726D 7320 6F66 2074 6869 7320 6C69 6365"
    $"6E73 652C 2070 7265 7373 2022 4167 7265"
    $"6522 2074 6F20 696E 7374 616C 6C20 7468"
    $"6520 736F 6674 7761 7265 2E20 2049 6620"
    $"796F 7520 646F 206E 6F74 2061 6772 6565"
    $"2C20 7072 6573 7320 2244 6973 6167 7265"
    $"6522 2E"
};\n\n""")
            with open(license_ja, 'r') as l:
                f.write('data \'TEXT\' (5006, "Japanese") {\n')
                for line in l:
                    if len(line) < 1000:
                        f.write('    "' + line.strip().replace('"', '\\"').decode("SHIFT_JIS").encode("SHIFT_JIS") +
                                '\\n"\n')
                    else:
                        for liner in line.split('.'):
                            f.write('    "' +
                                    liner.strip().replace('"', '\\"').decode("SHIFT_JIS").encode("SHIFT_JIS") +
                                    '. \\n"\n')
                f.write('};\n\n')
            f.write("""data 'STR#' (5006, "Japanese") {
    $"0006 084A 6170 616E 6573 650A 93AF 88D3"
    $"82B5 82DC 82B7 0C93 AF88 D382 B582 DC82"
    $"B982 F108 88F3 8DFC 82B7 82E9 0795 DB91"
    $"B62E 2E2E B496 7B83 5C83 7483 6783 4583"
    $"4783 418E 6797 708B 9691 F88C 5F96 F182"
    $"CC8F F08C 8F82 C993 AF88 D382 B382 EA82"
    $"E98F EA8D 8782 C982 CD81 4183 5C83 7483"
    $"6783 4583 4783 4182 F083 4383 9383 5883"
    $"6781 5B83 8B82 B782 E982 BD82 DF82 C981"
    $"7593 AF88 D382 B582 DC82 B781 7682 F089"
    $"9F82 B582 C482 AD82 BE82 B382 A281 4281"
    $"4093 AF88 D382 B382 EA82 C882 A28F EA8D"
    $"8782 C982 CD81 4181 7593 AF88 D382 B582"
    $"DC82 B982 F181 7682 F089 9F82 B582 C482"
    $"AD82 BE82 B382 A281 42"
};\n\n""")
        os.system('/usr/bin/hdiutil unflatten -quiet "%s"' % dmgFile)
        os.system('%s -a %s -o "%s"' %
                  (options.rez, tmpFile, dmgFile))

        os.system('/usr/bin/hdiutil flatten -quiet "%s"' % dmgFile)
        if options.compression is not None:
            os.system('cp %s %s.temp.dmg' % (dmgFile, dmgFile))
            os.remove(dmgFile)
            if options.compression == "bz2":
                os.system('hdiutil convert %s.temp.dmg -format UDBZ -o %s' %
                          (dmgFile, dmgFile))
            elif options.compression == "gz":
                os.system('hdiutil convert %s.temp.dmg -format ' % dmgFile +
                          'UDZO -imagekey zlib-devel=9 -o %s' % dmgFile)
            os.remove('%s.temp.dmg' % dmgFile)
    print "Successfully added license to '%s'" % dmgFile

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.set_usage("""%prog <dmgFile> <licenseFile> [OPTIONS]
  This program adds a software license agreement to a DMG file.
  It requires Xcode and a plain ascii text <licenseFile>.

  See --help for more details.""")
    parser.add_option(
        '--rez',
        '-r',
        action='store',
        default='/Applications/Xcode.app/Contents/Developer/Tools/Rez',
        help='The path to the Rez tool. Defaults to %default'
    )
    parser.add_option(
        '--compression',
        '-c',
        action='store',
        choices=['bz2', 'gz'],
        default=None,
        help='Optionally compress dmg using specified compression type. '
             'Choices are bz2 and gz.'
    )
    options, args = parser.parse_args()
    cond = not os.path.exists(options.rez)
    if cond:
        parser.print_usage()
        sys.exit(1)
    main(options, args)

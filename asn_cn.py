#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from html.parser import HTMLParser
import re
import urllib.request
import operator
from functools import reduce
import argparse

# ---- configs ----
_version = '1.0'
_datas_source_ipip = 'https://whois.ipip.net/countries/CN'
_datas_source_apnic = 'https://ftp.apnic.net/stats/apnic/delegated-apnic-latest'
_datas_source_he = 'https://bgp.he.net/country/CN'
_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'}
# ---- end ----


def main(args):
    CN_ASN = set()

    # load he
    if 'he' in args.source:
        table = get_table_from_url(_datas_source_he)
        table = reduce(operator.add, table)
        for item in table:
            if re.match(r'AS(\d+)', item):
                CN_ASN.add(int(item.strip('AS')))

    # load ipip
    if 'ipip' in args.source:
        table = get_table_from_url(_datas_source_ipip)
        table = reduce(operator.add, table)
        for item in table:
            if re.match(r'AS(\d+)', item):
                CN_ASN.add(int(item.strip('AS')))

    # load apnic
    if 'apnic' in args.source:
        response = urllib.request.urlopen(_datas_source_apnic)
        html = response.read().decode('utf-8')
        results = re.findall('apnic\|CN\|asn\|(\d+?)\|', html, re.S)
        for item in results:
            CN_ASN.add(int(item))

    # generate asn_cn.conf
    CN_ASN = sorted(CN_ASN)
    data_str = 'define china_asn = [\n'
    for index, asn in enumerate(CN_ASN):
        line = str(asn) + ('\n' if (index == len(CN_ASN)-1) else ',\n')
        data_str += line
    data_str += '];'
    with open(args.output, 'w') as file:
        file.write(data_str)


def do_request(url):
    return urllib.request.urlopen(urllib.request.Request(url=url, headers=_headers))


def get_table_from_url(url, index=0):
    response = do_request(_datas_source_he)
    html = response.read().decode('utf-8')
    p = HTMLTableParser()
    p.feed(html)
    return p.tables[index]

# -----------------------------------------------------------------------------
# Name:        html_table_parser
# Purpose:     Simple class for parsing an (x)html string to extract tables.
#              Written in python3
#
# Author:      Josua Schmid
#
# Created:     05.03.2014
# Copyright:   (c) Josua Schmid 2014
# Licence:     AGPLv3
# -----------------------------------------------------------------------------


class HTMLTableParser(HTMLParser):
    """ This class serves as a html table parser. It is able to parse multiple
    tables which you feed in. You can access the result per .tables field.
    """

    def __init__(
        self,
        decode_html_entities=False,
        data_separator=' ',
    ):

        HTMLParser.__init__(self, convert_charrefs=decode_html_entities)

        self._data_separator = data_separator

        self._in_td = False
        self._in_th = False
        self._current_table = []
        self._current_row = []
        self._current_cell = []
        self.tables = []
        self.named_tables = {}
        self.name = ""

    def handle_starttag(self, tag, attrs):
        """ We need to remember the opening point for the content of interest.
        The other tags (<table>, <tr>) are only handled at the closing point.
        """
        if tag == "table":
            name = [a[1] for a in attrs if a[0] == "id"]
            if len(name) > 0:
                self.name = name[0]
        if tag == 'td':
            self._in_td = True
        if tag == 'th':
            self._in_th = True

    def handle_data(self, data):
        """ This is where we save content to a cell """
        if self._in_td or self._in_th:
            self._current_cell.append(data.strip())

    def handle_endtag(self, tag):
        """ Here we exit the tags. If the closing tag is </tr>, we know that we
        can save our currently parsed cells to the current table as a row and
        prepare for a new row. If the closing tag is </table>, we save the
        current table and prepare for a new one.
        """
        if tag == 'td':
            self._in_td = False
        elif tag == 'th':
            self._in_th = False

        if tag in ['td', 'th']:
            final_cell = self._data_separator.join(self._current_cell).strip()
            self._current_row.append(final_cell)
            self._current_cell = []
        elif tag == 'tr':
            self._current_table.append(self._current_row)
            self._current_row = []
        elif tag == 'table':
            self.tables.append(self._current_table)
            if len(self.name) > 0:
                self.named_tables[self.name] = self._current_table
            self._current_table = []
            self.name = ""


class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string


if __name__ == "__main__":
    def fmt(prog): return CustomHelpFormatter(prog)
    parser = argparse.ArgumentParser(formatter_class=fmt,
                                     description='Generate China ASN list for BIRD.')
    parser.add_argument('-o', '--output',  metavar="<file>", default='asn_cn.conf',
                        help='write to file(default: asn_cn.conf)')
    parser.add_argument('-s', '--source', choices=['apnic', 'he', 'ipip'], default=['apnic', 'he', 'ipip'], nargs='*',
                        help='multiple sources can be used at the same time (default: apnic he ipip)')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s '+_version)
    args = parser.parse_args()
    main(args)

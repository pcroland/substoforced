#!/usr/bin/env python3

import argparse
import os
import re
import sys
from copy import copy

import pysrt
from rich import print

prog_name = 'substoforced'
prog_version = '1.0.1'


class RParse(argparse.ArgumentParser):
    def _print_message(self, message, file=None):
        if message:
            if message.startswith('usage'):
                message = f'[bold cyan]{prog_name}[/bold cyan] {prog_version}\n\n{message}'
                message = re.sub(r'(-[a-z]+\s*|\[)([A-Z]+)(?=]|,|\s\s|\s\.)', r'\1[{}]\2[/{}]'.format('bold color(231)', 'bold color(231)'), message)
                message = re.sub(r'((-|--)[a-z]+)', r'[{}]\1[/{}]'.format('green', 'green'), message)
                message = message.replace('usage', f'[yellow]USAGE[/yellow]')
                message = message.replace('options', f'[yellow]FLAGS[/yellow]', 1)
                message = message.replace(self.prog, f'[bold cyan]{self.prog}[/bold cyan]')
            message = f'[not bold white]{message.strip()}[/not bold white]'
            print(message)


class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string


parser = RParse(
    add_help=False,
    formatter_class=lambda prog: CustomHelpFormatter(prog)
)
parser.add_argument('-h', '--help',
                    action='help',
                    default=argparse.SUPPRESS,
                    help='show this help message.')
parser.add_argument('-v', '--version',
                    action='version',
                    version=f'[bold cyan]{prog_name}[/bold cyan] [not bold white]{prog_version}[/not bold white]',
                    help='show version.')
parser.add_argument('-s', '--sub',
                    default=argparse.SUPPRESS,
                    help='specifies srt input')
parser.add_argument('-f', '--folder',
                    metavar='DIR',
                    default=None,
                    help='specifies a folder where [bold color(231)]SubsMask2Img[/bold color(231)] generated timecodes (optional)\nyou should remove the junk from there manually')
args = parser.parse_args()


def print_exit(message):
    print(f'[color(231) on red]ERROR:[/color(231) on red] {message}')
    sys.exit(1)

def main():
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.sub): print_exit(f'{args.sub} doesn\'t exist.')
    print(f'Extracting forced cues from [bold cyan]{args.sub}[/bold cyan][not bold white]...[/not bold white]',)
    sub = pysrt.open(args.sub)

    if args.folder:
        if not os.path.isdir(args.folder): print_exit(f'{args.folder} is not a directory.')
        timecodes = os.listdir(args.folder)

        timecodes_tuple = []

        for timecode in timecodes:
            timecode = os.path.splitext(timecode)[0]
            timecode = timecode.split('__')
            timecode[0] = tuple(timecode[0].split('_'))
            timecode[1] = tuple(timecode[1].split('_'))
            timecodes_tuple.append(timecode)

    for cue in copy(sub):
        # keep uppercase cues
        if cue.text.isupper():
            continue

        skip = False
        # keep overlapping cues
        if args.folder:
            for timecode in timecodes_tuple:
                tc_start = timecode[0]
                tc_start = tuple(map(int, tc_start))
                tc_end = timecode[1]
                tc_end = tuple(map(int, tc_end))
                if tc_start < cue.start < tc_end:
                    skip = True
                    break
                if tc_start < cue.end < tc_end:
                    skip = True
                    break
                if cue.start < tc_start and cue.end > tc_end:
                    skip = True
                    break

        if not skip: sub.remove(cue)

    # renumber indexes
    sub.clean_indexes()

    # saving sub
    output_name = f'{os.path.splitext(os.path.basename(args.sub))[0]}_forced.srt'
    print(f'Saving [bold cyan]{output_name}[/bold cyan], contains [bold cyan]{len(sub)}[/bold cyan] cues[not bold white]...[/not bold white]')
    sub.save(os.path.join(os.getcwd(), output_name), encoding='utf-8')

if __name__ == '__main__':
    main()

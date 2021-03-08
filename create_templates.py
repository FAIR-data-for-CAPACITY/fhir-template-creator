#! /usr/bin/env python3

import json
from pathlib import Path
from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.formatters import Terminal256Formatter
from pprint import pformat

import click


def pprint(obj):
    json_string = json.dumps(obj, indent=INDENT)
    click.echo(highlight(json_string, JsonLexer(), Terminal256Formatter()))


ROOT_DIR = Path.cwd()
EXAMPLES = 'examples'
DEFAULT_EXAMPLES_DIR = ROOT_DIR / EXAMPLES
TEMPLATES_DIR = ROOT_DIR / 'templates'
ONE_UP = 'u'
INDENT = 2
CREATE_VARIABLE = 'v'
EXIT = 'x'


@click.command()
@click.argument('examples_path', type=str, default=DEFAULT_EXAMPLES_DIR)
def main(examples_path):
    examples_path = Path(examples_path)
    if examples_path.is_dir():
        examples = examples_path.iterdir()
    else:
        # Assume it's a single example file
        examples = [examples_path]

    TEMPLATES_DIR.mkdir(exist_ok=True)

    for f in examples:
        create_template(f)


def create_template(example_file):
    with example_file.open('r') as f:
        content = json.load(f)

    current_root = content
    json_path = []

    while True:
        click.echo('\n\n Current (sub)tree:')

        pprint(current_root)
        options = get_options(current_root)
        echo_options(options)

        choice = click.prompt('key').lower()

        print(choice)
        # User has not chosen a key, go up one level
        if choice == 'u':
            json_path.pop(-1)
            current_root = get_subtree(content, json_path)
            continue
        elif choice == CREATE_VARIABLE:
            variable_name = click.prompt(f'Jinja2 variable name (default is {current_root} ', default=current_root)
            jinja_variable = to_jinja_variable(variable_name)

            # Go up one level
            variable_key = json_path.pop(-1)
            current_root = get_subtree(content, json_path)

            # Replace example value with template variable
            current_root[variable_key] = jinja_variable
        elif choice == EXIT:
            break
        else:
            choice = int(choice)
            key = options[choice]
            json_path.append(key)

            # Go a level deeper
            current_root = current_root[key]

    write_template(example_file.name, content)


def write_template(filename, content):
    click.echo('The following template will be written to file:')
    click.echo(json.dumps(content, indent=INDENT))

    with (TEMPLATES_DIR / filename).open('w') as f:
        json.dump(content, f)


def to_jinja_variable(name):
    return '{{' + name + '}}'


def get_subtree(tree, json_path):
    # Clone json path so we don't modify original list
    json_path = list(json_path)

    while json_path:
        key = json_path.pop(0)
        tree = tree[key]

    return tree


def get_options(json_content):
    if isinstance(json_content, dict):
        return list(json_content.keys())
    elif isinstance(json_content, list):
        return range(len(json_content))
    else:
        return []


def echo_options(options):
    for idx, option in enumerate(options):
        click.echo(f'{idx}: {option}')

    click.echo('Press u to go up one level')
    click.echo('Press v to create variable')
    click.echo('Press x to save and go to next profile')


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from subprocess import call
from mind_matter_api.seeds import seed_database

import click

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-c/-C",
    "--coverage/--no-coverage",
    default=True,
    is_flag=True,
    help="Show coverage report",
)
@click.option(
    "-k",
    "--filter",
    default=None,
    help="Filter tests by keyword expressions",
)
@click.argument("pytest_args", nargs=-1)
def test(coverage, filter, pytest_args):
    """Run the tests."""
    import pytest

    args = [TEST_PATH, "--verbose"]
    if coverage:
        args.append("--cov=mind_matter_api")
    if filter:
        args.extend(["-k", filter])
    args.extend(pytest_args)
    rv = pytest.main(args=args)
    print(f"Pytest arguments: {args}")  
    
    exit(rv)


@click.command()
@click.option(
    "-f",
    "--fix-imports",
    default=True,
    is_flag=True,
    help="Fix imports using isort, before linting",
)
@click.option(
    "-c",
    "--check",
    default=False,
    is_flag=True,
    help="Don't make any changes to files, just confirm they are formatted correctly",
)
def lint(fix_imports, check):
    """Lint and check code style with black, flake8 and isort."""
    skip = ["node_modules", "requirements", "migrations"]
    root_files = glob("*.py")
    root_directories = [
        name for name in next(os.walk("."))[1] if not name.startswith(".")
    ]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip
    ]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo(f"{description}: {' '.join(command_line)}")
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    isort_args = []
    black_args = []
    if check:
        isort_args.append("--check")
        black_args.append("--check")
    if fix_imports:
        execute_tool("Fixing import order", "isort", *isort_args)
    execute_tool("Formatting style", "black", *black_args)
    execute_tool("Checking code style", "flake8")


@click.command()
@click.option("--users", default=10, help="Number of users to seed")
@click.option("--recipes", default=3, help="Number of recipes per user")
def seed(users, recipes):
    """Seed the database with mock data."""
    result = seed_database(users, recipes)
    click.echo(result)
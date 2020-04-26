import subprocess
from loguru import logger

def run(*args):
    return subprocess.check_call(['git'] + list(args))

def commit(message):
    run("add", ".")
    run("commit", "-m", message)
    run("push", "origin", "master")


def branch(branch_name):

    run("checkout", "-b", f'analysis_{branch_name}')
    run("push", "-u", "origin", f'analysis_{branch_name}')


def add_submodule(repo_name, user='dezeraecox-experiments', local_path='experimental_data/'):
    subprocess.Popen(['git', 'submodule', 'add', f'https://github.com/{user}/{repo_name}.git', f'{local_path}{repo_name}'])


def add_submodule_branches(branch_name):
    run('submodule', "foreach", "git", "checkout",
        "-b", f'analysis_{branch_name}')
    run('submodule', "foreach", "git", "push",
        "-u", "origin", f'analysis_{branch_name}')


def create_submodules(repositories, branch_name):

    for repository in repositories:
        add_submodule(repo_name=repository)

    commit("Adding submodules")
    add_submodule_branches(branch_name)

    logger.info(f'Submodules created and set to branch {branch_name}')

"""--------------------------------------------------------------------"""
"""
Automate the process of collecting experiments as submodules into an analysis folder, then create a new branch for the combined analysis.
"""

repositories = [
    'experiment',
    'EXP110_Hsp70-recombinant-client-unfolding',
    'EXP100_Urea-unfolding-Blac-TRP-TPEMI'
]

branch_name = 'test'

create_submodules(repositories, branch_name)

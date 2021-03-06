import argparse
import logging

from .env import gen_requirements, gen_virt_env, check_path_exist

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(
    description="""
        A tool for automatically migrating any python source code to a
        virtual environment with all dependencies automatically identified
        and installed. You can also use this tool to generate requirements.txt
        for your python code base, in general, this tool will help you to
        bring your old/hobby python codebase to production/distribution.
    """
)
parser.add_argument(
    "source", type=str,
    help="Path to source directory where you have the codebase to transform"
)
parser.add_argument(
    "target", type=str,
    help="Path to the destination where you need to generate a " +
    "virtual-environment or requirements.txt"
)
parser.add_argument(
    "--requirements", action="store_true", required=False,
    default=False,
    help="This flag tells the tool to generate requirements.txt"
)
parser.add_argument(
    "--syspkgs", action="store_true", required=False,
    default=False,
    help="Set this flag, if you want to use system site-packages " +
    "In other words, you will re-use the packages available on the system" +
    " instead of downloading them locally in the virtualenv."
)
parser.add_argument(
    "--symlink", action="store_true", required=False,
    default=False,
    help="Symlinks the python interpreter available on the system" +
    " rather than installing a new one."
)


def main():
    args = parser.parse_args()

    target = args.target
    source = args.source

    if not check_path_exist(target, check_abs=True):
        logging.error("Target {} not found".format(target))
        return

    if not check_path_exist(source):
        logging.error("Source {} not found".format(source))
        return

    if args.requirements:
        gen_requirements(source, target)
    else:
        options = {
            "system_site_packages": args.syspkgs,
            "symlinks": args.symlink
        }
        gen_virt_env(target, source, options)


if __name__ == "__main__":
    main()

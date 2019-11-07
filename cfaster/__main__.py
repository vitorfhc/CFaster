import logging
from click import Choice, group, command, option, argument, version_option

from .scrapers.codeforces import codeforces_scraper as cf_scraper
from . import __version__

logger = logging.getLogger(__name__)

target_scraper = {
    'cf': cf_scraper,
}

targets = [key for key in target_scraper.keys()]


def set_log_levels(level=logging.WARNING):
    format_ = '[%(levelname)s]: %(message)s'
    logging.basicConfig(level=level, format=format_)
    logger.info('Level of logs set to ' +
                logging.getLevelName(logger.getEffectiveLevel()))


@group()
@option('-v', '--verbose', is_flag=True, help='Output INFO level logs.')
@version_option(__version__, message='%(version)s')
def main_cmd(verbose):
    if verbose:
        set_log_levels(logging.INFO)
    else:
        set_log_levels()


@main_cmd.command(
    short_help='Scrapes the problem and saves inputs and outputs.'
)
@argument('url')
@option('-t', '--target', default=targets[0],
        show_default=True, type=Choice(targets),
        help='Website you are targeting to scrape.')
def scrape(url, target):
    logger.info('Running scrape command')
    target_scraper[target](url)


if __name__ == '__main__':
    main_cmd()

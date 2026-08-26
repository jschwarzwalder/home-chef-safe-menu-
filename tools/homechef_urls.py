"""Generate Home Chef weekly menu API URLs."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta


BASE_URL = "https://www.homechef.com/api/v3/menus/{date}/standard/meals"
DATE_FORMAT = "%d-%b-%Y"


def parse_date(value: str) -> date:
    """Parse a Home Chef date such as 31-aug-2026."""
    try:
        return datetime.strptime(value.lower(), DATE_FORMAT).date()
    except ValueError as exc:
        raise ValueError(
            f"Invalid date '{value}'. Expected format DD-mon-YYYY, "
            "for example 31-aug-2026."
        ) from exc


def next_monday(start_date: date) -> date:
    """Return start_date if Monday, otherwise the following Monday."""
    days_until_monday = (7 - start_date.weekday()) % 7
    return start_date + timedelta(days=days_until_monday)


def get_starting_monday(given_date: date | None = None) -> date:
    """Determine the Monday from which URL generation should begin.

    If no date is supplied, use today's date and find the next Monday.
    If the supplied date is already Monday, use that date.
    Otherwise, use the following Monday.
    """
    if given_date is None:
        given_date = date.today()

    return next_monday(given_date)


def generate_dates(starting_monday: date, weeks: int) -> list[date]:
    """Generate consecutive Mondays for the requested number of weeks."""
    if weeks < 1:
        raise ValueError("weeks must be at least 1.")

    return [
        starting_monday + timedelta(weeks=offset)
        for offset in range(weeks)
    ]


def format_date(menu_date: date) -> str:
    """Format a date exactly as Home Chef expects."""
    return menu_date.strftime(DATE_FORMAT).lower()


def generate_url(menu_date: date) -> str:
    """Generate the Home Chef menu API URL for a date."""
    return BASE_URL.format(date=format_date(menu_date))


def generate_urls(
    given_date: date | None = None,
    weeks: int = 1,
) -> list[tuple[date, str]]:
    """Generate Home Chef menu URLs starting from the appropriate Monday."""
    starting_monday = get_starting_monday(given_date)
    dates = generate_dates(starting_monday, weeks)

    return [(menu_date, generate_url(menu_date)) for menu_date in dates]


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate Home Chef weekly menu API URLs."
    )

    parser.add_argument(
        "date",
        nargs="?",
        help=(
            "Starting date in DD-mon-YYYY format. "
            "If omitted, the next Monday is used."
        ),
    )

    parser.add_argument(
        "--weeks",
        type=int,
        default=1,
        help="Number of weekly URLs to generate (default: 1).",
    )

    return parser


def main() -> int:
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        given_date = parse_date(args.date) if args.date else None
        results = generate_urls(given_date, args.weeks)
    except ValueError as exc:
        parser.error(str(exc))

    print(f"Starting Monday: {format_date(results[0][0])}")
    print(f"Weeks: {len(results)}")
    print()

    for menu_date, url in results:
        print(format_date(menu_date))
        print(url)
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
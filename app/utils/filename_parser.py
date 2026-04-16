from typing import Optional, Tuple


TAG_CATEGORY_COLORS = {
    'year': '220 10% 50%',
    'genre': '210 70% 50%',
    'quality': '150 60% 40%',
    'custom': '270 60% 55%',
}


RESOLUTION_MAP = {
    '2160p': '4K',
    '4k': '4K',
    'uhd': '4K',
    '1080p': '1080p',
    '1080i': '1080p',
    '720p': '720p',
    '480p': '480p',
}


class ParsedFilename:
    def __init__(self, year: Optional[int] = None, resolution: Optional[str] = None, tags: list = None):
        self.year = year
        self.resolution = resolution
        self.tags = tags or []


def parse_filename(filename: str) -> ParsedFilename:
    tags = []
    year = None
    resolution = None

    # Extract year (1900-2099)
    import re
    year_match = re.search(r'[\.\s\-\(]?((?:19|20)\d{2})[\.\s\-\)]', filename)
    if year_match:
        year = int(year_match.group(1))
        tags.append(str(year))

    # Extract resolution
    lower_name = filename.lower()
    for pattern, label in RESOLUTION_MAP.items():
        if pattern in lower_name:
            resolution = label
            tags.append(label)
            break

    return ParsedFilename(year=year, resolution=resolution, tags=tags)


def get_tag_category_for_name(name: str) -> Tuple[str, str]:
    import re
    if re.match(r'^(19|20)\d{2}$', name):
        return 'year', TAG_CATEGORY_COLORS['year']
    if name in ['4K', '1080p', '720p', '480p']:
        return 'quality', TAG_CATEGORY_COLORS['quality']
    return 'custom', TAG_CATEGORY_COLORS['custom']
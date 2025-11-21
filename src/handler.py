import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Media:
    title: str
    director: str
    cast: List[str]
    code: int
    date: datetime
    media_type: str
    tags: List[str]


def load_media_from_json(db_path: str) -> List[Media]:
    """Load media list from a JSON file."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Media")
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    media_list = [
        Media(
            title=row[column_names.index('Title')],
            director=row[column_names.index('Director')],
            cast=row[column_names.index('Cast')].split(', '),
            code=row[column_names.index('ID')],
            date=datetime.fromisoformat(row[column_names.index('Date')]),
            media_type=row[column_names.index('Type')].split(', '),
            tags=row[column_names.index('Tags')]
        )
        for row in data
    ]
    return media_list


def update_db(player, column: str, value: str):
    conn = sqlite3.connect(player.db_path)
    cursor = conn.cursor()

    for med in player.media:
        if med.code == player.selected_media.code:
            if column == 'Title':
                med.title = value
            elif column == 'Director':
                med.director = value
            elif column == 'Cast':
                med.cast = value
            elif column == 'Tags':
                med.tags = value

    query = f"""
        UPDATE Media
        SET {column} = '{value}'
        WHERE ID = {player.selected_media.code};
    """
    cursor.execute(query)

    conn.commit()
    conn.close()

    player.selector_panel.populate_selector()

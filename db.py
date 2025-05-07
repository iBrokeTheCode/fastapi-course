from typing import List

from schemas import BookCreate

sample_books: List[BookCreate] = [
    BookCreate(
        id=1,
        title="The Hitchhiker's Guide to the Galaxy",
        author="Douglas Adams",
        publisher="Pan Books",
        published_date="1979-10-12",
        page_count=224,
        language="English",
    ),
    BookCreate(
        id=2,
        title="Pride and Prejudice",
        author="Jane Austen",
        publisher="T. Egerton",
        published_date="1813-01-28",
        page_count=432,
        language="English",
    ),
    BookCreate(
        id=3,
        title="Cien años de soledad",
        author="Gabriel García Márquez",
        publisher="Editorial Sudamericana",
        published_date="1967",
        page_count=417,
        language="Spanish",
    ),
    BookCreate(
        id=4,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publisher="George Allen & Unwin",
        published_date="1954-07-29",
        page_count=1216,
        language="English",
    ),
    BookCreate(
        id=5,
        title="Le Petit Prince",
        author="Antoine de Saint-Exupéry",
        publisher="Reynal & Hitchcock",
        published_date="1943-04-06",
        page_count=96,
        language="French",
    ),
    BookCreate(
        id=6,
        title="Foundation",
        author="Isaac Asimov",
        publisher="Gnome Press",
        published_date="1951",
        page_count=255,
        language="English",
    ),
    BookCreate(
        id=7,
        title="La Divina Commedia",
        author="Dante Alighieri",
        publisher="Various (first edition self-published)",
        published_date="1472",
        page_count=640,
        language="Italian",
    ),
]

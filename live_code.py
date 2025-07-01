import os
import json
import functools
import urllib.parse
from livereload import Server
from dotenv import load_dotenv
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader


TEMPLATE_PATH = "template.html"
META_DATA_PATH = "media/meta_data.json"
BOOTSTRAP_PATH = "../static/bootstrap.min.css"
BOOTSTRAP_JS_PATH = "../static/bootstrap.bundle.min.js"
SERVER_PORT = 5507
AMOUNT_PAGE = 20


def load_books():
    with open(META_DATA_PATH, "r", encoding="utf-8") as file:
        books = json.load(file)

    data_dir = os.path.dirname(os.path.abspath(META_DATA_PATH))

    for book in books:
        if 'img_src' in book:
            img_path = os.path.normpath(os.path.join(data_dir, book["img_src"]))
            rel_img_path = os.path.relpath(img_path, "pages")
            book["img_src"] = rel_img_path.replace(os.sep, "/")

        if 'book_path' in book:
            book_path = os.path.normpath(os.path.join(data_dir, book["book_path"]))
            rel_book_path = os.path.relpath(book_path, "pages")
            parts = rel_book_path.split(os.sep)
            parse_parts = [urllib.parse.quote(part) for part in parts]
            book['book_path'] = '/'.join(parse_parts)
    return books


def create_pages(books, template, bootstrap_path, bootstrap_js_path, page_size=AMOUNT_PAGE):
    pages = list(chunked(books, page_size))
    total_pages = len(pages)
    os.makedirs("pages", exist_ok=True)

    for index, page_books in enumerate(pages, start=1):
        books_pairs = list(chunked(page_books, n=2))
        prev_page = f"index{index - 1}.html" if index > 1 else None
        next_page = f"index{index + 1}.html" if index < total_pages else None
        rendered_html = template.render(
            books_pairs=books_pairs,
            current_page=index,
            total_pages=total_pages,
            prev_page=prev_page,
            next_page=next_page,
            bootstrap_path=bootstrap_path,
            bootstrap_js_path=bootstrap_js_path
        )
        print(bootstrap_path)
        page_filename = f"pages/index{index}.html"
        with open(page_filename, "w", encoding="utf-8") as file:
            file.write(rendered_html)


def render_website(bootstrap_path, bootstrap_js_path):
    books = load_books()
    env = Environment(loader=FileSystemLoader("."), autoescape=True)
    template = env.get_template(TEMPLATE_PATH)
    create_pages(books, template, bootstrap_path, bootstrap_js_path, page_size=AMOUNT_PAGE)


def refresh(bootstrap_path, bootstrap_js_path):
    render_website(bootstrap_path, bootstrap_js_path)


def main():
    load_dotenv()
    bootstrap_path = os.getenv('BOOTSTRAP_PATH', BOOTSTRAP_PATH)
    bootstrap_js_path = os.getenv('BOOTSTRAP_JS_PATH', BOOTSTRAP_JS_PATH)
    render_website(bootstrap_path, bootstrap_js_path)

    reload_handler = functools.partial(refresh, bootstrap_path, bootstrap_js_path)

    server = Server()
    server.watch(TEMPLATE_PATH, reload_handler)
    server.watch(META_DATA_PATH, reload_handler)
    server.serve(root='.', port=SERVER_PORT)


if __name__ == "__main__":
    main()

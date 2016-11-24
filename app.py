import json
import os
import markdown2
from jinja2 import Environment, FileSystemLoader


def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def write_to_html_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def get_converted_markdown_to_html_text(data):
    return markdown2.markdown(data)


def create_if_not_exists_html_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_html_page(name, data, title1):
    name1 = name.split("\\")[-1]
    root1 = name.replace("articles", "static").replace(name1, "")
    name1 = name1.replace(".md", ".html")
    create_if_not_exists_html_folder(root1)
    template = get_template()
    output_from_parsed_template = template.render(bootstrap_folder="../../static/css/bootstrap.min.css",
                                                  articles=data,
                                                  article_name=title1)
    create_if_not_exists_html_folder(root1)
    write_to_html_file('{}\{}'.format(root1, name1), output_from_parsed_template)


def get_template():
    env = Environment(loader=FileSystemLoader('templates'))
    return env.get_template('template.html')


def get_article_name_from_congig():
    with open("config.json", "r", encoding="utf-8") as f:
        data = f.read()
    d = json.loads(data)
    return d


if __name__ == "__main__":
    articles = r"{}\articles".format(os.getcwd())

    d = get_article_name_from_congig()
    for i in d["articles"]:
        title = i["title"]
        file = "{0}\\{1}".format(articles, (i["source"].replace('/', '\\')))
        data_t = load_text(file)
        converted_html = get_converted_markdown_to_html_text(data_t)
        create_html_page(file, converted_html, title)
    print("Successful completed!")

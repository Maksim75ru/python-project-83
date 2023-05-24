def get_data_from_html(html: object) -> tuple[str]:
    h1 = html.h1.get_text() if html.h1 else ''
    title = html.title.get_text() if html.title else ''
    description = html.find('meta', {'name': 'description'})
    description_content = description['content'] if description else ''

    return h1, title, description_content

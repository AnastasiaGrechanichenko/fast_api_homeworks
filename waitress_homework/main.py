from waitress import serve
import html




def app(environ, start_response):
    method = environ.get('REQUEST_METHOD','')
    path = environ.get('PATH_INFO','')
    query = environ.get('QUERY_STRING','')
    ip = environ.get('REMOTE_ADDR','')
    protocol = environ.get('SERVER_PROTOCOL','')
    host = environ.get('HTTP_HOST','')
    agent = environ.get('HTTP_USER_AGENT','')
    referer = environ.get('HTTP_REFERER','')

    html_content = """<!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><title>Информация о запросе</title>
    <style>
    body { font-family: sans-serif; margin: 40px; background: #eee; }
    table { background: white; border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
    th { background: #EDFF21; color: red; }
    </style>
    </head>
    <body>
    <h1>Данные запроса</h1>
    <table>
    """
    html_content += f"<tr><th>Метод</th><td>{html.escape(method)}</td></tr>"
    html_content += f"<tr><th>Путь (PATH_INFO)</th><td>{html.escape(path)}</td></tr>"
    html_content += f"<tr><th>Query строка</th><td>{html.escape(query)}</td></tr>"
    html_content += f"<tr><th>IP клиента</th><td>{html.escape(ip)}</td></tr>"
    html_content += f"<tr><th>Протокол</th><td>{html.escape(protocol)}</td></tr>"
    html_content += f"<tr><th>Хост</th><td>{html.escape(host)}</td></tr>"
    html_content += f"<tr><th>User-Agent</th><td>{html.escape(agent)}</td></tr>"
    html_content += f"<tr><th>Referer</th><td>{html.escape(referer)}</td></tr>"

    for key,value in environ.items():
        if key.startswith('HTTP_') and key not in('HTTP_HOST','HTTP_USER_AGENT','HTTP_REFERER'):
            html_content+= f"<tr><th>{key}</th><td> {html.escape(str(value))}</td></tr>"

    html_content += """
    </table>
    </body>
    </html> """

    start_response("200 OK", [("Content-Type","text/html; charset=utf-8")])

    body_in_bytes = html_content.encode('utf-8')
    return [body_in_bytes]



if __name__ == '__main__':
    serve(app)
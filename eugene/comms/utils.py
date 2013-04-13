import time

from flask import current_app

from eugene.comms.models import Message
from eugene.database import get_session


class InvalidFormat(Exception):
    pass


def get_date(t):
    return time.strftime('%c', time.localtime(t))


def get_time(t):
    return time.strftime('%H:%M:%S', time.localtime(t))


class Writer(object):
    def __init__(self, filename):
        self.filename = filename
        self.lines = []

    def begin(self):
        pass

    def writeln(self, msg):
        pass

    def end(self):
        fp = open(self.filename, 'w')
        fp.write('\n'.join(self.lines))
        fp.close()


class HTMLWriter(Writer):
    def begin(self):
        super(HTMLWriter, self).begin()
        # Ew.
        self.lines.append('<!DOCTYPE html>')
        self.lines.append('<html>')
        self.lines.append('<head>')
        self.lines.append('<meta charset="UTF-8">')
        self.lines.append(
            '<style>'
            'table {width: 100%; border: 1px;}'
            'td {padding: 0.5em; border-bottom: 1px solid #ccc;}'
            'td.text {width: 70%;}'
            '</style>')
        self.lines.append('</head>')
        self.lines.append(
            '<body><table>'
            '<tr><th>time</th><th>sender</th><th>recipient</th><th>text</th>')

    def writeln(self, msg):
        self.lines.append(
            '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td class="text">{3}</td></tr>'.format(
                get_time(msg.created), msg.sender, msg.recipient, msg.text))

    def end(self):
        self.lines.append(
            '</table></body></html>')
        super(HTMLWriter, self).end()


class CSVWriter(Writer):
    def writeln(self, msg):
        self.lines.append(
            ','.join(['"{0}"'.format(part.replace('"', '\\"'))
                      for part in [
                        get_time(msg.created), msg.sender, msg.recipient,
                        msg.text]
            ]))


FORMATTERS = {
    'html': HTMLWriter,
    'csv': CSVWriter
    }


def export_log(output_format):
    try:
        writer_class = FORMATTERS[output_format]
    except KeyError:
        raise InvalidFormat('Output format "{0}" is not valid.'.format(
                output_format))

    filename = 'eugene.{0}'.format(output_format)
    writer = writer_class(filename)
    writer.begin()

    db = get_session(current_app)
    msgs = db.query(Message).order_by(Message.created)
    for msg in msgs:
        writer.writeln(msg)

    writer.end()

    return filename

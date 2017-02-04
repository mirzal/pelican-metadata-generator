import os
import logging
from slugify import slugify

from PyQt5 import (QtCore, QtWidgets)

import FileHandler


class NewPostMetadata(QtCore.QObject):
    changed = QtCore.pyqtSignal()
    fileHasHeaders = QtCore.pyqtSignal()
    def __init__(self):
        super(NewPostMetadata, self).__init__(None)
        self.title = ""
        self.slug = ""
        self.date = ""
        self.modified = ""
        self.category = ""
        self.tags = []
        self.authors = []
        self.summary = ""
        self.file_format = 'markdown'

    def set_title(self, value):
        self.title = value
        self.changed.emit()

    def set_slug(self, value):
        self.slug = value
        self.changed.emit()

    def set_created_date(self, value):
        self.date = value.toString("yyyy-MM-dd hh:mm:ss")
        self.changed.emit()

    def set_modified_date(self, value):
        if value:
            self.modified = value.toString("yyyy-MM-dd hh:mm:ss")
        else:
            self.modified = ""
        self.changed.emit()

    def set_category(self, value):
        self.category = value
        self.changed.emit()

    def add_tag(self, value):
        self.tags.append(value)
        self.changed.emit()

    def remove_tag(self, value):
        self.tags.remove(value)
        self.changed.emit()

    def set_author(self, value):
        if not value:
            self.authors = []
        else:
            self.authors = [value]
        self.changed.emit()

    def set_summary(self, text):
        self.summary = text
        self.changed.emit()

    def to_file(self, filepath):
        self.file = FileHandler.Factory(filepath, self.file_format).generate()

        if self.file.has_metadata():
            self.fileHasHeaders.emit()
        else:
            self.to_file_prepend_headers()

    def to_file_prepend_headers(self):
        self.file.headers = self._format_headers_object()
        self.file.prepend_headers()

    def to_file_overwrite_headers(self):
        self.file.headers = self._format_headers_object()
        self.file.overwrite_headers()

    def _format_headers_object(self):
        headers = {}

        for separator, key in [(", ", "tags"), ("; ", "authors")]:
            value = separator.join(sorted(getattr(self, key), key=str.lower))
            if value:
                headers[key] = value

        for key in ["title", "slug", "date", "modified", "category", "summary"]:
            if getattr(self, key):
                headers[key] = getattr(self, key)

        return headers

    def as_pelican_header(self):
        file_ = FileHandler.Factory("", self.file_format).generate()
        file_.headers = self._format_headers_object()
        return file_.formatted_headers

class MetadataDatabase(QtCore.QObject):
    changed = QtCore.pyqtSignal()
    def __init__(self, path=None):
        super(MetadataDatabase, self).__init__(None)
        self.category = []
        self.tags = []
        self.authors = []
        self.path = []
        self.read_directory(path)

    def read_directory(self, path):
        if not path:
            return

        path = os.path.abspath(path)
        if (os.path.isdir(path)):
            self._readPathFiles(path)
            self.path = path
            self.changed.emit()

    def _readPathFiles(self, path):
        for root, dirs, files in os.walk(path):
            for filename in files:
                self._parseFile(os.path.join(root, filename))

    def _parseFile(self, path):
        logging.debug("Processing {file}".format(file=path))

        try:
            post = FileHandler.Factory(path).generate()
        except NotImplementedError:
            msg = "Ignoring {file} because it has unsupported extension"
            logging.info(msg.format(file=path))
            return

        for header in post.headers:
            if header in ['tags', 'category', 'author', 'authors']:
                self._appendMeta(header, post.headers[header])

    def _appendMeta(self, name, values):
        """
        This takes string that is metadata tag value, makes it a list 
        (separated by semicolon or comma), and appends element from list
        into database of known values for given tag if that value hasn't
        been encountered earlier.
        This way we can be sure that known values in database are unique
        """
        if name == 'author':
            name = 'authors'

        if ';' in values:
            values = values.split(';')
        else:
            values = values.split(',')

        known_values = getattr(self, name)

        # TODO: I guess we don't support empty values? pelican does this a bit different
        values = [v.strip() for v in values]

        for v in values:
            if v and v not in known_values:
                logging.debug("Appending {v} to {n}".format(v=v, n=name))
                known_values.append(v)
                setattr(self, name, known_values)

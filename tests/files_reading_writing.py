import unittest

import os
import io
import logging

import FileHandler


CUR_DIR = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(CUR_DIR, 'posts')

class TestReadingMarkdownFiles(unittest.TestCase):

    def test_read_nonexisting_file(self):
        expected_headers = {}
        expected_content = ""
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_that_doesnt_exist.md"))

        md.read()

        self.assertFalse(md.exists)
        self.assertEqual(md.headers, expected_headers)
        self.assertEqual(md.post_content, expected_content)

    def test_read_file_without_metadata(self):
        expected_headers = {}
        expected_content = "File without headers\n"
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_without_headers.md"))

        md.read()

        self.assertTrue(md.exists)
        self.assertEqual(md.headers, expected_headers)
        self.assertEqual(md.post_content, expected_content)

    def test_read_file_with_metadata(self):
        expected_headers = {
                "title": "File with headers",
                "slug": "file-with-headers",
                "category": "Markdown",
                "tags": "File, Tag, Testing",
            }
        expected_content = "File with headers\n"
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_with_headers.md"))

        md.read()

        self.assertTrue(md.exists)
        self.assertEqual(md.headers, expected_headers)
        self.assertEqual(md.post_content, expected_content)

    def test_read_file_with_metadata_after_text(self):
        expected_headers = {
                "title": "File with metadata in text",
            }
        expected_content = (
                "This is example file with metadata-like line after paragraph of text\n"
                "Slug: file-with-metadata-in-text\n"
                "And one more paragraph\n"
                )
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_with_headers_after_text.md"))

        md.read()

        self.assertTrue(md.exists)
        self.assertEqual(md.headers, expected_headers)
        self.assertEqual(md.post_content, expected_content)

    def test_read_file_with_multiline_metadata(self):
        expected_headers = {
                "title": "File with headers",
                "category": "Markdown",
                "tags": "File; Tag; Testing",
            }
        expected_content = ""
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_with_multiline_metadata.md"))

        md.read()

        self.assertTrue(md.exists)
        self.assertEqual(md.headers, expected_headers)
        self.assertEqual(md.post_content, expected_content)

    def test_read_file_with_YAML_headers(self):
        expected_headers = {
                "title": "File with YAML headers",
                "slug": "file-with-yaml-headers",
                "category": "Markdown",
            }
        expected_content = "This file has YAML-style headers\n"
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_with_YAML_headers.md"))

        md.read()

        self.assertTrue(md.exists)
        self.assertEqual(md.headers, expected_headers)
        self.assertEqual(md.post_content, expected_content)

    def test_read_file_without_separator_between_headers_and_content(self):
        expected_headers = {
                "title": "File without separator after headers",
                "category": "Markdown",
            }
        expected_content = "This file has no separator between headers and content\n"
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_without_separator.md"))

        md.read()

        self.assertTrue(md.exists)
        self.assertEqual(md.headers, expected_headers)
        self.assertEqual(md.post_content, expected_content)

    def test_read_file_with_url_in_first_line_without_separator(self):
        expected_headers = {
                "title": "URL below headers",
            }
        expected_content = "http://miroslaw-zalewski.eu/\n"
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "url_in_first_line.md"))

        md.read()

        self.assertTrue(md.exists)
        self.assertEqual(md.headers, expected_headers)
        self.assertEqual(md.post_content, expected_content)

    def test_read_colon_after_separator(self):
        expected_headers = {
                "title": "File with colon in first line",
                "category": "Markdown",
            }
        expected_content = "Test: This is normal text, not header\n"
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_with_colon_in_first_line.md"))

        md.read()

        self.assertTrue(md.exists)
        self.assertEqual(md.headers, expected_headers)
        self.assertEqual(md.post_content, expected_content)

class TestWritingHeaders(unittest.TestCase):

    def test_markdown_prepend_headers_non_existing_file(self):
        expected = (
                "Title: Sample title\n"
                "Slug: sample-title\n"
                "Date: 2017-02-01 12:00\n"
                "Category: Test category\n"
                "Tags: Another, Tag\n"
                "\n"
                )
        test_stream = io.StringIO()
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_that_doesnt_exist.md"))
        md.read()
        md.headers = {
                "title": "Sample title",
                "slug": "sample-title",
                "date": "2017-02-01 12:00",
                "category": "Test category",
                "tags": "Another, Tag",
                }
        md.prepend_headers_stream(test_stream)

        test_stream.seek(0)

        self.assertEqual(test_stream.read(), expected)

    def test_markdown_overwrite_headers_non_existing_file(self):
        expected = (
                "Title: Sample title\n"
                "Slug: sample-title\n"
                "Date: 2017-02-01 12:00\n"
                "Category: Test category\n"
                "Tags: Another, Tag\n"
                "\n"
                )
        test_stream = io.StringIO()
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_that_doesnt_exist.md"))
        md.read()
        md.headers = {
                "title": "Sample title",
                "slug": "sample-title",
                "date": "2017-02-01 12:00",
                "category": "Test category",
                "tags": "Another, Tag",
                }
        md.overwrite_headers_stream(test_stream)

        test_stream.seek(0)

        self.assertEqual(test_stream.read(), expected)

    def test_markdown_prepend_headers_file_without_headers(self):
        expected = (
                "Title: Sample title\n"
                "Slug: sample-title\n"
                "Date: 2017-02-01 12:00\n"
                "Category: Test category\n"
                "Tags: Another, Tag\n"
                "\n"
                "File without headers\n"
                )
        test_stream = io.StringIO()
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_without_headers.md"))
        md.read()
        md.headers = {
                "title": "Sample title",
                "slug": "sample-title",
                "date": "2017-02-01 12:00",
                "category": "Test category",
                "tags": "Another, Tag",
                }
        md.prepend_headers_stream(test_stream)

        test_stream.seek(0)

        self.assertEqual(test_stream.read(), expected)

    def test_markdown_overwrite_headers_file_without_headers(self):
        expected = (
                "Title: Sample title\n"
                "Slug: sample-title\n"
                "Date: 2017-02-01 12:00\n"
                "Category: Test category\n"
                "Tags: Another, Tag\n"
                "\n"
                "File without headers\n"
                )
        test_stream = io.StringIO()
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_without_headers.md"))
        md.read()
        md.headers = {
                "title": "Sample title",
                "slug": "sample-title",
                "date": "2017-02-01 12:00",
                "category": "Test category",
                "tags": "Another, Tag",
                }
        md.overwrite_headers_stream(test_stream)

        test_stream.seek(0)

        self.assertEqual(test_stream.read(), expected)

    def test_markdown_prepend_headers_file_with_headers(self):
        expected = (
                "Title: Sample title\n"
                "Slug: sample-title\n"
                "Date: 2017-02-01 12:00\n"
                "Category: Test category\n"
                "Tags: Another, Tag\n"
                "\n"
                "Title: File with headers\n"
                "Slug: file-with-headers\n"
                "Category: Markdown\n"
                "Tags: File, Tag, Testing\n"
                "\n"
                "File with headers\n"
                )
        test_stream = io.StringIO()
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_with_headers.md"))
        md.read()
        md.headers = {
                "title": "Sample title",
                "slug": "sample-title",
                "date": "2017-02-01 12:00",
                "category": "Test category",
                "tags": "Another, Tag",
                }
        md.prepend_headers_stream(test_stream)

        test_stream.seek(0)

        self.assertEqual(test_stream.read(), expected)

    def test_markdown_overwrite_headers_file_with_headers(self):
        expected = (
                "Title: Sample title\n"
                "Slug: sample-title\n"
                "Date: 2017-02-01 12:00\n"
                "Category: Test category\n"
                "Tags: Another, Tag\n"
                "\n"
                "File with headers\n"
                )
        test_stream = io.StringIO()
        md = FileHandler.MarkdownHandler(os.path.join(CONTENT_PATH , "file_with_headers.md"))
        md.read()
        md.headers = {
                "title": "Sample title",
                "slug": "sample-title",
                "date": "2017-02-01 12:00",
                "category": "Test category",
                "tags": "Another, Tag",
                }
        md.overwrite_headers_stream(test_stream)

        test_stream.seek(0)

        self.assertEqual(test_stream.read(), expected)

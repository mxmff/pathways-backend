from django.test import TestCase
from newcomers_guide.clean_data import clean_up_http_links, clean_up_email_links, clean_up_newlines

# Need to replace single newlines with space, except when the line before
# and/or after is a list item or heading. This is because the markdown
# component renders newlines as line breaks, see
# https://github.com/mientjan/react-native-markdown-renderer/issues/74

# For the markdown component, one newline means a line break, two newlines
# or more means a paragraph break. So since we are converting one newline
# into space, we need to convert two newlines into one newline and three or
# more newlines into two newlines. To simplify the implementation, two newlines
# separated by all whitespace is converted into just two newlines as a pre-
# processing step.

# Need to replace multiple spaces with a single space, because the markdown
# component renders larger horizontal spaces for multiple space characters.
# However, multiple spaces at the start of a line are not changed

# Need to leave all whitespace following one or more newlines unchanged,
# because this whitespace can be meaningful when formatting nested lists.

# One newline is enough before and after headings. Three or more newlines
# in a row is OK, even when they're interspersed with other whitespace


class CleanUpNewlinesTest(TestCase):
    def test_removes_carriage_returns(self):
        text = 'abc\rdef'
        self.assertEqual(clean_up_newlines(text), 'abcdef')

    def test_removes_duplicate_spaces(self):
        text = 'abc  def'
        self.assertEqual(clean_up_newlines(text), 'abc def')

    def test_leaves_duplicate_spaces_at_line_start_unchanged(self):
        text = '  abc'
        self.assertEqual(clean_up_newlines(text), '  abc')

    def test_removes_whitespace_between_newlines(self):
        text = 'abc\n\t\r \ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\ndef')

    def test_removes_whitespace_before_newline(self):
        text = 'abc\t \r\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc def')

    def test_replaces_single_newline_with_space(self):
        text = 'abc\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc def')

    def test_replaces_single_newline_in_two_places_with_spaces(self):
        text = 'abc\ndef\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc def ghi')

    def test_replaces_double_newline_with_single_newline(self):
        text = 'abc\n\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\ndef')

    def test_replaces_double_newline_with_single_newline_after_inline_bullet_character(self):
        text = ('a*bc\n\ndef')
        self.assertEqual(clean_up_newlines(text), 'a*bc\ndef')

    def test_replaces_double_newline_with_single_newline_after_inline_number(self):
        text = ('a1.bc\n\ndef')
        self.assertEqual(clean_up_newlines(text), 'a1.bc\ndef')

    def test_replaces_tripple_newline_with_double_newline(self):
        text = 'abc\n\n\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\ndef')

    def test_replaces_four_newlines_with_double_newline(self):
        text = 'abc\n\n\n\ndef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\ndef')

    def test_leaves_newline_unchanged_before_heading(self):
        text = 'abc\n# def'
        self.assertEqual(clean_up_newlines(text), 'abc\n# def')

    def test_leaves_newline_unchanged_after_heading(self):
        text = 'abc\n# def\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n# def\nghi')
        text = '# def\nghi'
        self.assertEqual(clean_up_newlines(text), '# def\nghi')

    def test_leaves_newline_unchanged_before_star_bullet(self):
        text = 'abc\n* def'
        self.assertEqual(clean_up_newlines(text), 'abc\n* def')

    def test_replaces_newline_with_space_after_star_bullet(self):
        text = 'abc\n* def\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n* def ghi')
        text = '* def\nghi'
        self.assertEqual(clean_up_newlines(text), '* def ghi')

    def test_leaves_newline_unchanged_before_plus_bullet(self):
        text = 'abc\n+ def'
        self.assertEqual(clean_up_newlines(text), 'abc\n+ def')

    def test_replaces_newline_with_space_after_plus_bullet(self):
        text = 'abc\n+ def\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n+ def ghi')
        text = '+ def\nghi'
        self.assertEqual(clean_up_newlines(text), '+ def ghi')

    def test_leaves_newline_unchanged_before_dash_bullet(self):
        text = 'abc\n- def'
        self.assertEqual(clean_up_newlines(text), 'abc\n- def')

    def test_replaces_newline_with_space_after_dash_bullet(self):
        text = 'abc\n- def\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n- def ghi')
        text = '- def\nghi'
        self.assertEqual(clean_up_newlines(text), '- def ghi')

    def test_leaves_double_newline_after_bullet_list_unchanged(self):
        self.maxDiff = None
        text = ('Before list.\n'
                '* First item\n'
                'continues here.\n'
                '* Second item\n'
                'continues here.\n'
                '\n'
                'After list.')
        expected = ('Before list.\n'
                    '* First item continues here.\n'
                    '* Second item continues here.\n'
                    '\n'
                    'After list.')
        self.assertEqual(clean_up_newlines(text), expected)

    def test_leaves_double_newline_after_numbered_list_unchanged(self):
        self.maxDiff = None
        text = ('Before list.\n'
                '1. First item\n'
                'continues here.\n'
                '1. Second item\n'
                'continues here.\n'
                '\n'
                'After list.')
        expected = ('Before list.\n'
                    '1. First item continues here.\n'
                    '1. Second item continues here.\n'
                    '\n'
                    'After list.')
        self.assertEqual(clean_up_newlines(text), expected)

    def test_leaves_newline_unchanged_before_line_starting_with_space(self):
        text = 'abc\n def'
        self.assertEqual(clean_up_newlines(text), 'abc\n def')

    def test_leaves_newline_unchanged_after_line_starting_with_space(self):
        text = 'abc\n def\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n def\nghi')
        text = ' def\nghi'
        self.assertEqual(clean_up_newlines(text), ' def\nghi')

    def test_leaves_newline_unchanged_before_line_starting_with_tab(self):
        text = 'abc\n\tdef'
        self.assertEqual(clean_up_newlines(text), 'abc\n\tdef')

    def test_leaves_newline_unchanged_after_line_starting_with_tab(self):
        text = 'abc\n\tdef\nghi'
        self.assertEqual(clean_up_newlines(text), 'abc\n\tdef\nghi')
        text = '\tdef\nghi'
        self.assertEqual(clean_up_newlines(text), '\tdef\nghi')

    def test_leaves_newline_unchanged_before_numbered_list_item_with_period(self):
        text = 'abc\n123. def'
        self.assertEqual(clean_up_newlines(text), 'abc\n123. def')

    def test_replaces_newline_with_space_after_numbered_list_item_with_period(self):
        text = 'abc\n123. def\nefg'
        self.assertEqual(clean_up_newlines(text), 'abc\n123. def efg')
        text = '123. def\nefg'
        self.assertEqual(clean_up_newlines(text), '123. def efg')

    def test_leaves_newline_unchanged_before_numbered_list_item_with_bracket(self):
        text = 'abc\n123) def'
        self.assertEqual(clean_up_newlines(text), 'abc\n123) def')

    def test_replaces_newline_with_space_after_numbered_list_item_with_bracket(self):
        text = 'abc\n123) def\nefg'
        self.assertEqual(clean_up_newlines(text), 'abc\n123) def efg')
        text = '123) def\nefg'
        self.assertEqual(clean_up_newlines(text), '123) def efg')

    def test_replaces_single_newlines_with_space_also_after_punctuation(self):
        text = 'abc,\r\ndef.\r\nghi)\r\njkl'
        self.assertEqual(clean_up_newlines(text), 'abc, def. ghi) jkl')

    def test_handles_newlines_after_punctuation(self):
        text = 'abc,\r\n\r\ndef.\r\n\r\nghi)\r\n\r\njkl'
        self.assertEqual(clean_up_newlines(text), 'abc,\ndef.\nghi)\njkl')

    # What to do with bullets, throw an error?
    def ignore_test_replaces_bullet_character_with_star(self):
        text = '• This is a bullet'
        self.assertEqual(clean_up_newlines(text), '* This is a bullet')

    def test_leaves_newline_after_heading_unchanged(self):
        text = 'previous paragraph.\n\n# Heading\nBody text.'
        self.assertEqual(clean_up_newlines(text), 'previous paragraph. \n# Heading\nBody text.')

    def test_leaves_newline_after_heading_at_the_start_of_string_unchanged(self):
        text = '# Heading\nBody text.'
        self.assertEqual(clean_up_newlines(text), '# Heading\nBody text.')

    def test_realistic_example(self):
        self.maxDiff = None
        text = ('## Try CommonMark\n\n\n'
                'You can try CommonMark here.\n'
                'This dingus is powered by\n\n'
                '[commonmark.js](https://github.com/jgm/commonmark.js), the\n\n'
                'JavaScript reference implementation.\n'
                '1. item one\n'
                '2. item two\n'
                '   - sublist\n'
                '   - sublist\n')
        expected = ('## Try CommonMark\n\n'
                    'You can try CommonMark here. This dingus is powered by\n'
                    '[commonmark.js](https://github.com/jgm/commonmark.js), the\n'
                    'JavaScript reference implementation.\n'
                    '1. item one\n'
                    '2. item two\n'
                    '   - sublist\n'
                    '   - sublist\n')
        self.assertEqual(clean_up_newlines(text), expected)


class CleanUpUrlLinksTest(TestCase):
    def test_replaces_http_link_with_markdown(self):
        text = 'abc http://example.com def'
        self.assertEqual(clean_up_http_links(text), 'abc [example.com](http://example.com) def')

    def test_replaces_two_links_with_markdown(self):
        text = 'abc http://example.com def http://example.org ghi'
        expected = 'abc [example.com](http://example.com) def [example.org](http://example.org) ghi'
        self.assertEqual(clean_up_http_links(text), expected)

    def test_includes_just_host_in_link_name(self):
        text = 'abc http://example.com/foo/bar def'
        self.assertEqual(clean_up_http_links(text), 'abc [example.com](http://example.com/foo/bar) def')

    def test_replaces_https_link_with_markdown(self):
        text = 'https://example.com'
        self.assertEqual(clean_up_http_links(text), '[example.com](https://example.com)')

    def test_handles_urls_with_dash_in_the_host_name(self):
        text = 'http://www.cra-arc.gc.ca/tx/ndvdls/vlntr/menu-eng.html'
        expected = '[www.cra-arc.gc.ca](http://www.cra-arc.gc.ca/tx/ndvdls/vlntr/menu-eng.html)'
        self.assertEqual(clean_up_http_links(text), expected)


class CleanUpMailtoLinksTest(TestCase):
    def test_replaces_email_link_with_markdown(self):
        text = 'abc foo@bar.com def'
        self.assertEqual(clean_up_email_links(text), 'abc [foo@bar.com](mailto:foo@bar.com) def')
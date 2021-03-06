import unittest

import bokeh
import bokeh.resources as resources

WRAPPER = """$(function() {
    foo
});"""

WRAPPER_DEV = '''require(["jquery", "main"], function($, Bokeh) {
    $(function() {
        foo
    });
});'''

class TestResources(unittest.TestCase):

    def test_basic(self):
        r = resources.Resources()
        self.assertEqual(r.mode, "inline")


    def test_module_attrs(self):
        self.assertEqual(resources.CDN.mode, "cdn")
        self.assertEqual(resources.INLINE.mode, "inline")

    def test_inline(self):
        r = resources.Resources(mode="inline")
        self.assertEqual(r.mode, "inline")
        self.assertEqual(r.dev, False)

        self.assertEqual(len(r.js_raw), 1)
        self.assertEqual(len(r.css_raw), 1)
        self.assertEqual(r.messages, [])

    def test_cdn(self):
        resources.__version__ = "1.0"
        r = resources.Resources(mode="cdn", version="1.0")
        self.assertEqual(r.mode, "cdn")
        self.assertEqual(r.dev, False)

        self.assertEqual(r.js_raw, [])
        self.assertEqual(r.css_raw, [])
        self.assertEqual(r.messages, [])

        resources.__version__ = "1.0-1-abc"
        r = resources.Resources(mode="cdn", version="1.0")
        self.assertEqual(r.messages, [
            {'text': "Requesting CDN BokehJS version '1.0' from Bokeh development version '1.0-1-abc'. This configuration is unsupported and may not work!",
            'type': 'warn'}
        ])

    def test_server(self):
        r = resources.Resources(mode="server")
        self.assertEqual(r.mode, "server")
        self.assertEqual(r.dev, False)

        self.assertEqual(r.js_raw, [])
        self.assertEqual(r.css_raw, [])
        self.assertEqual(r.messages, [])

    def test_server_dev(self):
        r = resources.Resources(mode="server-dev")
        self.assertEqual(r.mode, "server")
        self.assertEqual(r.dev, True)

        self.assertEqual(len(r.js_raw), 1)
        self.assertEqual(r.css_raw, [])
        self.assertEqual(r.messages, [])

    def test_relative(self):
        r = resources.Resources(mode="relative")
        self.assertEqual(r.mode, "relative")
        self.assertEqual(r.dev, False)

        self.assertEqual(r.js_raw, [])
        self.assertEqual(r.css_raw, [])
        self.assertEqual(r.messages, [])

    def test_relative_dev(self):
        r = resources.Resources(mode="relative-dev")
        self.assertEqual(r.mode, "relative")
        self.assertEqual(r.dev, True)

        self.assertEqual(len(r.js_raw), 1)
        self.assertEqual(r.css_raw, [])
        self.assertEqual(r.messages, [])

    def test_absolute(self):
        r = resources.Resources(mode="absolute")
        self.assertEqual(r.mode, "absolute")
        self.assertEqual(r.dev, False)

        self.assertEqual(r.js_raw, [])
        self.assertEqual(r.css_raw, [])
        self.assertEqual(r.messages, [])

    def test_absolute_dev(self):
        r = resources.Resources(mode="absolute-dev")
        self.assertEqual(r.mode, "absolute")
        self.assertEqual(r.dev, True)

        self.assertEqual(len(r.js_raw), 1)
        self.assertEqual(r.css_raw, [])
        self.assertEqual(r.messages, [])

    def test_argument_checks(self):
        self.assertRaises(ValueError, resources.Resources, "foo")

        for mode in ("inline", "cdn", "server", "server-dev", "absolute", "absolute-dev"):
            self.assertRaises(ValueError, resources.Resources, mode, root_dir="foo")

        for mode in ("inline", "server", "server-dev", "relative", "relative-dev", "absolute", "absolute-dev"):
            self.assertRaises(ValueError, resources.Resources, mode, version="foo")

        for mode in ("inline", "cdn", "relative", "relative-dev", "absolute", "absolute-dev"):
            self.assertRaises(ValueError, resources.Resources, mode, root_url="foo")

    def test_js_wrapper(self):
        for mode in ("inline", "server", "cdn", "relative", "absolute"):
            r = resources.Resources(mode)
            self.assertEqual(r.js_wrapper("foo"), WRAPPER)

        for mode in ("server-dev", "relative-dev", "absolute-dev"):
            r = resources.Resources(mode)
            self.assertEqual(r.js_wrapper("foo"), WRAPPER_DEV)

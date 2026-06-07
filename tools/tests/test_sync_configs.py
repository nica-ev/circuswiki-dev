from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from sync_configs import describe_changes, sync_config_text  # noqa: E402


class SyncConfigsTests(unittest.TestCase):
    def test_sync_config_text_updates_core_fields_and_alternates(self) -> None:
        before = '''[project]
site_url = "old"
docs_dir = "old-docs"
site_dir = "old-site"

[project.extra]
alternate = [
  { name = "German", link = "/old/", lang = "de" },
]

[project.theme]
language = "old"
'''
        after = sync_config_text(before, "en", "/circuswiki/", "https://example.test/circuswiki/")
        self.assertIn('site_url = "https://example.test/circuswiki/en/"', after)
        self.assertIn('docs_dir = ".build/en"', after)
        self.assertIn('site_dir = "site/en"', after)
        self.assertIn('language = "en"', after)
        self.assertIn('lang = "sk"', after)
        self.assertIn('link = "/circuswiki/en/"', after)

    def test_describe_changes_reports_field_changes(self) -> None:
        before = '''[project]
site_url = "old"
docs_dir = "old-docs"
site_dir = "old-site"

[project.extra]
alternate = []

[project.theme]
language = "old"
'''
        after = sync_config_text(before, "de", "/circuswiki/", "https://example.test/circuswiki/")
        changes = describe_changes(ROOT / "zensical.toml", "de", before, after)
        fields = {change.field for change in changes}
        self.assertIn("site_url", fields)
        self.assertIn("docs_dir", fields)
        self.assertIn("site_dir", fields)
        self.assertIn("theme.language", fields)
        self.assertIn("alternate", fields)


if __name__ == "__main__":
    unittest.main()

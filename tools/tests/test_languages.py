from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from core.languages import (  # noqa: E402
    default_language,
    language_codes,
    native_language_name,
    site_subpath,
    validate_registry,
    validate_zensical_alternates,
    zensical_configs,
)


class LanguageRegistryTests(unittest.TestCase):
    def test_registry_contains_expected_defaults(self) -> None:
        self.assertEqual(default_language(), "de")
        self.assertIn("en", language_codes())
        self.assertIn("sk", language_codes())
        self.assertEqual(native_language_name("pt"), "Português")

    def test_site_subpath_keeps_default_at_root(self) -> None:
        self.assertEqual(site_subpath("de", "/circuswiki/"), "/circuswiki/")
        self.assertEqual(site_subpath("en", "/circuswiki/"), "/circuswiki/en/")

    def test_all_registry_configs_exist(self) -> None:
        for language, path in zensical_configs().items():
            with self.subTest(language=language):
                self.assertTrue(path.exists(), path)

    def test_zensical_alternates_match_registry(self) -> None:
        self.assertEqual(validate_zensical_alternates(), [])

    def test_registry_validation_passes(self) -> None:
        result = validate_registry()
        self.assertTrue(result["ok"], result["issues"])


if __name__ == "__main__":
    unittest.main()

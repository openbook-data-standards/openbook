"""CI-only regression cases for informational onboarding integrity."""
import json
import subprocess
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import build_onboarding as onboarding
from jsonschema import ValidationError


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(onboarding.CATALOG.read_text())

    def load(self, data):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "docs").mkdir()
            (root / "docs/ecosystem.json").write_text(json.dumps(data))
            (root / "docs/ecosystem.schema.json").write_text(
                (onboarding.ROOT / "docs/ecosystem.schema.json").read_text()
            )
            with patch.object(onboarding, "ROOT", root), patch.object(onboarding, "CATALOG", root / "docs/ecosystem.json"):
                return onboarding.load_catalog()

    def test_current_catalog_and_skills(self):
        onboarding.load_catalog()
        onboarding.check_skills(self.data)

    def test_duplicate_project_rejected(self):
        self.data["projects"].append(deepcopy(self.data["projects"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.load(self.data)

    def test_missing_license_rejected(self):
        del self.data["projects"][0]["license"]
        with self.assertRaises(ValidationError):
            self.load(self.data)

    def test_unknown_skill_rejected(self):
        self.data["projects"][0]["skill"] = "not-a-skill"
        with self.assertRaisesRegex(ValueError, "Unknown skill"):
            self.load(self.data)

    def test_source_cannot_point_at_another_repository(self):
        self.data["projects"][0]["sources"] = ["https://github.com/openbook-data-standards/private-project/blob/main/README.md"]
        with self.assertRaisesRegex(ValueError, "catalogued public project"):
            self.load(self.data)

    def test_rendered_onboarding_links(self):
        onboarding.check_site()

    def test_unknown_relationship_rejected(self):
        self.data["projects"][0]["related_projects"] = ["not-a-project"]
        with self.assertRaisesRegex(ValueError, "Unknown/self-related"):
            self.load(self.data)

    def test_unknown_blocker_rejected(self):
        self.data["projects"][0]["blockers"] = ["ONB-999"]
        with self.assertRaisesRegex(ValueError, "Unknown blocker"):
            self.load(self.data)

    def test_orphan_blocker_rejected(self):
        for project in self.data["projects"]:
            project["blockers"] = []
        with self.assertRaisesRegex(ValueError, "attached to a project"):
            self.load(self.data)

    def test_future_date_rejected(self):
        self.data["reviewed_on"] = "9999-01-01"
        with self.assertRaisesRegex(ValueError, "future"):
            self.load(self.data)

    def test_invalid_date_rejected(self):
        self.data["reviewed_on"] = "2026-02-30"
        with self.assertRaises(ValidationError):
            self.load(self.data)

    def test_generated_copies_are_current(self):
        expected = onboarding.render(self.data)
        self.assertEqual((onboarding.ROOT / "docs/ecosystem.md").read_text(), expected)
        self.assertEqual((onboarding.SKILLS / "openbook/references/ecosystem.md").read_text(), expected)


class LinkTests(unittest.TestCase):
    def test_local_links_and_fragments(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "guide.md"
            page.write_text("# Guide\n\n[section](#guide)\n")
            with patch.object(onboarding, "ROOT", root):
                onboarding.check_links([page])
                page.write_text("[missing](missing.md)\n")
                with self.assertRaisesRegex(ValueError, "Missing/outside"):
                    onboarding.check_links([page])
                page.write_text("[escape](../outside.md)\n")
                with self.assertRaisesRegex(ValueError, "Missing/outside"):
                    onboarding.check_links([page])
                page.write_text("[missing](#absent)\n")
                with self.assertRaisesRegex(ValueError, "Missing heading"):
                    onboarding.check_links([page])

    def test_unsafe_scheme_rejected(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "guide.md"
            page.write_text("[bad](javascript:alert)\n")
            with patch.object(onboarding, "ROOT", root), self.assertRaisesRegex(ValueError, "scheme"):
                onboarding.check_links([page])


class UpstreamTests(unittest.TestCase):
    def setUp(self):
        self.data = onboarding.load_catalog()
        self.inventory = "\n".join(p["id"] for p in self.data["projects"])

    def response(self, stdout="", returncode=0):
        return subprocess.CompletedProcess([], returncode, stdout=stdout, stderr="")

    def test_new_public_project_rejected(self):
        with (
            patch.object(onboarding.subprocess, "run", return_value=self.response(self.inventory + "\nnew-project")),
            self.assertRaisesRegex(ValueError, "uncatalogued=.*new-project"),
        ):
            onboarding.check_upstream(self.data)

    def test_readme_at_repository_root_is_supported(self):
        responses = [self.response(self.inventory)]
        responses += [self.response() for p in self.data["projects"] for _ in p["sources"]]
        with patch.object(onboarding.subprocess, "run", side_effect=responses) as run:
            onboarding.check_upstream(self.data)
        self.assertTrue(any("contents/README.md?ref=main" in call.args[0][2] for call in run.call_args_list[1:]))

    def test_unavailable_source_rejected(self):
        with (
            patch.object(onboarding.subprocess, "run", side_effect=[self.response(self.inventory), self.response(returncode=1)]),
            self.assertRaisesRegex(ValueError, "Source unavailable"),
        ):
            onboarding.check_upstream(self.data)

    def test_authentication_failure_is_not_empty_inventory(self):
        with (
            patch.object(onboarding.subprocess, "run", side_effect=subprocess.CalledProcessError(1, ["gh", "api"])),
            self.assertRaises(subprocess.CalledProcessError),
        ):
            onboarding.check_upstream(self.data)

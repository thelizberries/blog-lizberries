import ast
import pathlib
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / ".github" / "scripts" / "translate_and_copy.py"


def load_functions_from_script(script_path: pathlib.Path):
    source = script_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(script_path))

    wanted_functions = {
        "normalize_single_quotes",
        "read_front_matter_value",
        "write_front_matter_value",
    }
    wanted_assignments = {"APOSTROPHE_VARIANTS"}

    selected_nodes = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            # Keep only imports required by tested helpers.
            names = {alias.name for alias in node.names}
            if "re" in names:
                selected_nodes.append(node)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in wanted_assignments:
                    selected_nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in wanted_functions:
            selected_nodes.append(node)

    module = ast.Module(body=selected_nodes, type_ignores=[])
    compiled = compile(module, filename=str(script_path), mode="exec")
    namespace = {}
    exec(compiled, namespace)
    return namespace


class TestTranslateApostrophes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ns = load_functions_from_script(SCRIPT_PATH)
        cls.normalize_single_quotes = staticmethod(ns["normalize_single_quotes"])
        cls.read_front_matter_value = staticmethod(ns["read_front_matter_value"])
        cls.write_front_matter_value = staticmethod(ns["write_front_matter_value"])

    def test_normalize_replaces_unicode_apostrophes(self):
        raw = "Dolores’ voice, The Cranberries‘ dream, Lingerʼs echo, It`s back"
        normalized = self.normalize_single_quotes(raw)

        self.assertEqual(
            normalized,
            "Dolores' voice, The Cranberries' dream, Linger's echo, It's back",
        )

    def test_normalize_collapses_double_apostrophes(self):
        raw = "Dolores'' O''Riordan''s style"
        normalized = self.normalize_single_quotes(raw)

        self.assertEqual(normalized, "Dolores' O'Riordan's style")

    def test_front_matter_title_description_are_md_safe(self):
        fm = (
            "layout: post\n"
            "title: \"Cranberries: Dolores’ '' dream\"\n"
            "description: \"It‘s the band‘s '' best era\"\n"
            "image: /assets/images/posts/sample.webp\n"
        )

        title = self.normalize_single_quotes(self.read_front_matter_value(fm, "title"))
        description = self.normalize_single_quotes(self.read_front_matter_value(fm, "description"))

        updated = self.write_front_matter_value(fm, "title", title)
        updated = self.write_front_matter_value(updated, "description", description)

        self.assertIn('title: "Cranberries: Dolores\' dream"', updated)
        self.assertIn('description: "It\'s the band\'s best era"', updated)
        self.assertNotIn("''", updated)


if __name__ == "__main__":
    unittest.main()

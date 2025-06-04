import unittest
import os
import sys
import importlib
from unittest.mock import patch, MagicMock

# Add project root to sys.path to allow importing core modules
# This might need adjustment based on actual test execution context
# For example, if tests are run from the project root, this might not be needed
# or might need to be `sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))`
# Assuming tests are in a 'tests' subdirectory sibling to 'core'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.processors.base import ProcessorBase
from core.processors import PROCESSOR_REGISTRY, register_processor, discover_processors, get_all_processors, get_processor

# --- Helper / Mock Processor Classes ---

class MockValidProcessor(ProcessorBase):
    _is_abstract = False # Mark as non-abstract for testing
    def __init__(self, graphics_path, output_dir): # Match expected constructor
        self.graphics_path = graphics_path
        self.output_dir = output_dir
    def is_applicable(self, order_data): return True
    def process(self, order_data, output_dir, graphics_path): pass

class MockValidProcessorAlternate(ProcessorBase):
    _is_abstract = False
    def __init__(self, graphics_path, output_dir):
        self.graphics_path = graphics_path
        self.output_dir = output_dir
    def is_applicable(self, order_data): return True
    def process(self, order_data, output_dir, graphics_path): pass

class NonProcessorBaseClass: # Does not inherit from ProcessorBase
    pass

# --- Test Cases ---

class TestProcessorRegistry(unittest.TestCase):

    def setUp(self):
        # Clear the registry before each test
        PROCESSOR_REGISTRY.clear()

    def test_register_valid_processor(self):
        register_processor("mock_valid", MockValidProcessor)
        self.assertIn("mock_valid", PROCESSOR_REGISTRY)
        self.assertEqual(PROCESSOR_REGISTRY["mock_valid"], MockValidProcessor)

    def test_register_invalid_processor_type(self):
        with self.assertRaisesRegex(ValueError, "must inherit from ProcessorBase"):
            register_processor("mock_invalid", NonProcessorBaseClass)
        self.assertNotIn("mock_invalid", PROCESSOR_REGISTRY)

    def test_reregister_processor_logs_warning(self):
        register_processor("mock_valid", MockValidProcessor)
        with patch('builtins.print') as mock_print: # Using builtins.print for Python 3
            register_processor("mock_valid", MockValidProcessorAlternate)
        mock_print.assert_called_with("Warning: Processor 'mock_valid' is being re-registered.")
        self.assertEqual(PROCESSOR_REGISTRY["mock_valid"], MockValidProcessorAlternate) # Should update

    def test_get_processor(self):
        register_processor("mock_get", MockValidProcessor)
        processor_class = get_processor("mock_get")
        self.assertEqual(processor_class, MockValidProcessor)
        self.assertIsNone(get_processor("non_existent_processor"))

    def test_get_all_processors(self):
        register_processor("mock1", MockValidProcessor)
        register_processor("mock2", MockValidProcessorAlternate)
        all_procs = get_all_processors()
        self.assertEqual(len(all_procs), 2)
        self.assertEqual(all_procs["mock1"], MockValidProcessor)
        self.assertEqual(all_procs["mock2"], MockValidProcessorAlternate)


class TestProcessorDiscovery(unittest.TestCase):

    def setUp(self):
        PROCESSOR_REGISTRY.clear()
        # Create dummy processor files for discovery tests
        self.test_processors_dir = os.path.join(os.path.dirname(__file__), '..', 'core', 'processors') # Assumes 'core/processors'
        os.makedirs(self.test_processors_dir, exist_ok=True)

        self.dummy_files_to_remove = []

    def _create_dummy_processor_file(self, filename, content):
        filepath = os.path.join(self.test_processors_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
        self.dummy_files_to_remove.append(filepath)
        return filepath # Return full path for importlib operations

    def tearDown(self):
        PROCESSOR_REGISTRY.clear()
        for filepath in self.dummy_files_to_remove:
            try:
                # Remove .pyc file if it exists
                # Construct module name as imported by discover_processors
                module_name_simple = os.path.basename(filepath)[:-3]
                full_module_name_for_sys = f"core.processors.{module_name_simple}"

                # Try to remove from sys.modules if loaded
                if full_module_name_for_sys in sys.modules:
                    del sys.modules[full_module_name_for_sys]

                # Construct .pyc path (specific to Python version and environment)
                # This is a common location, but might vary.
                # For simplicity, we'll try one common pattern for __pycache__.
                pycache_dir = os.path.join(os.path.dirname(filepath), "__pycache__")
                # Example: dummy_proc_self.cpython-38.pyc (adjust for actual Python version if needed)
                # A more robust way would be to use importlib.util.cache_from_source(filepath)
                try:
                    pyc_path = importlib.util.cache_from_source(filepath)
                    if os.path.exists(pyc_path):
                        os.remove(pyc_path)
                except Exception: # Broad exception if cache_from_source fails or path is odd
                    pass # pyc cleanup is best-effort

                if os.path.exists(filepath):
                    os.remove(filepath)

            except OSError as e:
                print(f"Warning: could not remove dummy file {filepath} or its .pyc: {e}")


    # Note: This test relies on the dummy files being importable.
    # The sys.path manipulation at the top of this test file is crucial.
    def test_discover_processors_imports_and_registers(self):
        dummy_content_self_register = """
from core.processors.base import ProcessorBase
from core.processors import register_processor
class DiscoveredProcessor1(ProcessorBase):
    _is_abstract = False
    def __init__(self, graphics_path, output_dir): pass
    def is_applicable(self, order_data): return True
    def process(self, order_data, output_dir, graphics_path): pass
register_processor("discovered1", DiscoveredProcessor1)
"""
        dummy_content_auto_register = """
from core.processors.base import ProcessorBase
class DiscoveredProcessor2(ProcessorBase):
    _is_abstract = False
    def __init__(self, graphics_path, output_dir): pass
    def is_applicable(self, order_data): return True
    def process(self, order_data, output_dir, graphics_path): pass
"""
        self._create_dummy_processor_file("dummy_proc_self.py", dummy_content_self_register)
        self._create_dummy_processor_file("dummy_proc_auto.py", dummy_content_auto_register)

        # Ensure registry is clean before discovery
        PROCESSOR_REGISTRY.clear()

        with patch('builtins.print') as mock_print:
            discover_processors()

        self.assertIn("discovered1", PROCESSOR_REGISTRY)
        self.assertEqual(PROCESSOR_REGISTRY["discovered1"].__name__, "DiscoveredProcessor1")

        self.assertIn("discoveredprocessor2", PROCESSOR_REGISTRY)
        self.assertEqual(PROCESSOR_REGISTRY["discoveredprocessor2"].__name__, "DiscoveredProcessor2")
        mock_print.assert_any_call("Auto-registering processor 'DiscoveredProcessor2' as 'discoveredprocessor2'. Consider explicit registration in the module.")


    @patch('importlib.import_module', side_effect=ImportError("Test Import Error"))
    @patch('builtins.print')
    def test_discover_processors_handles_import_error(self, mock_print, mock_import_module_raising_error):
        # This test specifically mocks import_module to *always* raise an error
        # To test this, we need a file that discover_processors will attempt to import.
        self._create_dummy_processor_file("dummy_proc_causes_error.py", "print('This should not execute if import fails early')")

        PROCESSOR_REGISTRY.clear()
        discover_processors() # This will call the mocked import_module

        # Check that an error message was printed for the dummy file
        # The exact module name depends on how listdir and module_name construction works
        # Assuming it tries to import core.processors.dummy_proc_causes_error
        mock_print.assert_any_call("Error importing processor module core.processors.dummy_proc_causes_error: Test Import Error")
        self.assertEqual(len(PROCESSOR_REGISTRY), 0)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

```

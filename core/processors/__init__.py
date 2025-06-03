import os
import importlib
import inspect
from .base import ProcessorBase

PROCESSOR_REGISTRY = {}

def register_processor(name, processor_class):
    """Registers a processor class with the given name."""
    if name in PROCESSOR_REGISTRY:
        # Allow re-registration for development/reloading, but log it.
        print(f"Warning: Processor '{name}' is being re-registered.")
    if not issubclass(processor_class, ProcessorBase):
        raise ValueError(
            f"Processor class '{processor_class.__name__}' must inherit from ProcessorBase."
        )
    PROCESSOR_REGISTRY[name] = processor_class

def discover_processors():
    """
    Discovers and imports all processor modules from the current directory.
    This function should be called once at application startup.
    """
    current_dir = os.path.dirname(__file__)
    for filename in os.listdir(current_dir):
        if filename.endswith(".py") and filename not in ("__init__.py", "base.py", "svg_utils.py", "text_utils.py"):
            module_name = filename[:-3]
            try:
                # Construct the full module path relative to the 'core' package
                full_module_name = f"core.processors.{module_name}"
                module = importlib.import_module(full_module_name)

                # After importing, check for classes that subclass ProcessorBase
                # and call register_processor if they haven't self-registered.
                # Typically, processors should self-register using `register_processor`
                # at the end of their respective files.
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and                        issubclass(obj, ProcessorBase) and                        obj is not ProcessorBase and                        name not in PROCESSOR_REGISTRY and                        not getattr(obj, '_is_abstract', False): # Check for an optional _is_abstract attribute
                        # Attempt to infer a name if not explicitly registered
                        # This is a fallback, explicit registration is preferred.
                        processor_instance_name = name.replace("Processor", "").lower()
                        if processor_instance_name not in PROCESSOR_REGISTRY:
                             print(f"Auto-registering processor '{name}' as '{processor_instance_name}'. "
                                   "Consider explicit registration in the module.")
                             register_processor(processor_instance_name, obj)

            except ImportError as e:
                print(f"Error importing processor module {full_module_name}: {e}")

def get_processor(name):
    """Returns the processor class with the given name."""
    return PROCESSOR_REGISTRY.get(name)

def get_all_processors():
    """Returns a dictionary of all registered processors."""
    return PROCESSOR_REGISTRY.copy()

# You might want to call discover_processors() here if you want it to run
# when the package is first imported, though often it's better to call it
# explicitly at a controlled point in your application's startup.
# For now, we'll require explicit calling.
# discover_processors()

import yaml
from typing import Any, Dict, List

def _sort_dict_recursively(d: Any) -> Any:
    """Recursively sorts nested dictionaries and lists containing dictionaries."""
    if isinstance(d, dict):
        # Sort dictionary items by key and recursively sort values
        return {k: _sort_dict_recursively(v) for k, v in sorted(d.items())}
    elif isinstance(d, list):
        # Recursively sort items within lists if they are dicts or lists
        return [_sort_dict_recursively(item) for item in d]
    else:
        # Return non-dict/list items as is
        return d

def normalize_yaml(data: Dict[str, Any]) -> str:
    """
    Normalizes a dictionary by recursively sorting keys and serializes it
    to a canonical YAML string representation suitable for hashing.

    Args:
        data: The dictionary to normalize.

    Returns:
        A canonical YAML string representation.
    """
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary")

    # Recursively sort the dictionary
    sorted_data = _sort_dict_recursively(data)

    # Dump to YAML string with consistent formatting
    return yaml.dump(
        sorted_data,
        sort_keys=True, # Ensures top-level keys are sorted (though _sort_dict_recursively handles nested)
        default_flow_style=False,
        indent=2,
        allow_unicode=True,
        # Dumper=yaml.SafeDumper # Use SafeDumper if needed, though default should be safe
    )

def normalize_yaml_old(data: dict) -> str:
    """Placeholder stub for YAML normalization function.
    
    Sorts keys recursively and returns a consistent YAML string representation.
    Implementation pending (Subtask 5.5).
    """
    # Actual implementation will go here
    # For now, return a simple sorted dump to satisfy import and basic tests
    try:
        return yaml.dump(data, sort_keys=True, allow_unicode=True, default_flow_style=None)
    except Exception:
        # Basic fallback if dump fails
        return "{}" 
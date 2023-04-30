import warnings

def emit_module_deprecation_warning(name):
    warnings.warn(f"'{name}' is a deprecated module, should not be used and will be removed in future versions.")

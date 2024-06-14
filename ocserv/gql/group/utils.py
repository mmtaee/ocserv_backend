from typing import AnyStr, Type


def group_config_repr(data: Type) -> tuple[list[AnyStr], dict]:
    configs = []
    metadata = {}
    for key, val in data.__dict__.items():
        if val is not None:
            if isinstance(val, bool):
                val = str(val).lower()
            configs.append(f"{key.replace('_', '-').lower()}={val}")
            metadata[key] = val
    return configs, metadata

#!/usr/bin/env python3
"""Validate public-safe tracked config templates and optional local overrides."""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised via CLI only
    print(
        "Error: PyYAML is required. Run `python -m pip install -r requirements-dev.txt`.",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


PLACEHOLDER_PREFIX = "YOUR_"

CONFIG_SPECS = {
    "notion": {
        "tracked": Path("config/notion.yaml"),
        "example": Path("config/notion.example.yaml"),
        "local": Path("config/notion.local.yaml"),
        "required_paths": [
            ("tasks_db_id",),
            ("weekly_pages",),
            ("weekly_pages", "root_page_id"),
            ("project_key_map",),
            ("automation",),
            ("property_names",),
            ("status_values",),
            ("priority_map",),
        ],
        "sensitive_paths": [
            ("tasks_db_id",),
            ("weekly_pages", "root_page_id"),
        ],
    },
    "confluence": {
        "tracked": Path("config/confluence.yaml"),
        "example": Path("config/confluence.example.yaml"),
        "local": Path("config/confluence.local.yaml"),
        "required_paths": [
            ("atlassian_domain",),
            ("default_space_key",),
            ("spaces",),
            ("parent_pages",),
            ("parent_pages", "pmo_docs"),
            ("meeting_minutes_map",),
            ("title_formats",),
        ],
        "sensitive_paths": [
            ("atlassian_domain",),
            ("default_space_key",),
            ("spaces", 0, "key"),
            ("parent_pages", "pmo_docs"),
            ("meeting_minutes_map", 0, "parent_id"),
            ("meeting_minutes_map", 0, "space_key"),
            ("meeting_minutes_map", 0, "copy_from"),
            ("meeting_minutes_map", 1, "parent_id"),
            ("meeting_minutes_map", 1, "space_key"),
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate config layering for tracked templates and optional local overrides."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root to validate.",
    )
    parser.add_argument(
        "--config",
        choices=["all", *CONFIG_SPECS.keys()],
        default="all",
        help="Specific config set to validate.",
    )
    parser.add_argument(
        "--tracked-only",
        action="store_true",
        help="Validate tracked templates and examples only.",
    )
    parser.add_argument(
        "--check-local",
        action="store_true",
        help="Require and validate local override files on top of tracked templates.",
    )
    return parser.parse_args()


def load_yaml_file(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        raise ValueError(f"{path} contains invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a YAML mapping")
    return data


def path_label(path_parts: tuple[object, ...]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts[-1] = f"{parts[-1]}[{part}]"
        else:
            parts.append(str(part))
    return ".".join(parts)


def get_path(data, path_parts: tuple[object, ...]):
    current = data
    for part in path_parts:
        if isinstance(part, int):
            if not isinstance(current, list) or len(current) <= part:
                raise KeyError(path_label(path_parts))
            current = current[part]
        else:
            if not isinstance(current, dict) or part not in current:
                raise KeyError(path_label(path_parts))
            current = current[part]
    return current


def has_path(data, path_parts: tuple[object, ...]) -> bool:
    try:
        get_path(data, path_parts)
    except KeyError:
        return False
    return True


def deep_merge(base, override):
    if isinstance(base, dict) and isinstance(override, dict):
        merged = copy.deepcopy(base)
        for key, value in override.items():
            merged[key] = deep_merge(merged[key], value) if key in merged else copy.deepcopy(value)
        return merged
    return copy.deepcopy(override)


def is_placeholder(value) -> bool:
    return isinstance(value, str) and value.startswith(PLACEHOLDER_PREFIX)


def validate_required_paths(config_name: str, data: dict, source: str, errors: list[str]) -> None:
    for path_parts in CONFIG_SPECS[config_name]["required_paths"]:
        if not has_path(data, path_parts):
            errors.append(f"{source}: missing required key `{path_label(path_parts)}`")


def validate_tracked_template(config_name: str, repo_root: Path, errors: list[str], notes: list[str]) -> dict:
    spec = CONFIG_SPECS[config_name]
    tracked_path = repo_root / spec["tracked"]
    example_path = repo_root / spec["example"]

    if not tracked_path.exists():
        errors.append(f"{tracked_path}: tracked template is missing")
        return {}
    if not example_path.exists():
        errors.append(f"{example_path}: example file is missing")
        return {}

    try:
        tracked = load_yaml_file(tracked_path)
        example = load_yaml_file(example_path)
    except ValueError as exc:
        errors.append(str(exc))
        return {}

    validate_required_paths(config_name, tracked, str(tracked_path), errors)
    validate_required_paths(config_name, example, str(example_path), errors)

    for path_parts in spec["sensitive_paths"]:
        label = path_label(path_parts)
        try:
            tracked_value = get_path(tracked, path_parts)
        except KeyError:
            continue
        if not is_placeholder(tracked_value):
            errors.append(
                f"{tracked_path}: `{label}` must stay as a YOUR_* placeholder. "
                f"Restore the tracked template and move concrete values to {spec['local']}."
            )

    notes.append(f"PASS tracked template: {tracked_path}")
    notes.append(f"PASS example file: {example_path}")
    return tracked


def validate_local_override(config_name: str, repo_root: Path, tracked: dict, errors: list[str], notes: list[str]) -> None:
    spec = CONFIG_SPECS[config_name]
    local_path = repo_root / spec["local"]
    example_path = repo_root / spec["example"]

    if not local_path.exists():
        errors.append(
            f"{local_path}: local override is missing. Copy {example_path} to {spec['local']} "
            "and replace the YOUR_* placeholders there."
        )
        return

    try:
        local = load_yaml_file(local_path)
    except ValueError as exc:
        errors.append(str(exc))
        return
    effective = deep_merge(tracked, local)
    validate_required_paths(config_name, effective, f"effective config for {config_name}", errors)

    for path_parts in spec["sensitive_paths"]:
        label = path_label(path_parts)
        try:
            effective_value = get_path(effective, path_parts)
        except KeyError:
            continue
        if not isinstance(effective_value, str) or effective_value.strip() == "":
            errors.append(
                f"{local_path}: `{label}` is missing in the effective config. "
                f"Set it in {spec['local']}."
            )
            continue
        if is_placeholder(effective_value):
            errors.append(
                f"{local_path}: `{label}` is still a placeholder in the effective config. "
                f"Replace YOUR_* in {spec['local']}."
            )

    notes.append(f"PASS local override: {local_path}")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    config_names = CONFIG_SPECS.keys() if args.config == "all" else [args.config]

    errors: list[str] = []
    notes: list[str] = []

    for config_name in config_names:
        tracked = validate_tracked_template(config_name, repo_root, errors, notes)
        if tracked and args.check_local and not args.tracked_only:
            validate_local_override(config_name, repo_root, tracked, errors, notes)

    for note in notes:
        print(note)

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    mode = "tracked templates only" if args.tracked_only or not args.check_local else "tracked templates + local overrides"
    print(f"Config validation passed for {mode}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

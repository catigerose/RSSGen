from __future__ import annotations

import runpy
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SOURCES_DIR = PROJECT_ROOT / "sources"

# 这些文件不是站点脚本，不应被批量执行。
EXCLUDED_SOURCE_FILES = {
    "__init__.py",
}


def discover_scripts():
    """自动发现 sources 目录下的站点脚本。

    这样移动脚本到 backup 或新增脚本时，无需再手动维护列表。
    """
    scripts = []
    for script_path in sorted(SOURCES_DIR.glob("*.py")):
        if script_path.name in EXCLUDED_SOURCE_FILES:
            continue
        scripts.append(script_path)
    return scripts


def resolve_scripts(arguments):
    """将命令行参数转换为待执行脚本列表。"""
    if not arguments:
        return discover_scripts()

    script_paths = []
    for argument in arguments:
        script_name = argument if argument.endswith(".py") else f"{argument}.py"
        candidate_paths = [
            PROJECT_ROOT / script_name,
            SOURCES_DIR / script_name,
        ]
        script_path = next((path for path in candidate_paths if path.exists()), None)
        if script_path is None:
            raise FileNotFoundError(f"未找到脚本: {script_name}")
        script_paths.append(script_path)
    return script_paths


def main():
    scripts = resolve_scripts(sys.argv[1:])
    for script_path in scripts:
        print(f"开始执行: {script_path.name}")
        # 使用 runpy 保持现有“每个站点一个独立脚本”的项目结构。
        runpy.run_path(str(script_path), run_name="__main__")
        print(f"执行完成: {script_path.name}")


if __name__ == "__main__":
    main()

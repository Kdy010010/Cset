import os
import sys
import argparse
import logging
import platform
import shutil

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(levelname)s: %(message)s")

def set_environment_variables():
    os.environ["MY_CUSTOM_ENV"] = "custom_value"

def copy_required_files(output_folder):
    # 예시: 복사할 파일 경로 설정
    source_file = "path/to/source/file"
    
    # 목적지 폴더 생성 (이미 존재하면 덮어쓰기)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 파일 복사
    shutil.copy(source_file, output_folder)

def check_system_requirements():
    # 예시: 특정 시스템 설정을 확인하는 로직 추가
    if platform.system() == "Windows":
        logging.info("Running on Windows system")
    else:
        logging.warning("Unsupported operating system")
        sys.exit(1)

def create_wrapper(script_path, output_folder, wrapper_name=None, script_args=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    script_name = os.path.basename(script_path)
    if wrapper_name is None:
        if os.name == "nt":
            wrapper_name = script_name[:-3] + ".bat"
        else:
            wrapper_name = script_name[:-3]

    wrapper_path = os.path.join(output_folder, wrapper_name)

    if os.name == "nt":
        wrapper_content = f"""@echo off
set MY_CUSTOM_ENV=custom_value
python "{script_path}" {' '.join(script_args) if script_args else ''}
"""
    else:
        wrapper_content = f"""#!/bin/bash
export MY_CUSTOM_ENV=custom_value
python3 "{script_path}" {' '.join(script_args) if script_args else ''}
"""

    with open(wrapper_path, "w") as wrapper_file:
        wrapper_file.write(wrapper_content)

    if os.name != "nt":
        os.chmod(wrapper_path, 0o755)

    print(f"Wrapper created: {wrapper_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a wrapper for a Python script.")
    parser.add_argument("script_path", help="Path to the Python script")
    parser.add_argument("output_folder", help="Output folder for the wrapper file")
    parser.add_argument("--wrapper_name", help="Name for the wrapper file (default: script name)")
    parser.add_argument("--args", nargs="+", help="Arguments to pass to the script")

    args = parser.parse_args()

    setup_logging(os.path.join(args.output_folder, "wrapper.log"))
    logging.info("Starting wrapper script")

    copy_required_files(args.output_folder)

    set_environment_variables()

    check_system_requirements()

    create_wrapper(args.script_path, args.output_folder, args.wrapper_name, args.args)

    logging.info("Wrapper script completed")

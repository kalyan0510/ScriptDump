import pkg_resources
from tabulate import tabulate
from packaging import version

def check_installed_versions(requirements_file):
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    installed_packages = {pkg.key.lower().replace('_','-'): pkg.version for pkg in pkg_resources.working_set}

    categorized_packages = {
        "INSTALLED IS LATEST THAN REQUIRED": [],
        "REQUIRED IS SAME AS INSTALLED": [],
        "NOT INSTALLED": [],
        "INSTALLED IS OLDER THAN REQUIRED": []
    }

    for req in requirements:
        package, required_version = (req.split('==') + [None])[:2]
        package = package.split('[')[0]
        package=package.lower().replace('_', '-')
        installed_version = installed_packages.get(package, None)

        if installed_version is None:
            categorized_packages["NOT INSTALLED"].append([package, "Not installed", required_version if required_version else "Any"])
        elif required_version is None:
            categorized_packages["REQUIRED IS SAME AS INSTALLED"].append([package, installed_version, "Any"])
        else:
            if version.parse(installed_version) > version.parse(required_version):
                categorized_packages["INSTALLED IS LATEST THAN REQUIRED"].append([package, installed_version, required_version])
            elif version.parse(installed_version) == version.parse(required_version):
                categorized_packages["REQUIRED IS SAME AS INSTALLED"].append([package, installed_version, required_version])
            else:
                categorized_packages["INSTALLED IS OLDER THAN REQUIRED"].append([package, installed_version, required_version])

    for category, table in categorized_packages.items():
        print(f"\n{category}:")
        print(tabulate(table, headers=["Package", "Installed Version", "Required Version"], tablefmt="grid"))

if __name__ == "__main__":
    check_installed_versions("requirements.txt")

{ pkgs }: {
    deps = [
        pkgs.python310
        pkgs.python310Packages.pip
        pkgs.python310Packages.setuptools
        pkgs.python310Packages.wheel
        pkgs.gcc
        pkgs.swig
    ];
}

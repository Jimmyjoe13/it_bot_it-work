{
  description = "Python environment for IT-Bot";
  deps = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.gcc
    pkgs.swig
    pkgs.pkg-config
    pkgs.openssl
    pkgs.git
  ];
}

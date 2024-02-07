{ pkgs, lib, python3Packages, }:
python3Packages.buildPythonPackage rec {
  name = "generate-qr-page";
  src = ./generate-qr-page;
  format = "pyproject";
  propagatedBuildInputs = [
    python3Packages.setuptools
    python3Packages.qrcode
  ] ++ lib.optionals (!pkgs.stdenv.isDarwin) [
    # no hope to run this, detect it from /Applications?
    pkgs.chromium
  ];

  makeWrapperArgs = let
    fontconfig_file = pkgs.makeFontsConf {
      fontDirectories = [
        pkgs.freefont_ttf
        pkgs.dejavu_fonts
      ];
    };
  in ["--set FONTCONFIG_FILE ${fontconfig_file}"];
}

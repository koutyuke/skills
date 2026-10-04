{
  description = "Development tools for personal skills";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    { nixpkgs, treefmt-nix, ... }:
    let
      system = "aarch64-darwin";
      pkgs = nixpkgs.legacyPackages.${system};
      treefmt = treefmt-nix.lib.evalModule pkgs {
        projectRootFile = "flake.nix";
        programs = {
          nixfmt.enable = true;
          oxfmt.enable = true;
          ruff-format.enable = true;
          typstyle.enable = true;
        };
      };
    in
    {
      formatter.${system} = treefmt.config.build.wrapper;

      devShells.${system}.default = pkgs.mkShell {
        packages = [
          treefmt.config.build.wrapper
          pkgs.textlint
          pkgs.oxfmt
          pkgs.nixfmt
          pkgs.ruff
          pkgs.typstyle
        ];
        shellHook = ''
          export NODE_PATH="${pkgs.textlint-rule-preset-ja-spacing}/lib/node_modules"
        '';
      };
    };
}

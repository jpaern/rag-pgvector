{
  description = "Template for nix flakes.";
  nixConfig.bash-prompt = "[nix (my-project)] ";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            eza
            git
            diff-so-fancy
            lazygit
            python310
            postgresql_16
          ];

          shellHook = ''
            alias ls=eza
            alias ll="ls -l"
            set -o vi
          '';
        };
      });
}

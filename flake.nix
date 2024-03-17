{
  description = "Template for nix flakes.";
  # nixConfig.bash-prompt = "[nix (my-project)] ";
  nixConfig.bash-prompt-prefix = "(venv)";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        #docker = {
        #  buildInputs = with pkgs; [
        #    postgresql_16
        #  ];
        #};
        #python = {
        #  buildInputs = with pkgs; [
        #    eza
        #    git
        #    diff-so-fancy
        #    lazygit
        #    openssl
        #    python311
        #    postgresql_16
        #  ];
        #};
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            eza
            git
            diff-so-fancy
            lazygit
            openssl
            python311
            postgresql_16
          ];

          shellHook = ''
            alias ls=eza
            alias ll="ls -l"
            set -o vi
            export PS1="$VIRTUAL_ENV_PROMPT$PS1"
          '';
        };
      });
}

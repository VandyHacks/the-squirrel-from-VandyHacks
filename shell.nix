{ nixpkgs ? fetchTarball "https://github.com/NixOS/nixpkgs/archive/refs/tags/21.05.tar.gz"
, pkgs ? (import nixpkgs {}) }:
with pkgs;

let
  pythonEnv = (python3.withPackages (p: [
    p.discordpy
    p.databases
    p.python-dotenv
    p.psutil
    p.requests
    p.python-dateutil
    p.asyncpg
    p.psycopg2
  ]));
in

mkShell {
  buildInputs = [ pythonEnv postgresql_13 ];
}

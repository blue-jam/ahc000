# ahc000
Template repository for AtCoder Heuristic Contest based on AHC039.

## Cheat Sheet

### Init

Non-interactive init with Rust language and objective function `max`:
```sh
pahcer init -p ahc000 -o max -l rust
```

Interactive init with C++ and objective function `min`:
```sh
pahcer init -p ahc030 -o min -l cpp -i
```

Download tools
```sh
./download-tools.sh "URL_TO_ZIP_FILE"
```

Run `pahcer-studio`
```sh
cd pahcer-studio
yarn install && yarn start
```

### Run

All cases

```sh
pahcer run
```

Single case, copy output to clipboard

```sh
./run.sh 0 -c
```

Single case, show output on the console

```sh
./run.sh 0 -o
```

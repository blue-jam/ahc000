# INSTRUCTIONS

## Project Overview

This is an AtCoder Heuristic Contest (AHC) repository based on AHC039. It's a Rust-based optimization problem solver for competitive programming contests focused on heuristic algorithms.

## Instruction for solution development

- Problem statement is in `PROBLEM.md`. You can also refer `PROBLEM.html` when you need to understand the input/output format and equation correctly.
- **ALWAYS** write/update your solution approach in `SOLUTION.md`, when you try a new idea.
- **DO NOT REVERT** your ongoing implementation when you get stuck. Instead, stop implementation and write your thoughts in `SOLUTION.md`. I'll help you to fix it.
- Implement your heuristic algorithm in `src/main.rs`.
- Every time you make changes, **ALWAYS RUN TEST** by `./run.sh 0 -o`.
- Receive input from `stdin` and output results to `stdout`. Use `proconio` for Input.
    - Put inputs to `Input` struct.
    - Put outputs to `Output` struct.
- Put your logic in `solve()` function.
    - Add a new function when you try a new solution.
- **DO NOT MODIFY** files in `tools/`, `pahcer/` and `pahcer-studio/` directories.
- **DO NOT USE** `timeout` command on execution of the program.

## Key Architecture

- **Main solver**: `src/main.rs` - Contains the core optimization algorithm.
- **Tools integration**: Uses `pahcer` runner for automated testing and `pahcer-studio` for visualization

## Development Commands

### Building and Running
```bash
# Build release binary
cargo build --release

# Run single test case
./run.sh <test_number>           # Save output to tools/out/
./run.sh <test_number> -c        # Copy output to clipboard
./run.sh <test_number> -o        # Print output to console
```

### Configuration
- **pahcer_config.toml**: Defines test execution, scoring, and compilation steps
- **Test range**: Seeds 0-99 by default in pahcer config

## Project Structure

```
src/main.rs             # Main solver with random search algorithm
tools/                  # Contest tools (generator, visualizer) **DO NOT MODIFY**
  ├── in/               # Input test files
  ├── out/              # Output files
  └── src/              # Tool binaries (gen, vis)
pahcer/                 # Test execution results **DO NOT MODIFY**
pahcer-studio/          # Web-based visualization (TypeScript/Vite) **DO NOT MODIFY**
run.sh                  # Single test execution script
PROBLEM.md              # Problem statement in Markdown **DO NOT MODIFY**
PROBLEM.html            # Problem statement in HTML **DO NOT MODIFY**
SOLUTION.md             # Explanation of solution approach.
```

## Testing Workflow

1. Use `./run.sh N` for quick single case testing during development
    - where `N` is the test case number (0-)

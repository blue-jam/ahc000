# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AtCoder Heuristic Contest (AHC) template repository based on AHC039. It's a Rust-based optimization problem solver for competitive programming contests focused on heuristic algorithms.

## Instruction for solution development

- Problem statement is in `PROBLEM.md`.
- Write/update your solution approach in `SOLUTION.md`.
- Implement your heuristic algorithm in `src/main.rs`.
- Every time you make changes, **ALWAYS RUN TEST** by `./run.sh 0 -o`.
- Receive input from `stdin` and output results to `stdout`. Use proconio for Input.
    - Put inputs to `Input` struct.
    - Put outputs to `Output` struct.
- Put your logic in `solve()` function.
    - Add a new function when you try a new solution.
- **DO NOT MODIFY** files in `tools/`, `pahcer/` and `pahcer-studio` directories.

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

# Run all test cases with pahcer
pahcer run
```

### Configuration
- **pahcer_config.toml**: Defines test execution, scoring, and compilation steps
- **TIME_LIMIT_MS**: Currently set to 1700ms in main.rs for contest timing
- **Test range**: Seeds 0-100 by default in pahcer config

## Project Structure

```
src/main.rs              # Main solver with random search algorithm
tools/                   # Contest tools (generator, visualizer) **DO NOT MODIFY**
  ├── in/               # Input test files
  ├── out/              # Output files
  └── src/              # Tool binaries (gen, vis)
pahcer/                  # Test execution results **DO NOT MODIFY**
pahcer-studio/           # Web-based visualization (TypeScript/Vite) **DO NOT MODIFY**
run.sh                   # Single test execution script
PROBLEM.md              # Problem statement
SOLUTION.md             # Explanation of solution approach.
```

## Testing Workflow

1. Use `./run.sh N` for quick single case testing during development
2. Use `pahcer run` for comprehensive evaluation across all test cases
3. Check `pahcer/summary.md` for aggregate results and scoring

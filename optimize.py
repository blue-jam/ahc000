import json
import math
import os
import subprocess
import threading
import time
from typing import Any

import optuna


def generate_params(trial: optuna.trial.Trial) -> dict[str, str]:
    # for more information, see https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html
    params = {
        "SEARCH_DEPTH": str(trial.suggest_int("SEARCH_DEPTH", 3, 10)),
    }

    return params


def extract_score(result: dict[str, Any]) -> float:
    absolute_score = result["score"]  # noqa: F841
    log10_score = math.log10(absolute_score) if absolute_score > 0.0 else 0.0  # noqa: F841
    relative_score = result["relative_score"]  # noqa: F841

    # score = absolute_score    # for absolute score problems
    # score = log10_score       # for relative score problems (alternative)
    score = relative_score      # for relative score problems

    return score


def get_direction() -> str:
    # direction = "minimize"
    direction = "maximize"
    return direction


def run_optimization(study: optuna.study.Study) -> None:
    # study.optimize(Objective(), timeout=300)
    study.optimize(Objective(), n_trials=100)


class Objective:
    def __init__(self) -> None:
        pass

    def __call__(self, trial: optuna.trial.Trial) -> float:
        params = generate_params(trial)
        env = os.environ.copy()
        env.update(params)

        # get # of test cases from tools/in/*.txt
        num_cases = len(glob.glob("tools/in/*.txt"))

        first_successful_scores = {}
        error_occurred = False
        last_error_msg = ""
        
        for attempt in range(5):
            cmd = [
                "pahcer",
                "run",
                "--json",
                "--shuffle",
                "--no-result-file",
                "--freeze-best-scores",
            ]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                env=env,
            )

            # Timeout after 30 minutes
            timer = threading.Timer(1800.0, lambda p: p.kill() if p.poll() is None else None, [process])
            timer.start()

            try:
                for line in process.stdout:
                    try:
                        result = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # If an error occurs, we skip this seed on this attempt
                    if result.get("error_message", "") != "":
                        print(f"Warning: stderr for seed {result.get('seed', 'unknown')} on attempt {attempt+1}: {result['error_message']}")
                        continue
                    
                    seed = result["seed"]
                    if seed not in first_successful_scores:
                        score = extract_score(result)
                        first_successful_scores[seed] = score
                        
                        try:
                            trial.report(score, seed)
                        except ValueError:
                            pass

                        if trial.should_prune():
                            print(f"Trial {trial.number} pruned.")
                            process.send_signal(subprocess.signal.SIGINT)

                            scores_list = list(first_successful_scores.values())
                            objective_value = sum(scores_list) / len(scores_list) if scores_list else 0
                            is_better_than_best = False
                            try:
                                is_better_than_best = (
                                    trial.study.direction == optuna.study.StudyDirection.MINIMIZE
                                    and objective_value < trial.study.best_value
                                ) or (
                                    trial.study.direction == optuna.study.StudyDirection.MAXIMIZE
                                    and objective_value > trial.study.best_value
                                )
                            except ValueError:
                                pass # No best value yet

                            if is_better_than_best:
                                raise optuna.TrialPruned()
                            else:
                                return objective_value

                process.wait()
                if process.returncode != 0 and process.returncode != -subprocess.signal.SIGINT:
                    error_occurred = True
                    if not last_error_msg:
                        last_error_msg = f"Process exited with code {process.returncode} (Timeout or internal error)"

            except optuna.TrialPruned:
                raise
            except Exception as e:
                error_occurred = True
                last_error_msg = str(e)
            finally:
                timer.cancel()
                if process.poll() is None:
                    process.kill()
                    process.wait()
                    
            if len(first_successful_scores) >= num_cases:
                break

        if len(first_successful_scores) == 0:
            if error_occurred:
                raise RuntimeError(f"Failed to run pahcer. Last error: {last_error_msg}")
            else:
                return 0.0

        scores = list(first_successful_scores.values())
        missing_count = num_cases - len(scores)
        if missing_count > 0:
            scores.extend([0.0] * missing_count)
            
        return sum(scores) / len(scores)


study = optuna.create_study(
    direction=get_direction(),
    study_name="optuna-study",
    pruner=optuna.pruners.WilcoxonPruner(),
    sampler=optuna.samplers.TPESampler(),
)

run_optimization(study)

print(f"best params = {study.best_params}")
print(f"best score  = {study.best_value}")
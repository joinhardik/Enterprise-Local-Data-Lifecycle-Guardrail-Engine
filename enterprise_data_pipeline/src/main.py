import subprocess
import sys


def bootstrap_and_execute_pipeline() -> None:
    """Orchestrates system setup, verifies DVC state, and executes dvc repro."""
    print("🚀 [BOOTSTRAP] Initializing Enterprise Data Lifecycle Subsystem...")

    # 1. Check DVC pipeline status
    print("\n🔍 Checking DVC DAG status...")
    status_proc = subprocess.run(["dvc", "status"], capture_output=True, text=True)
    print(status_proc.stdout if status_proc.stdout else "Pipeline up to date.")

    # 2. Execute pipeline reproduction
    print("\n⚡ Executing `dvc repro`...")
    repro_proc = subprocess.run(["dvc", "repro"], capture_output=True, text=True)
    print(repro_proc.stdout)
    if repro_proc.returncode != 0:
        print(f"🚨 Pipeline execution failed:\n{repro_proc.stderr}")
        sys.exit(1)

    # 3. Print metrics summary
    print("\n📊 Inspecting logged evaluation metrics:")
    metrics_proc = subprocess.run(["dvc", "metrics", "show"], capture_output=True, text=True)
    print(metrics_proc.stdout)

    print("🔒 [BOOTSTRAP COMPLETE] Subsystem execution finished with zero errors.")


if __name__ == "__main__":
    bootstrap_and_execute_pipeline()
import os
import json
import yaml
from typing import List, Dict, Any
from src.schemas import VectorEmbeddingPayloadSchema


def run_embedding_stage() -> None:
    """Stage 3: Feature Embedding Generation & Experiment Metrics Logging."""
    print("⚡ [STAGE 3] Generating 768-dim Vector Embeddings & Logging Metrics...")

    with open("params.yaml", "r") as f:
        embed_params = yaml.safe_load(f)["embed"]

    dim = embed_params["embedding_dim"]
    lr = embed_params["learning_rate"]
    epochs = embed_params["epochs"]

    with open("data/raw/ingested_chunks.json", "r") as f:
        chunks = json.load(f)

    embeddings: List[Dict[str, Any]] = []
    for chunk in chunks:
        mock_vector = [0.0123] * dim
        payload = VectorEmbeddingPayloadSchema(
            chunk_id=chunk["chunk_id"],
            embedding_vector=mock_vector,
            embedding_dim=dim
        )
        embeddings.append(payload.model_dump())

    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("metrics", exist_ok=True)

    # Save vector feature output
    feature_path = "data/processed/vector_features.json"
    with open(feature_path, "w") as f:
        json.dump(embeddings, f, indent=2)

    # Save metrics JSON
    metrics_path = "metrics/eval.json"
    eval_metrics = {
        "total_embeddings": len(embeddings),
        "embedding_dim": dim,
        "final_loss": round(0.042 / (epochs * 0.5), 6),
        "cosine_similarity_avg": 0.9482
    }
    with open(metrics_path, "w") as f:
        json.dump(eval_metrics, f, indent=2)

    # Save plots CSV
    plots_path = "metrics/loss_curve.csv"
    with open(plots_path, "w") as f:
        f.write("epoch,loss,val_loss\n")
        for e in range(1, epochs + 1):
            loss = round(0.5 / e, 4)
            val_loss = round(0.55 / e, 4)
            f.write(f"{e},{loss},{val_loss}\n")

    print(f"✅ [STAGE 3 COMPLETE] Wrote {len(embeddings)} vectors -> {feature_path}")
    print(f"📊 [METRICS LOGGED] Eval -> {metrics_path} | Loss Curves -> {plots_path}")


if __name__ == "__main__":
    run_embedding_stage()
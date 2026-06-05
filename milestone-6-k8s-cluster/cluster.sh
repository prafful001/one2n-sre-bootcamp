 #!/usr/bin/env bash
set -euo pipefail

PROFILE="prod-cluster"

start_cluster() {
    echo "[INFO] Starting 3-node Minikube cluster..."
    minikube start \
        --nodes 3 \
        --driver docker \
        --cpus 2 \
        --memory 2048 \
        --profile "$PROFILE"
    echo "[INFO] Cluster started successfully."
}

label_nodes() {
    echo "[INFO] Applying node labels..."
    kubectl label node "${PROFILE}"      type=application        --overwrite
    kubectl label node "${PROFILE}-m02"  type=database           --overwrite
    kubectl label node "${PROFILE}-m03"  type=dependent_services --overwrite
    echo "[INFO] Labels applied."
}

verify() {
    echo "[INFO] Final cluster state:"
    kubectl get nodes -L type
}

main() {
    start_cluster
    label_nodes
    verify
}

main "$@"
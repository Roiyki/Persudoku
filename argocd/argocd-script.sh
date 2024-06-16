#!/bin/bash

# Create the namespace
 kubectl create namespace argocd-namespace

# Add ArgoCD Helm repository
 helm repo add argo https://argoproj.github.io/argo-helm

# Install ArgoCD if it's not installed, or upgrade it if it's already installed
 helm upgrade --install argocd argo/argo-cd --namespace argocd-namespace \
   --set server.admin.enabled=true \
   --set server.admin.password=roiyiy123 \
   --set server.service.type=NodePort \
   --set server.service.nodePorts.http=30080 \
   --set persistence.enabled=true \
   --set persistence.size=8Gi \
   --set persistence.storageClass=standard

# kubectl -n argocd-namespace get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
# Wait for Argo CD to be ready (adjust timeout as needed)
 kubectl wait --for=condition=available deployment/argocd-server --timeout=300s -n argocd-namespace

# Apply the updated argocd-cm ConfigMap (if needed, but since it's already configured, you may skip this step)
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd-namespace
data:
  accounts.admin: apiKey
  admin.enabled: "true"
  application.instanceLabelKey: argocd.argoproj.io/instance
  exec.enabled: "false"
  server.rbac.log.enforce.enable: "false"
  statusbadge.enabled: "false"
  timeout.hard.reconciliation: 0s
  timeout.reconciliation: 180s
  url: https://argocd.example.com
EOF
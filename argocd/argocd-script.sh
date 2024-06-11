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
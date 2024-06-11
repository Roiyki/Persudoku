#!/bin/bash

# Store the Argo CD initial admin password in a variable
PASSWORD=$(kubectl -n argocd-namespace get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

# Log in to Argo CD
./argocd login 192.168.68.60:30080 --username admin --password $PASSWORD --insecure

# Update the password to a new one
./argocd account update-password --current-password $PASSWORD --new-password roiyiy123 --insecure

# Log in with the new password
./argocd login 192.168.68.60:30080 --username admin --password roiyiy123 --insecure

# Create or update the Persudoku application
./argocd app create persudoku \
  --project default \
  --repo https://github.com/Roiyki/Persudoku.git \
  --path charts/appchart \
  --revision HEAD \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default \
  --helm-set-file values=values.yaml \
  --sync-policy automated \
  --self-heal \
  --upsert

# Create or update the Jenkins application
./argocd app create jenkins \
  --project default \
  --repo https://github.com/Roiyki/Persudoku.git \
  --path charts/jenkinschart \
  --revision HEAD \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace jenkins \
  --helm-set-file values=values.yaml \
  --sync-policy automated \
  --self-heal \
  --upsert

<<<<<<< HEAD:charts/kube-prometheus-stack/charts/grafana/README.md
# Grafana Helm Chart

* Installs the web dashboarding system [Grafana](http://grafana.org/)

## Get Repo Info

```console
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

_See [helm repo](https://helm.sh/docs/helm/helm_repo/) for command documentation._

## Installing the Chart

To install the chart with the release name `my-release`:

```console
helm install my-release grafana/grafana
```

## Uninstalling the Chart

To uninstall/delete the my-release deployment:

```console
helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Upgrading an existing Release to a new major version

A major chart version change (like v1.2.3 -> v2.0.0) indicates that there is an
incompatible breaking change needing manual actions.

### To 4.0.0 (And 3.12.1)

This version requires Helm >= 2.12.0.

### To 5.0.0

You have to add --force to your helm upgrade command as the labels of the chart have changed.

### To 6.0.0

This version requires Helm >= 3.1.0.

### To 7.0.0

For consistency with other Helm charts, the `global.image.registry` parameter was renamed
to `global.imageRegistry`. If you were not previously setting `global.image.registry`, no action
is required on upgrade. If you were previously setting `global.image.registry`, you will
need to instead set `global.imageRegistry`.

## Configuration

| Parameter                                 | Description                                   | Default                                                 |
|-------------------------------------------|-----------------------------------------------|---------------------------------------------------------|
| `replicas`                                | Number of nodes                               | `1`                                                     |
| `podDisruptionBudget.minAvailable`        | Pod disruption minimum available              | `nil`                                                   |
| `podDisruptionBudget.maxUnavailable`      | Pod disruption maximum unavailable            | `nil`                                                   |
| `podDisruptionBudget.apiVersion`          | Pod disruption apiVersion                     | `nil`                                                   |
| `deploymentStrategy`                      | Deployment strategy                           | `{ "type": "RollingUpdate" }`                           |
| `livenessProbe`                           | Liveness Probe settings                       | `{ "httpGet": { "path": "/api/health", "port": 3000 } "initialDelaySeconds": 60, "timeoutSeconds": 30, "failureThreshold": 10 }` |
| `readinessProbe`                          | Readiness Probe settings                      | `{ "httpGet": { "path": "/api/health", "port": 3000 } }`|
| `securityContext`                         | Deployment securityContext                    | `{"runAsUser": 472, "runAsGroup": 472, "fsGroup": 472}`  |
| `priorityClassName`                       | Name of Priority Class to assign pods         | `nil`                                                   |
| `image.registry`                          | Image registry                                | `docker.io`                                       |
| `image.repository`                        | Image repository                              | `grafana/grafana`                                       |
| `image.tag`                               | Overrides the Grafana image tag whose default is the chart appVersion (`Must be >= 5.0.0`) | ``                                                      |
| `image.sha`                               | Image sha (optional)                          | ``                                                      |
| `image.pullPolicy`                        | Image pull policy                             | `IfNotPresent`                                          |
| `image.pullSecrets`                       | Image pull secrets (can be templated)         | `[]`                                                    |
| `service.enabled`                         | Enable grafana service                        | `true`                                                  |
| `service.type`                            | Kubernetes service type                       | `ClusterIP`                                             |
| `service.port`                            | Kubernetes port where service is exposed      | `80`                                                    |
| `service.portName`                        | Name of the port on the service               | `service`                                               |
| `service.appProtocol`                     | Adds the appProtocol field to the service     | ``                                                      |
| `service.targetPort`                      | Internal service is port                      | `3000`                                                  |
| `service.nodePort`                        | Kubernetes service nodePort                   | `nil`                                                   |
| `service.annotations`                     | Service annotations (can be templated)        | `{}`                                                    |
| `service.labels`                          | Custom labels                                 | `{}`                                                    |
| `service.clusterIP`                       | internal cluster service IP                   | `nil`                                                   |
| `service.loadBalancerIP`                  | IP address to assign to load balancer (if supported) | `nil`                                            |
| `service.loadBalancerSourceRanges`        | list of IP CIDRs allowed access to lb (if supported) | `[]`                                             |
| `service.externalIPs`                     | service external IP addresses                 | `[]`                                                    |
| `service.externalTrafficPolicy`           | change the default externalTrafficPolicy | `nil`                                            |
| `headlessService`                         | Create a headless service                     | `false`                                                 |
| `extraExposePorts`                        | Additional service ports for sidecar containers| `[]`                                                   |
| `hostAliases`                             | adds rules to the pod's /etc/hosts            | `[]`                                                    |
| `ingress.enabled`                         | Enables Ingress                               | `false`                                                 |
| `ingress.annotations`                     | Ingress annotations (values are templated)    | `{}`                                                    |
| `ingress.labels`                          | Custom labels                                 | `{}`                                                    |
| `ingress.path`                            | Ingress accepted path                         | `/`                                                     |
| `ingress.pathType`                        | Ingress type of path                          | `Prefix`                                                |
| `ingress.hosts`                           | Ingress accepted hostnames                    | `["chart-example.local"]`                                                    |
| `ingress.extraPaths`                      | Ingress extra paths to prepend to every host configuration. Useful when configuring [custom actions with AWS ALB Ingress Controller](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.6/guide/ingress/annotations/#actions). Requires `ingress.hosts` to have one or more host entries. | `[]`                                                    |
| `ingress.tls`                             | Ingress TLS configuration                     | `[]`                                                    |
| `ingress.ingressClassName`                | Ingress Class Name. MAY be required for Kubernetes versions >= 1.18 | `""`                              |
| `resources`                               | CPU/Memory resource requests/limits           | `{}`                                                    |
| `nodeSelector`                            | Node labels for pod assignment                | `{}`                                                    |
| `tolerations`                             | Toleration labels for pod assignment          | `[]`                                                    |
| `affinity`                                | Affinity settings for pod assignment          | `{}`                                                    |
| `extraInitContainers`                     | Init containers to add to the grafana pod     | `{}`                                                    |
| `extraContainers`                         | Sidecar containers to add to the grafana pod  | `""`                                                    |
| `extraContainerVolumes`                   | Volumes that can be mounted in sidecar containers | `[]`                                                |
| `extraLabels`                             | Custom labels for all manifests               | `{}`                                                    |
| `schedulerName`                           | Name of the k8s scheduler (other than default) | `nil`                                                  |
| `persistence.enabled`                     | Use persistent volume to store data           | `false`                                                 |
| `persistence.type`                        | Type of persistence (`pvc` or `statefulset`)  | `pvc`                                                   |
| `persistence.size`                        | Size of persistent volume claim               | `10Gi`                                                  |
| `persistence.existingClaim`               | Use an existing PVC to persist data (can be templated) | `nil`                                          |
| `persistence.storageClassName`            | Type of persistent volume claim               | `nil`                                                   |
| `persistence.accessModes`                 | Persistence access modes                      | `[ReadWriteOnce]`                                       |
| `persistence.annotations`                 | PersistentVolumeClaim annotations             | `{}`                                                    |
| `persistence.finalizers`                  | PersistentVolumeClaim finalizers              | `[ "kubernetes.io/pvc-protection" ]`                    |
| `persistence.extraPvcLabels`              | Extra labels to apply to a PVC.               | `{}`                                                    |
| `persistence.subPath`                     | Mount a sub dir of the persistent volume (can be templated) | `nil`                                     |
| `persistence.inMemory.enabled`            | If persistence is not enabled, whether to mount the local storage in-memory to improve performance | `false`                                                   |
| `persistence.inMemory.sizeLimit`          | SizeLimit for the in-memory local storage     | `nil`                                                   |
| `initChownData.enabled`                   | If false, don't reset data ownership at startup | true                                                  |
| `initChownData.image.registry`            | init-chown-data container image registry      | `docker.io`                                               |
| `initChownData.image.repository`          | init-chown-data container image repository    | `busybox`                                               |
| `initChownData.image.tag`                 | init-chown-data container image tag           | `1.31.1`                                                |
| `initChownData.image.sha`                 | init-chown-data container image sha (optional)| `""`                                                    |
| `initChownData.image.pullPolicy`          | init-chown-data container image pull policy   | `IfNotPresent`                                          |
| `initChownData.resources`                 | init-chown-data pod resource requests & limits | `{}`                                                   |
| `schedulerName`                           | Alternate scheduler name                      | `nil`                                                   |
| `env`                                     | Extra environment variables passed to pods    | `{}`                                                    |
| `envValueFrom`                            | Environment variables from alternate sources. See the API docs on [EnvVarSource](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.17/#envvarsource-v1-core) for format details. Can be templated | `{}` |
| `envFromSecret`                           | Name of a Kubernetes secret (must be manually created in the same namespace) containing values to be added to the environment. Can be templated | `""` |
| `envFromSecrets`                          | List of Kubernetes secrets (must be manually created in the same namespace) containing values to be added to the environment. Can be templated | `[]` |
| `envFromConfigMaps`                       | List of Kubernetes ConfigMaps (must be manually created in the same namespace) containing values to be added to the environment. Can be templated | `[]` |
| `envRenderSecret`                         | Sensible environment variables passed to pods and stored as secret. (passed through [tpl](https://helm.sh/docs/howto/charts_tips_and_tricks/#using-the-tpl-function))   | `{}`                               |
| `enableServiceLinks`                      | Inject Kubernetes services as environment variables. | `true`                                           |
| `extraSecretMounts`                       | Additional grafana server secret mounts       | `[]`                                                    |
| `extraVolumeMounts`                       | Additional grafana server volume mounts       | `[]`                                                    |
| `extraVolumes`                            | Additional Grafana server volumes             | `[]`                                                    |
| `automountServiceAccountToken`            | Mounted the service account token on the grafana pod. Mandatory, if sidecars are enabled  | `true`      |
| `createConfigmap`                         | Enable creating the grafana configmap         | `true`                                                  |
| `extraConfigmapMounts`                    | Additional grafana server configMap volume mounts (values are templated) | `[]`                         |
| `extraEmptyDirMounts`                     | Additional grafana server emptyDir volume mounts | `[]`                                                 |
| `plugins`                                 | Plugins to be loaded along with Grafana       | `[]`                                                    |
| `datasources`                             | Configure grafana datasources (passed through tpl) | `{}`                                               |
| `alerting`                                | Configure grafana alerting (passed through tpl) | `{}`                                                  |
| `notifiers`                               | Configure grafana notifiers                   | `{}`                                                    |
| `dashboardProviders`                      | Configure grafana dashboard providers         | `{}`                                                    |
| `dashboards`                              | Dashboards to import                          | `{}`                                                    |
| `dashboardsConfigMaps`                    | ConfigMaps reference that contains dashboards | `{}`                                                    |
| `grafana.ini`                             | Grafana's primary configuration               | `{}`                                                    |
| `global.imageRegistry`                    | Global image pull registry for all images.    | `null`                                   |
| `global.imagePullSecrets`                 | Global image pull secrets (can be templated). Allows either an array of {name: pullSecret} maps (k8s-style), or an array of strings (more common helm-style).  | `[]`                                                    |
| `ldap.enabled`                            | Enable LDAP authentication                    | `false`                                                 |
| `ldap.existingSecret`                     | The name of an existing secret containing the `ldap.toml` file, this must have the key `ldap-toml`. | `""` |
| `ldap.config`                             | Grafana's LDAP configuration                  | `""`                                                    |
| `annotations`                             | Deployment annotations                        | `{}`                                                    |
| `labels`                                  | Deployment labels                             | `{}`                                                    |
| `podAnnotations`                          | Pod annotations                               | `{}`                                                    |
| `podLabels`                               | Pod labels                                    | `{}`                                                    |
| `podPortName`                             | Name of the grafana port on the pod           | `grafana`                                               |
| `lifecycleHooks`                          | Lifecycle hooks for podStart and preStop [Example](https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/#define-poststart-and-prestop-handlers)     | `{}`                                                    |
| `sidecar.image.registry`                  | Sidecar image registry                        | `quay.io`                          |
| `sidecar.image.repository`                | Sidecar image repository                      | `kiwigrid/k8s-sidecar`                          |
| `sidecar.image.tag`                       | Sidecar image tag                             | `1.26.0`                                                |
| `sidecar.image.sha`                       | Sidecar image sha (optional)                  | `""`                                                    |
| `sidecar.imagePullPolicy`                 | Sidecar image pull policy                     | `IfNotPresent`                                          |
| `sidecar.resources`                       | Sidecar resources                             | `{}`                                                    |
| `sidecar.securityContext`                 | Sidecar securityContext                       | `{}`                                                    |
| `sidecar.enableUniqueFilenames`           | Sets the kiwigrid/k8s-sidecar UNIQUE_FILENAMES environment variable. If set to `true` the sidecar will create unique filenames where duplicate data keys exist between ConfigMaps and/or Secrets within the same or multiple Namespaces. | `false`                           |
| `sidecar.alerts.enabled`             | Enables the cluster wide search for alerts and adds/updates/deletes them in grafana |`false`       |
| `sidecar.alerts.label`               | Label that config maps with alerts should have to be added | `grafana_alert`                               |
| `sidecar.alerts.labelValue`          | Label value that config maps with alerts should have to be added | `""`                                |
| `sidecar.alerts.searchNamespace`     | Namespaces list. If specified, the sidecar will search for alerts config-maps  inside these namespaces. Otherwise the namespace in which the sidecar is running will be used. It's also possible to specify ALL to search in all namespaces. | `nil`                               |
| `sidecar.alerts.watchMethod`         | Method to use to detect ConfigMap changes. With WATCH the sidecar will do a WATCH requests, with SLEEP it will list all ConfigMaps, then sleep for 60 seconds. | `WATCH` |
| `sidecar.alerts.resource`            | Should the sidecar looks into secrets, configmaps or both. | `both`                               |
| `sidecar.alerts.reloadURL`           | Full url of datasource configuration reload API endpoint, to invoke after a config-map change | `"http://localhost:3000/api/admin/provisioning/alerting/reload"` |
| `sidecar.alerts.skipReload`          | Enabling this omits defining the REQ_URL and REQ_METHOD environment variables | `false` |
| `sidecar.alerts.initAlerts`          | Set to true to deploy the alerts sidecar as an initContainer. This is needed if skipReload is true, to load any alerts defined at startup time. | `false` |
| `sidecar.alerts.extraMounts`         | Additional alerts sidecar volume mounts. | `[]`                               |
| `sidecar.dashboards.enabled`              | Enables the cluster wide search for dashboards and adds/updates/deletes them in grafana | `false`       |
| `sidecar.dashboards.SCProvider`           | Enables creation of sidecar provider          | `true`                                                  |
| `sidecar.dashboards.provider.name`        | Unique name of the grafana provider           | `sidecarProvider`                                       |
| `sidecar.dashboards.provider.orgid`       | Id of the organisation, to which the dashboards should be added | `1`                                   |
| `sidecar.dashboards.provider.folder`      | Logical folder in which grafana groups dashboards | `""`                                                |
| `sidecar.dashboards.provider.folderUid`   | Allows you to specify the static UID for the logical folder above | `""`                                |
| `sidecar.dashboards.provider.disableDelete` | Activate to avoid the deletion of imported dashboards | `false`                                       |
| `sidecar.dashboards.provider.allowUiUpdates` | Allow updating provisioned dashboards from the UI | `false`                                          |
| `sidecar.dashboards.provider.type`        | Provider type                                 | `file`                                                  |
| `sidecar.dashboards.provider.foldersFromFilesStructure`        | Allow Grafana to replicate dashboard structure from filesystem.                                 | `false`                                                  |
| `sidecar.dashboards.watchMethod`          | Method to use to detect ConfigMap changes. With WATCH the sidecar will do a WATCH requests, with SLEEP it will list all ConfigMaps, then sleep for 60 seconds. | `WATCH` |
| `sidecar.skipTlsVerify`                   | Set to true to skip tls verification for kube api calls | `nil`                                         |
| `sidecar.dashboards.label`                | Label that config maps with dashboards should have to be added | `grafana_dashboard`                                |
| `sidecar.dashboards.labelValue`                | Label value that config maps with dashboards should have to be added | `""`                                |
| `sidecar.dashboards.folder`               | Folder in the pod that should hold the collected dashboards (unless `sidecar.dashboards.defaultFolderName` is set). This path will be mounted. | `/tmp/dashboards`    |
| `sidecar.dashboards.folderAnnotation`     | The annotation the sidecar will look for in configmaps to override the destination folder for files | `nil`                                                  |
| `sidecar.dashboards.defaultFolderName`    | The default folder name, it will create a subfolder under the `sidecar.dashboards.folder` and put dashboards in there instead | `nil`                                |
| `sidecar.dashboards.searchNamespace`      | Namespaces list. If specified, the sidecar will search for dashboards config-maps  inside these namespaces. Otherwise the namespace in which the sidecar is running will be used. It's also possible to specify ALL to search in all namespaces. | `nil`                                |
| `sidecar.dashboards.script`               | Absolute path to shell script to execute after a configmap got reloaded. | `nil`                                |
| `sidecar.dashboards.reloadURL`            | Full url of dashboards configuration reload API endpoint, to invoke after a config-map change | `"http://localhost:3000/api/admin/provisioning/dashboards/reload"` |
| `sidecar.dashboards.skipReload`           | Enabling this omits defining the REQ_USERNAME, REQ_PASSWORD, REQ_URL and REQ_METHOD environment variables | `false` |
| `sidecar.dashboards.resource`             | Should the sidecar looks into secrets, configmaps or both. | `both`                               |
| `sidecar.dashboards.extraMounts`          | Additional dashboard sidecar volume mounts. | `[]`                               |
| `sidecar.datasources.enabled`             | Enables the cluster wide search for datasources and adds/updates/deletes them in grafana |`false`       |
| `sidecar.datasources.label`               | Label that config maps with datasources should have to be added | `grafana_datasource`                               |
| `sidecar.datasources.labelValue`          | Label value that config maps with datasources should have to be added | `""`                                |
| `sidecar.datasources.searchNamespace`     | Namespaces list. If specified, the sidecar will search for datasources config-maps  inside these namespaces. Otherwise the namespace in which the sidecar is running will be used. It's also possible to specify ALL to search in all namespaces. | `nil`                               |
| `sidecar.datasources.watchMethod`         | Method to use to detect ConfigMap changes. With WATCH the sidecar will do a WATCH requests, with SLEEP it will list all ConfigMaps, then sleep for 60 seconds. | `WATCH` |
| `sidecar.datasources.resource`            | Should the sidecar looks into secrets, configmaps or both. | `both`                               |
| `sidecar.datasources.reloadURL`           | Full url of datasource configuration reload API endpoint, to invoke after a config-map change | `"http://localhost:3000/api/admin/provisioning/datasources/reload"` |
| `sidecar.datasources.skipReload`          | Enabling this omits defining the REQ_URL and REQ_METHOD environment variables | `false` |
| `sidecar.datasources.initDatasources`     | Set to true to deploy the datasource sidecar as an initContainer in addition to a container. This is needed if skipReload is true, to load any datasources defined at startup time. | `false` |
| `sidecar.notifiers.enabled`               | Enables the cluster wide search for notifiers and adds/updates/deletes them in grafana | `false`        |
| `sidecar.notifiers.label`                 | Label that config maps with notifiers should have to be added | `grafana_notifier`                               |
| `sidecar.notifiers.labelValue`            | Label value that config maps with notifiers should have to be added | `""`                                |
| `sidecar.notifiers.searchNamespace`       | Namespaces list. If specified, the sidecar will search for notifiers config-maps (or secrets) inside these namespaces. Otherwise the namespace in which the sidecar is running will be used. It's also possible to specify ALL to search in all namespaces. | `nil`                               |
| `sidecar.notifiers.watchMethod`           | Method to use to detect ConfigMap changes. With WATCH the sidecar will do a WATCH requests, with SLEEP it will list all ConfigMaps, then sleep for 60 seconds. | `WATCH` |
| `sidecar.notifiers.resource`              | Should the sidecar looks into secrets, configmaps or both. | `both`                               |
| `sidecar.notifiers.reloadURL`             | Full url of notifier configuration reload API endpoint, to invoke after a config-map change | `"http://localhost:3000/api/admin/provisioning/notifications/reload"` |
| `sidecar.notifiers.skipReload`            | Enabling this omits defining the REQ_URL and REQ_METHOD environment variables | `false` |
| `sidecar.notifiers.initNotifiers`         | Set to true to deploy the notifier sidecar as an initContainer in addition to a container. This is needed if skipReload is true, to load any notifiers defined at startup time. | `false` |
| `smtp.existingSecret`                     | The name of an existing secret containing the SMTP credentials. | `""`                                  |
| `smtp.userKey`                            | The key in the existing SMTP secret containing the username. | `"user"`                                 |
| `smtp.passwordKey`                        | The key in the existing SMTP secret containing the password. | `"password"`                             |
| `admin.existingSecret`                    | The name of an existing secret containing the admin credentials (can be templated). | `""`                                 |
| `admin.userKey`                           | The key in the existing admin secret containing the username. | `"admin-user"`                          |
| `admin.passwordKey`                       | The key in the existing admin secret containing the password. | `"admin-password"`                      |
| `serviceAccount.automountServiceAccountToken` | Automount the service account token on all pods where is service account is used | `false` |
| `serviceAccount.annotations`              | ServiceAccount annotations                    |                                                         |
| `serviceAccount.create`                   | Create service account                        | `true`                                                  |
| `serviceAccount.labels`                   | ServiceAccount labels                         | `{}`                                                    |
| `serviceAccount.name`                     | Service account name to use, when empty will be set to created account if `serviceAccount.create` is set else to `default` | `` |
| `serviceAccount.nameTest`                 | Service account name to use for test, when empty will be set to created account if `serviceAccount.create` is set else to `default` | `nil` |
| `rbac.create`                             | Create and use RBAC resources                 | `true`                                                  |
| `rbac.namespaced`                         | Creates Role and Rolebinding instead of the default ClusterRole and ClusteRoleBindings for the grafana instance  | `false` |
| `rbac.useExistingRole`                    | Set to a rolename to use existing role - skipping role creating - but still doing serviceaccount and rolebinding to the rolename set here. | `nil` |
| `rbac.pspEnabled`                         | Create PodSecurityPolicy (with `rbac.create`, grant roles permissions as well) | `false`                |
| `rbac.pspUseAppArmor`                     | Enforce AppArmor in created PodSecurityPolicy (requires `rbac.pspEnabled`)  | `false`                   |
| `rbac.extraRoleRules`                     | Additional rules to add to the Role           | []                                                      |
| `rbac.extraClusterRoleRules`              | Additional rules to add to the ClusterRole    | []                                                      |
| `command`                                 | Define command to be executed by grafana container at startup | `nil`                                   |
| `args`                                    | Define additional args if command is used     | `nil`                                                   |
| `testFramework.enabled`                   | Whether to create test-related resources      | `true`                                                  |
| `testFramework.image.registry`            | `test-framework` image registry.            | `docker.io`                                             |
| `testFramework.image.repository`          | `test-framework` image repository.            | `bats/bats`                                             |
| `testFramework.image.tag`                 | `test-framework` image tag.                   | `v1.4.1`                                                |
| `testFramework.imagePullPolicy`           | `test-framework` image pull policy.           | `IfNotPresent`                                          |
| `testFramework.securityContext`           | `test-framework` securityContext              | `{}`                                                    |
| `downloadDashboards.env`                  | Environment variables to be passed to the `download-dashboards` container | `{}`                        |
| `downloadDashboards.envFromSecret`        | Name of a Kubernetes secret (must be manually created in the same namespace) containing values to be added to the environment. Can be templated | `""` |
| `downloadDashboards.resources`            | Resources of `download-dashboards` container  | `{}`                                                    |
| `downloadDashboardsImage.registry`        | Curl docker image registry                    | `docker.io`                                       |
| `downloadDashboardsImage.repository`      | Curl docker image repository                  | `curlimages/curl`                                       |
| `downloadDashboardsImage.tag`             | Curl docker image tag                         | `7.73.0`                                                |
| `downloadDashboardsImage.sha`             | Curl docker image sha (optional)              | `""`                                                    |
| `downloadDashboardsImage.pullPolicy`      | Curl docker image pull policy                 | `IfNotPresent`                                          |
| `namespaceOverride`                       | Override the deployment namespace             | `""` (`Release.Namespace`)                              |
| `serviceMonitor.enabled`                  | Use servicemonitor from prometheus operator   | `false`                                                 |
| `serviceMonitor.namespace`                | Namespace this servicemonitor is installed in |                                                         |
| `serviceMonitor.interval`                 | How frequently Prometheus should scrape       | `1m`                                                    |
| `serviceMonitor.path`                     | Path to scrape                                | `/metrics`                                              |
| `serviceMonitor.scheme`                   | Scheme to use for metrics scraping            | `http`                                                  |
| `serviceMonitor.tlsConfig`                | TLS configuration block for the endpoint      | `{}`                                                    |
| `serviceMonitor.labels`                   | Labels for the servicemonitor passed to Prometheus Operator      |  `{}`                                |
| `serviceMonitor.scrapeTimeout`            | Timeout after which the scrape is ended       | `30s`                                                   |
| `serviceMonitor.relabelings`              | RelabelConfigs to apply to samples before scraping.     | `[]`                                      |
| `serviceMonitor.metricRelabelings`        | MetricRelabelConfigs to apply to samples before ingestion.  | `[]`                                      |
| `revisionHistoryLimit`                    | Number of old ReplicaSets to retain           | `10`                                                    |
| `imageRenderer.enabled`                    | Enable the image-renderer deployment & service                                     | `false`                          |
| `imageRenderer.image.registry`             | image-renderer Image registry                                                      | `docker.io` |
| `imageRenderer.image.repository`           | image-renderer Image repository                                                    | `grafana/grafana-image-renderer` |
| `imageRenderer.image.tag`                  | image-renderer Image tag                                                           | `latest`                         |
| `imageRenderer.image.sha`                  | image-renderer Image sha (optional)                                                | `""`                             |
| `imageRenderer.image.pullPolicy`           | image-renderer ImagePullPolicy                                                     | `Always`                         |
| `imageRenderer.env`                        | extra env-vars for image-renderer                                                  | `{}`                             |
| `imageRenderer.envValueFrom`               | Environment variables for image-renderer from alternate sources. See the API docs on [EnvVarSource](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.17/#envvarsource-v1-core) for format details. Can be templated | `{}` |
| `imageRenderer.serviceAccountName`         | image-renderer deployment serviceAccountName                                       | `""`                             |
| `imageRenderer.securityContext`            | image-renderer deployment securityContext                                          | `{}`                             |
| `imageRenderer.podAnnotations `            | image-renderer image-renderer pod annotation                                       | `{}`                             |
| `imageRenderer.hostAliases`                | image-renderer deployment Host Aliases                                             | `[]`                             |
| `imageRenderer.priorityClassName`          | image-renderer deployment priority class                                           | `''`                             |
| `imageRenderer.service.enabled`            | Enable the image-renderer service                                                  | `true`                           |
| `imageRenderer.service.portName`           | image-renderer service port name                                                   | `http`                           |
| `imageRenderer.service.port`               | image-renderer port used by deployment                                             | `8081`                           |
| `imageRenderer.service.targetPort`         | image-renderer service port used by service                                        | `8081`                           |
| `imageRenderer.appProtocol`                | Adds the appProtocol field to the service                                          | ``                               |
| `imageRenderer.grafanaSubPath`             | Grafana sub path to use for image renderer callback url                            | `''`                             |
| `imageRenderer.podPortName`                | name of the image-renderer port on the pod                                         | `http`                           |
| `imageRenderer.revisionHistoryLimit`       | number of image-renderer replica sets to keep                                      | `10`                             |
| `imageRenderer.networkPolicy.limitIngress` | Enable a NetworkPolicy to limit inbound traffic from only the created grafana pods | `true`                           |
| `imageRenderer.networkPolicy.limitEgress`  | Enable a NetworkPolicy to limit outbound traffic to only the created grafana pods  | `false`                          |
| `imageRenderer.resources`                  | Set resource limits for image-renderer pods                                        | `{}`                             |
| `imageRenderer.nodeSelector`               | Node labels for pod assignment                | `{}`                                                    |
| `imageRenderer.tolerations`                | Toleration labels for pod assignment          | `[]`                                                    |
| `imageRenderer.affinity`                   | Affinity settings for pod assignment          | `{}`                                                    |
| `networkPolicy.enabled`                    | Enable creation of NetworkPolicy resources.                                                                              | `false`             |
| `networkPolicy.allowExternal`              | Don't require client label for connections                                                                               | `true`              |
| `networkPolicy.explicitNamespacesSelector` | A Kubernetes LabelSelector to explicitly select namespaces from which traffic could be allowed                           | `{}`                |
| `networkPolicy.ingress`                    | Enable the creation of an ingress network policy             | `true`    |
| `networkPolicy.egress.enabled`             | Enable the creation of an egress network policy              | `false`   |
| `networkPolicy.egress.ports`               | An array of ports to allow for the egress                    | `[]`    |
| `enableKubeBackwardCompatibility`          | Enable backward compatibility of kubernetes where pod's defintion version below 1.13 doesn't have the enableServiceLinks option  | `false`     |

### Example ingress with path

With grafana 6.3 and above

```yaml
grafana.ini:
  server:
    domain: monitoring.example.com
    root_url: "%(protocol)s://%(domain)s/grafana"
    serve_from_sub_path: true
ingress:
  enabled: true
  hosts:
    - "monitoring.example.com"
  path: "/grafana"
```

### Example of extraVolumeMounts and extraVolumes

Configure additional volumes with `extraVolumes` and volume mounts with `extraVolumeMounts`.

Example for `extraVolumeMounts` and corresponding `extraVolumes`:

```yaml
extraVolumeMounts:
  - name: plugins
    mountPath: /var/lib/grafana/plugins
    subPath: configs/grafana/plugins
    readOnly: false
  - name: dashboards
    mountPath: /var/lib/grafana/dashboards
    hostPath: /usr/shared/grafana/dashboards
    readOnly: false

extraVolumes:
  - name: plugins
    existingClaim: existing-grafana-claim
  - name: dashboards
    hostPath: /usr/shared/grafana/dashboards
```

Volumes default to `emptyDir`. Set to `persistentVolumeClaim`,
`hostPath`, `csi`, or `configMap` for other types. For a
`persistentVolumeClaim`, specify an existing claim name with
`existingClaim`.

## Import dashboards

There are a few methods to import dashboards to Grafana. Below are some examples and explanations as to how to use each method:

```yaml
dashboards:
  default:
    some-dashboard:
      json: |
        {
          "annotations":

          ...
          # Complete json file here
          ...

          "title": "Some Dashboard",
          "uid": "abcd1234",
          "version": 1
        }
    custom-dashboard:
      # This is a path to a file inside the dashboards directory inside the chart directory
      file: dashboards/custom-dashboard.json
    prometheus-stats:
      # Ref: https://grafana.com/dashboards/2
      gnetId: 2
      revision: 2
      datasource: Prometheus
    loki-dashboard-quick-search:
      gnetId: 12019
      revision: 2
      datasource:
      - name: DS_PROMETHEUS
        value: Prometheus
      - name: DS_LOKI
        value: Loki
    local-dashboard:
      url: https://raw.githubusercontent.com/user/repository/master/dashboards/dashboard.json
```

## BASE64 dashboards

Dashboards could be stored on a server that does not return JSON directly and instead of it returns a Base64 encoded file (e.g. Gerrit)
A new parameter has been added to the url use case so if you specify a b64content value equals to true after the url entry a Base64 decoding is applied before save the file to disk.
If this entry is not set or is equals to false not decoding is applied to the file before saving it to disk.

### Gerrit use case

Gerrit API for download files has the following schema: <https://yourgerritserver/a/{project-name}/branches/{branch-id}/files/{file-id}/content> where {project-name} and
{file-id} usually has '/' in their values and so they MUST be replaced by %2F so if project-name is user/repo, branch-id is master and file-id is equals to dir1/dir2/dashboard
the url value is <https://yourgerritserver/a/user%2Frepo/branches/master/files/dir1%2Fdir2%2Fdashboard/content>

## Sidecar for dashboards

If the parameter `sidecar.dashboards.enabled` is set, a sidecar container is deployed in the grafana
pod. This container watches all configmaps (or secrets) in the cluster and filters out the ones with
a label as defined in `sidecar.dashboards.label`. The files defined in those configmaps are written
to a folder and accessed by grafana. Changes to the configmaps are monitored and the imported
dashboards are deleted/updated.

A recommendation is to use one configmap per dashboard, as a reduction of multiple dashboards inside
one configmap is currently not properly mirrored in grafana.

Example dashboard config:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sample-grafana-dashboard
  labels:
     grafana_dashboard: "1"
data:
  k8s-dashboard.json: |-
  [...]
```

## Sidecar for datasources

If the parameter `sidecar.datasources.enabled` is set, an init container is deployed in the grafana
pod. This container lists all secrets (or configmaps, though not recommended) in the cluster and
filters out the ones with a label as defined in `sidecar.datasources.label`. The files defined in
those secrets are written to a folder and accessed by grafana on startup. Using these yaml files,
the data sources in grafana can be imported.

Should you aim for reloading datasources in Grafana each time the config is changed, set `sidecar.datasources.skipReload: false` and adjust `sidecar.datasources.reloadURL` to `http://<svc-name>.<namespace>.svc.cluster.local/api/admin/provisioning/datasources/reload`.

Secrets are recommended over configmaps for this usecase because datasources usually contain private
data like usernames and passwords. Secrets are the more appropriate cluster resource to manage those.

Example values to add a postgres datasource as a kubernetes secret:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: grafana-datasources
  labels:
    grafana_datasource: 'true' # default value for: sidecar.datasources.label
stringData:
  pg-db.yaml: |-
    apiVersion: 1
    datasources:
      - name: My pg db datasource
        type: postgres
        url: my-postgresql-db:5432
        user: db-readonly-user
        secureJsonData:
          password: 'SUperSEcretPa$$word'
        jsonData:
          database: my_datase
          sslmode: 'disable' # disable/require/verify-ca/verify-full
          maxOpenConns: 0 # Grafana v5.4+
          maxIdleConns: 2 # Grafana v5.4+
          connMaxLifetime: 14400 # Grafana v5.4+
          postgresVersion: 1000 # 903=9.3, 904=9.4, 905=9.5, 906=9.6, 1000=10
          timescaledb: false
        # <bool> allow users to edit datasources from the UI.
        editable: false
```

Example values to add a datasource adapted from [Grafana](http://docs.grafana.org/administration/provisioning/#example-datasource-config-file):

```yaml
datasources:
 datasources.yaml:
   apiVersion: 1
   datasources:
      # <string, required> name of the datasource. Required
    - name: Graphite
      # <string, required> datasource type. Required
      type: graphite
      # <string, required> access mode. proxy or direct (Server or Browser in the UI). Required
      access: proxy
      # <int> org id. will default to orgId 1 if not specified
      orgId: 1
      # <string> url
      url: http://localhost:8080
      # <string> database password, if used
      password:
      # <string> database user, if used
      user:
      # <string> database name, if used
      database:
      # <bool> enable/disable basic auth
      basicAuth:
      # <string> basic auth username
      basicAuthUser:
      # <string> basic auth password
      basicAuthPassword:
      # <bool> enable/disable with credentials headers
      withCredentials:
      # <bool> mark as default datasource. Max one per org
      isDefault:
      # <map> fields that will be converted to json and stored in json_data
      jsonData:
         graphiteVersion: "1.1"
         tlsAuth: true
         tlsAuthWithCACert: true
      # <string> json object of data that will be encrypted.
      secureJsonData:
        tlsCACert: "..."
        tlsClientCert: "..."
        tlsClientKey: "..."
      version: 1
      # <bool> allow users to edit datasources from the UI.
      editable: false
```

## Sidecar for notifiers

If the parameter `sidecar.notifiers.enabled` is set, an init container is deployed in the grafana
pod. This container lists all secrets (or configmaps, though not recommended) in the cluster and
filters out the ones with a label as defined in `sidecar.notifiers.label`. The files defined in
those secrets are written to a folder and accessed by grafana on startup. Using these yaml files,
the notification channels in grafana can be imported. The secrets must be created before
`helm install` so that the notifiers init container can list the secrets.

Secrets are recommended over configmaps for this usecase because alert notification channels usually contain
private data like SMTP usernames and passwords. Secrets are the more appropriate cluster resource to manage those.

Example datasource config adapted from [Grafana](https://grafana.com/docs/grafana/latest/administration/provisioning/#alert-notification-channels):

```yaml
notifiers:
  - name: notification-channel-1
    type: slack
    uid: notifier1
    # either
    org_id: 2
    # or
    org_name: Main Org.
    is_default: true
    send_reminder: true
    frequency: 1h
    disable_resolve_message: false
    # See `Supported Settings` section for settings supporter for each
    # alert notification type.
    settings:
      recipient: 'XXX'
      token: 'xoxb'
      uploadImage: true
      url: https://slack.com

delete_notifiers:
  - name: notification-channel-1
    uid: notifier1
    org_id: 2
  - name: notification-channel-2
    # default org_id: 1
```

## Sidecar for alerting resources

If the parameter `sidecar.alerts.enabled` is set, a sidecar container is deployed in the grafana
pod. This container watches all configmaps (or secrets) in the cluster (namespace defined by `sidecar.alerts.searchNamespace`) and filters out the ones with
a label as defined in `sidecar.alerts.label` (default is `grafana_alert`). The files defined in those configmaps are written
to a folder and accessed by grafana. Changes to the configmaps are monitored and the imported alerting resources are updated, however, deletions are a little more complicated (see below).

This sidecar can be used to provision alert rules, contact points, notification policies, notification templates and mute timings as shown in [Grafana Documentation](https://grafana.com/docs/grafana/next/alerting/set-up/provision-alerting-resources/file-provisioning/).

To fetch the alert config which will be provisioned, use the alert provisioning API ([Grafana Documentation](https://grafana.com/docs/grafana/next/developers/http_api/alerting_provisioning/)).
You can use either JSON or YAML format.

Example config for an alert rule:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sample-grafana-alert
  labels:
     grafana_alert: "1"
data:
  k8s-alert.yml: |-
    apiVersion: 1
    groups:
        - orgId: 1
          name: k8s-alert
          [...]
```

To delete provisioned alert rules is a two step process, you need to delete the configmap which defined the alert rule
and then create a configuration which deletes the alert rule.

Example deletion configuration:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: delete-sample-grafana-alert
  namespace: monitoring
  labels:
    grafana_alert: "1"
data:
  delete-k8s-alert.yml: |-
    apiVersion: 1
    deleteRules:
      - orgId: 1
        uid: 16624780-6564-45dc-825c-8bded4ad92d3
```

## Statically provision alerting resources
If you don't need to change alerting resources (alert rules, contact points, notification policies and notification templates) regularly you could use the `alerting` config option instead of the sidecar option above.
This will grab the alerting config and apply it statically at build time for the helm file.

There are two methods to statically provision alerting configuration in Grafana. Below are some examples and explanations as to how to use each method:

```yaml
alerting:
  team1-alert-rules.yaml:
    file: alerting/team1/rules.yaml
  team2-alert-rules.yaml:
    file: alerting/team2/rules.yaml
  team3-alert-rules.yaml:
    file: alerting/team3/rules.yaml
  notification-policies.yaml:
    file: alerting/shared/notification-policies.yaml
  notification-templates.yaml:
    file: alerting/shared/notification-templates.yaml
  contactpoints.yaml:
    apiVersion: 1
    contactPoints:
      - orgId: 1
        name: Slack channel
        receivers:
          - uid: default-receiver
            type: slack
            settings:
              # Webhook URL to be filled in
              url: ""
              # We need to escape double curly braces for the tpl function.
              text: '{{ `{{ template "default.message" . }}` }}'
              title: '{{ `{{ template "default.title" . }}` }}'
```

The two possibilities for static alerting resource provisioning are:

* Inlining the file contents as shown for contact points in the above example.
* Importing a file using a relative path starting from the chart root directory as shown for the alert rules in the above example.

### Important notes on file provisioning

* The format of the files is defined in the [Grafana documentation](https://grafana.com/docs/grafana/next/alerting/set-up/provision-alerting-resources/file-provisioning/) on file provisioning.
* The chart supports importing YAML and JSON files.
* The filename must be unique, otherwise one volume mount will overwrite the other.
* In case of inlining, double curly braces that arise from the Grafana configuration format and are not intended as templates for the chart must be escaped.
* The number of total files under `alerting:` is not limited. Each file will end up as a volume mount in the corresponding provisioning folder of the deployed Grafana instance.
* The file size for each import is limited by what the function `.Files.Get` can handle, which suffices for most cases.

## How to serve Grafana with a path prefix (/grafana)

In order to serve Grafana with a prefix (e.g., <http://example.com/grafana>), add the following to your values.yaml.

```yaml
ingress:
  enabled: true
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/rewrite-target: /$1
    nginx.ingress.kubernetes.io/use-regex: "true"

  path: /grafana/?(.*)
  hosts:
    - k8s.example.dev

grafana.ini:
  server:
    root_url: http://localhost:3000/grafana # this host can be localhost
```

## How to securely reference secrets in grafana.ini

This example uses Grafana [file providers](https://grafana.com/docs/grafana/latest/administration/configuration/#file-provider) for secret values and the `extraSecretMounts` configuration flag (Additional grafana server secret mounts) to mount the secrets.

In grafana.ini:

```yaml
grafana.ini:
  [auth.generic_oauth]
  enabled = true
  client_id = $__file{/etc/secrets/auth_generic_oauth/client_id}
  client_secret = $__file{/etc/secrets/auth_generic_oauth/client_secret}
```

Existing secret, or created along with helm:

```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: auth-generic-oauth-secret
type: Opaque
stringData:
  client_id: <value>
  client_secret: <value>
```

Include in the `extraSecretMounts` configuration flag:

```yaml
- extraSecretMounts:
  - name: auth-generic-oauth-secret-mount
    secretName: auth-generic-oauth-secret
    defaultMode: 0440
    mountPath: /etc/secrets/auth_generic_oauth
    readOnly: true
```

### extraSecretMounts using a Container Storage Interface (CSI) provider

This example uses a CSI driver e.g. retrieving secrets using [Azure Key Vault Provider](https://github.com/Azure/secrets-store-csi-driver-provider-azure)

```yaml
- extraSecretMounts:
  - name: secrets-store-inline
    mountPath: /run/secrets
    readOnly: true
    csi:
      driver: secrets-store.csi.k8s.io
      readOnly: true
      volumeAttributes:
        secretProviderClass: "my-provider"
      nodePublishSecretRef:
        name: akv-creds
```

## Image Renderer Plug-In

This chart supports enabling [remote image rendering](https://github.com/grafana/grafana-image-renderer/blob/master/README.md#run-in-docker)

```yaml
imageRenderer:
  enabled: true
```

### Image Renderer NetworkPolicy

By default the image-renderer pods will have a network policy which only allows ingress traffic from the created grafana instance

### High Availability for unified alerting

If you want to run Grafana in a high availability cluster you need to enable
the headless service by setting `headlessService: true` in your `values.yaml`
file.

As next step you have to setup the `grafana.ini` in your `values.yaml` in a way
that it will make use of the headless service to obtain all the IPs of the
cluster. You should replace ``{{ Name }}`` with the name of your helm deployment.

```yaml
grafana.ini:
  ...
  unified_alerting:
    enabled: true
    ha_peers: {{ Name }}-headless:9094
    ha_listen_address: ${POD_IP}:9094
    ha_advertise_address: ${POD_IP}:9094

  alerting:
    enabled: false
=======
# kube-prometheus-stack

Installs the [kube-prometheus stack](https://github.com/prometheus-operator/kube-prometheus), a collection of Kubernetes manifests, [Grafana](http://grafana.com/) dashboards, and [Prometheus rules](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/) combined with documentation and scripts to provide easy to operate end-to-end Kubernetes cluster monitoring with [Prometheus](https://prometheus.io/) using the [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator).

See the [kube-prometheus](https://github.com/prometheus-operator/kube-prometheus) README for details about components, dashboards, and alerts.

_Note: This chart was formerly named `prometheus-operator` chart, now renamed to more clearly reflect that it installs the `kube-prometheus` project stack, within which Prometheus Operator is only one component._

## Prerequisites

- Kubernetes 1.19+
- Helm 3+

## Get Helm Repository Info

```console
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

_See [`helm repo`](https://helm.sh/docs/helm/helm_repo/) for command documentation._

## Install Helm Chart

```console
helm install [RELEASE_NAME] prometheus-community/kube-prometheus-stack
```

_See [configuration](#configuration) below._

_See [helm install](https://helm.sh/docs/helm/helm_install/) for command documentation._

## Dependencies

By default this chart installs additional, dependent charts:

- [prometheus-community/kube-state-metrics](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-state-metrics)
- [prometheus-community/prometheus-node-exporter](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-node-exporter)
- [grafana/grafana](https://github.com/grafana/helm-charts/tree/main/charts/grafana)

To disable dependencies during installation, see [multiple releases](#multiple-releases) below.

_See [helm dependency](https://helm.sh/docs/helm/helm_dependency/) for command documentation._

## Uninstall Helm Chart

```console
helm uninstall [RELEASE_NAME]
```

This removes all the Kubernetes components associated with the chart and deletes the release.

_See [helm uninstall](https://helm.sh/docs/helm/helm_uninstall/) for command documentation._

CRDs created by this chart are not removed by default and should be manually cleaned up:

```console
kubectl delete crd alertmanagerconfigs.monitoring.coreos.com
kubectl delete crd alertmanagers.monitoring.coreos.com
kubectl delete crd podmonitors.monitoring.coreos.com
kubectl delete crd probes.monitoring.coreos.com
kubectl delete crd prometheusagents.monitoring.coreos.com
kubectl delete crd prometheuses.monitoring.coreos.com
kubectl delete crd prometheusrules.monitoring.coreos.com
kubectl delete crd scrapeconfigs.monitoring.coreos.com
kubectl delete crd servicemonitors.monitoring.coreos.com
kubectl delete crd thanosrulers.monitoring.coreos.com
```

## Upgrading Chart

```console
helm upgrade [RELEASE_NAME] prometheus-community/kube-prometheus-stack
```

With Helm v3, CRDs created by this chart are not updated by default and should be manually updated.
Consult also the [Helm Documentation on CRDs](https://helm.sh/docs/chart_best_practices/custom_resource_definitions).

_See [helm upgrade](https://helm.sh/docs/helm/helm_upgrade/) for command documentation._

### Upgrading an existing Release to a new major version

A major chart version change (like v1.2.3 -> v2.0.0) indicates that there is an incompatible breaking change needing manual actions.

### From 59.x to 60.x

This version upgrades the Grafana chart to v8.0.x which introduces Grafana 11. This new major version of Grafana contains some breaking changes described in [Breaking changes in Grafana v11.0](https://grafana.com/docs/grafana/latest/breaking-changes/breaking-changes-v11-0/).

### From 58.x to 59.x

This version upgrades Prometheus-Operator to v0.74.0

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.74.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.74.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.74.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.74.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.74.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusagents.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.74.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.74.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.74.0/example/prometheus-operator-crd/monitoring.coreos.com_scrapeconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.74.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.74.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 57.x to 58.x

This version upgrades Prometheus-Operator to v0.73.0

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.73.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.73.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.73.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.73.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.73.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusagents.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.73.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.73.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.73.0/example/prometheus-operator-crd/monitoring.coreos.com_scrapeconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.73.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.73.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 56.x to 57.x

This version upgrades Prometheus-Operator to v0.72.0

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.72.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.72.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.72.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.72.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.72.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusagents.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.72.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.72.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.72.0/example/prometheus-operator-crd/monitoring.coreos.com_scrapeconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.72.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.72.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 55.x to 56.x

This version upgrades Prometheus-Operator to v0.71.0, Prometheus to 2.49.1

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.71.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.71.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.71.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.71.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.71.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusagents.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.71.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.71.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.71.0/example/prometheus-operator-crd/monitoring.coreos.com_scrapeconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.71.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.71.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 54.x to 55.x

This version upgrades Prometheus-Operator to v0.70.0

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.70.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.70.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.70.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.70.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.70.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusagents.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.70.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.70.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.70.0/example/prometheus-operator-crd/monitoring.coreos.com_scrapeconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.70.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.70.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 53.x to 54.x

Grafana Helm Chart has bumped to version 7

Please note Grafana Helm Chart [changelog](https://github.com/grafana/helm-charts/tree/main/charts/grafana#to-700).

### From 52.x to 53.x

This version upgrades Prometheus-Operator to v0.69.1, Prometheus to 2.47.2

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.69.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.69.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.69.1/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.69.1/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.69.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheusagents.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.69.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.69.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.69.1/example/prometheus-operator-crd/monitoring.coreos.com_scrapeconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.69.1/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.69.1/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 51.x to 52.x

This includes the ability to select between using existing secrets or create new secret objects for various thanos config. The defaults have not changed but if you were setting:

- `thanosRuler.thanosRulerSpec.alertmanagersConfig` or
- `thanosRuler.thanosRulerSpec.objectStorageConfig` or
- `thanosRuler.thanosRulerSpec.queryConfig` or
- `prometheus.prometheusSpec.thanos.objectStorageConfig`

you will have to need to set `existingSecret` or `secret` based on your requirement

For instance, the `thanosRuler.thanosRulerSpec.alertmanagersConfig` used to be configured as follow:

```yaml
thanosRuler:
  thanosRulerSpec:
    alertmanagersConfig:
      alertmanagers:
        - api_version: v2
          http_config:
            basic_auth:
              username: some_user
              password: some_pass
          static_configs:
            - alertmanager.thanos.io
          scheme: http
          timeout: 10s
```

But it now moved to:

```yaml
thanosRuler:
  thanosRulerSpec:
    alertmanagersConfig:
      secret:
        alertmanagers:
          - api_version: v2
            http_config:
              basic_auth:
                username: some_user
                password: some_pass
            static_configs:
              - alertmanager.thanos.io
            scheme: http
            timeout: 10s
```

or the `thanosRuler.thanosRulerSpec.objectStorageConfig` used to be configured as follow:

```yaml
thanosRuler:
  thanosRulerSpec:
    objectStorageConfig:
      name: existing-secret-not-created-by-this-chart
      key: object-storage-configs.yaml
```

But it now moved to:

```yaml
thanosRuler:
  thanosRulerSpec:
    objectStorageConfig:
      existingSecret:
        name: existing-secret-not-created-by-this-chart
        key: object-storage-configs.yaml
```

### From 50.x to 51.x

This version upgrades Prometheus-Operator to v0.68.0, Prometheus to 2.47.0 and Thanos to v0.32.2

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.68.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.68.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.68.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.68.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.68.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusagents.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.68.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.68.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.68.0/example/prometheus-operator-crd/monitoring.coreos.com_scrapeconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.68.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.68.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 49.x to 50.x

This version requires Kubernetes 1.19+.

We do not expect any breaking changes in this version.

### From 48.x to 49.x

This version upgrades Prometheus-Operator to v0.67.1, 0, Alertmanager to v0.26.0, Prometheus to 2.46.0 and Thanos to v0.32.0

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.67.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.67.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.67.1/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.67.1/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.67.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheusagents.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.67.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.67.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.67.1/example/prometheus-operator-crd/monitoring.coreos.com_scrapeconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.67.1/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.67.1/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 47.x to 48.x

This version moved all CRDs into a dedicated sub-chart. No new CRDs are introduced in this version.
See [#3548](https://github.com/prometheus-community/helm-charts/issues/3548) for more context.

We do not expect any breaking changes in this version.

### From 46.x to 47.x

This version upgrades Prometheus-Operator to v0.66.0 with new CRDs (PrometheusAgent and ScrapeConfig).

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.66.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.66.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.66.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.66.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.66.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusagents.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.66.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.66.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.66.0/example/prometheus-operator-crd/monitoring.coreos.com_scrapeconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.66.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.66.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 45.x to 46.x

This version upgrades Prometheus-Operator to v0.65.1 with new CRDs (PrometheusAgent and ScrapeConfig), Prometheus to v2.44.0 and Thanos to v0.31.0.

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.65.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.65.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.65.1/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.65.1/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.65.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheusagents.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.65.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.65.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.65.1/example/prometheus-operator-crd/monitoring.coreos.com_scrapeconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.65.1/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.65.1/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 44.x to 45.x

This version upgrades Prometheus-Operator to v0.63.0, Prometheus to v2.42.0 and Thanos to v0.30.2.

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.63.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.63.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.63.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.63.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.63.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.63.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.63.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.63.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 43.x to 44.x

This version upgrades Prometheus-Operator to v0.62.0, Prometheus to v2.41.0 and Thanos to v0.30.1.

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.62.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.62.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.62.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.62.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.62.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.62.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.62.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.62.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

If you have explicitly set `prometheusOperator.admissionWebhooks.failurePolicy`, this value is now always used even when `.prometheusOperator.admissionWebhooks.patch.enabled` is `true` (the default).

The values for `prometheusOperator.image.tag` & `prometheusOperator.prometheusConfigReloader.image.tag` are now empty by default and the Chart.yaml `appVersion` field is used instead.

### From 42.x to 43.x

This version upgrades Prometheus-Operator to v0.61.1, Prometheus to v2.40.5 and Thanos to v0.29.0.

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.61.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.61.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.61.1/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.61.1/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.61.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.61.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.61.1/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.61.1/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 41.x to 42.x

This includes the overridability of container registry for all containers at the global level using `global.imageRegistry` or per container image. The defaults have not changed but if you were using a custom image, you will have to override the registry of said custom container image before you upgrade.

For instance, the prometheus-config-reloader used to be configured as follow:

```yaml
    image:
      repository: quay.io/prometheus-operator/prometheus-config-reloader
      tag: v0.60.1
      sha: ""
```

But it now moved to:

```yaml
    image:
      registry: quay.io
      repository: prometheus-operator/prometheus-config-reloader
      tag: v0.60.1
      sha: ""
```

### From 40.x to 41.x

This version upgrades Prometheus-Operator to v0.60.1, Prometheus to v2.39.1 and Thanos to v0.28.1.
This version also upgrades the Helm charts of kube-state-metrics to 4.20.2, prometheus-node-exporter to 4.3.0 and Grafana to 6.40.4.

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.60.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.60.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.60.1/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.60.1/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.60.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.60.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.60.1/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.60.1/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

This version splits kubeScheduler recording and altering rules in separate config values.
Instead of `defaultRules.rules.kubeScheduler` the 2 new variables `defaultRules.rules.kubeSchedulerAlerting` and `defaultRules.rules.kubeSchedulerRecording` are used.

### From 39.x to 40.x

This version upgrades Prometheus-Operator to v0.59.1, Prometheus to v2.38.0, kube-state-metrics to v2.6.0 and Thanos to v0.28.0.
This version also upgrades the Helm charts of kube-state-metrics to 4.18.0 and prometheus-node-exporter to 4.2.0.

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.59.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.59.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.59.1/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.59.1/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.59.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.59.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.59.1/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.59.1/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

Starting from prometheus-node-exporter version 4.0.0, the `node exporter` chart is using the [Kubernetes recommended labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/). Therefore you have to delete the daemonset before you upgrade.

```console
kubectl delete daemonset -l app=prometheus-node-exporter
helm upgrade -i kube-prometheus-stack prometheus-community/kube-prometheus-stack
```

If you use your own custom [ServiceMonitor](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#servicemonitor) or [PodMonitor](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#podmonitor), please ensure to upgrade their `selector` fields accordingly to the new labels.

### From 38.x to 39.x

This upgraded prometheus-operator to v0.58.0 and prometheus to v2.37.0

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.58.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.58.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.58.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.58.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.58.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.58.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.58.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.58.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 37.x to 38.x

Reverted one of the default metrics relabelings for cAdvisor added in 36.x, due to it breaking container_network_* and various other statistics. If you do not want this change, you will need to override the `kubelet.cAdvisorMetricRelabelings`.

### From 36.x to 37.x

This includes some default metric relabelings for cAdvisor and apiserver metrics to reduce cardinality. If you do not want these defaults, you will need to override the `kubeApiServer.metricRelabelings` and or `kubelet.cAdvisorMetricRelabelings`.

### From 35.x to 36.x

This upgraded prometheus-operator to v0.57.0 and prometheus to v2.36.1

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.57.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.57.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.57.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.57.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.57.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.57.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.57.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.57.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 34.x to 35.x

This upgraded prometheus-operator to v0.56.0 and prometheus to v2.35.0

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.56.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.56.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.56.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.56.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.56.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.56.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.56.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.56.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 33.x to 34.x

This upgrades to prometheus-operator to v0.55.0 and prometheus to v2.33.5.

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.55.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.55.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.55.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.55.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.55.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.55.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.55.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.55.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 32.x to 33.x

This upgrades the prometheus-node-exporter Chart to v3.0.0. Please review the changes to this subchart if you make customizations to hostMountPropagation.

### From 31.x to 32.x

This upgrades to prometheus-operator to v0.54.0 and prometheus to v2.33.1. It also changes the default for `grafana.serviceMonitor.enabled` to `true.

Run these commands to update the CRDs before applying the upgrade.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.54.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.54.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.54.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.54.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.54.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.54.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.54.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.54.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 30.x to 31.x

This version removes the built-in grafana ServiceMonitor and instead relies on the ServiceMonitor of the sub-chart.
`grafana.serviceMonitor.enabled` must be set instead of `grafana.serviceMonitor.selfMonitor` and the old ServiceMonitor may
need to be manually cleaned up after deploying the new release.

### From 29.x to 30.x

This version updates kube-state-metrics to 4.3.0 and uses the new option `kube-state-metrics.releaseLabel=true` which adds the "release" label to kube-state-metrics labels, making scraping of the metrics by kube-prometheus-stack work out of the box again, independent of the used kube-prometheus-stack release name. If you already set the "release" label via `kube-state-metrics.customLabels` you might have to remove that and use it via the new option.

### From 28.x to 29.x

This version makes scraping port for kube-controller-manager and kube-scheduler dynamic to reflect changes to default serving ports
for those components in Kubernetes versions v1.22 and v1.23 respectively.

If you deploy on clusters using version v1.22+, kube-controller-manager will be scraped over HTTPS on port 10257.

If you deploy on clusters running version v1.23+, kube-scheduler will be scraped over HTTPS on port 10259.

### From 27.x to 28.x

This version disables PodSecurityPolicies by default because they are deprecated in Kubernetes 1.21 and will be removed in Kubernetes 1.25.

If you are using PodSecurityPolicies you can enable the previous behaviour by setting `kube-state-metrics.podSecurityPolicy.enabled`, `prometheus-node-exporter.rbac.pspEnabled`, `grafana.rbac.pspEnabled` and `global.rbac.pspEnabled` to `true`.

### From 26.x to 27.x

This version splits prometheus-node-exporter chart recording and altering rules in separate config values.
Instead of `defaultRules.rules.node` the 2 new variables `defaultRules.rules.nodeExporterAlerting` and `defaultRules.rules.nodeExporterRecording` are used.

Also the following defaultRules.rules has been removed as they had no effect: `kubeApiserverError`, `kubePrometheusNodeAlerting`, `kubernetesAbsent`, `time`.

The ability to set a rubookUrl via `defaultRules.rules.rubookUrl` was reintroduced.

### From 25.x to 26.x

This version enables the prometheus-node-exporter subchart servicemonitor by default again, by setting `prometheus-node-exporter.prometheus.monitor.enabled` to `true`.

### From 24.x to 25.x

This version upgrade to prometheus-operator v0.53.1. It removes support for setting a runbookUrl, since the upstream format for runbooks changed.

```console
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.53.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.53.1/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.53.1/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.53.1/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.53.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.53.1/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.53.1/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply --server-side -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.53.1/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 23.x to 24.x

The custom `ServiceMonitor` for the _kube-state-metrics_ & _prometheus-node-exporter_ charts have been removed in favour of the built-in sub-chart `ServiceMonitor`; for both sub-charts this means that `ServiceMonitor` customisations happen via the values passed to the chart. If you haven't directly customised this behaviour then there are no changes required to upgrade, but if you have please read the following.

For _kube-state-metrics_ the `ServiceMonitor` customisation is now set via `kube-state-metrics.prometheus.monitor` and the `kubeStateMetrics.serviceMonitor.selfMonitor.enabled` value has moved to `kube-state-metrics.selfMonitor.enabled`.

For _prometheus-node-exporter_ the `ServiceMonitor` customisation is now set via `prometheus-node-exporter.prometheus.monitor` and the `nodeExporter.jobLabel` values has moved to `prometheus-node-exporter.prometheus.monitor.jobLabel`.

### From 22.x to 23.x

Port names have been renamed for Istio's
[explicit protocol selection](https://istio.io/latest/docs/ops/configuration/traffic-management/protocol-selection/#explicit-protocol-selection).

| | old value | new value |
|-|-----------|-----------|
| `alertmanager.alertmanagerSpec.portName` | `web` | `http-web` |
| `grafana.service.portName` | `service` | `http-web` |
| `prometheus-node-exporter.service.portName` | `metrics` (hardcoded) | `http-metrics` |
| `prometheus.prometheusSpec.portName` | `web` | `http-web` |

### From 21.x to 22.x

Due to the upgrade of the `kube-state-metrics` chart, removal of its deployment/stateful needs to done manually prior to upgrading:

```console
kubectl delete deployments.apps -l app.kubernetes.io/instance=prometheus-operator,app.kubernetes.io/name=kube-state-metrics --cascade=orphan
```

or if you use autosharding:

```console
kubectl delete statefulsets.apps -l app.kubernetes.io/instance=prometheus-operator,app.kubernetes.io/name=kube-state-metrics --cascade=orphan
```

### From 20.x to 21.x

The config reloader values have been refactored. All the values have been moved to the key `prometheusConfigReloader` and the limits and requests can now be set separately.

### From 19.x to 20.x

Version 20 upgrades prometheus-operator from 0.50.x to 0.52.x. Helm does not automatically upgrade or install new CRDs on a chart upgrade, so you have to install the CRDs manually before updating:

```console
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.52.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.52.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.52.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.52.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.52.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.52.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.52.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.52.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 18.x to 19.x

`kubeStateMetrics.serviceMonitor.namespaceOverride` was removed.
Please use `kube-state-metrics.namespaceOverride` instead.

### From 17.x to 18.x

Version 18 upgrades prometheus-operator from 0.49.x to 0.50.x. Helm does not automatically upgrade or install new CRDs on a chart upgrade, so you have to install the CRDs manually before updating:

```console
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.50.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.50.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.50.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.50.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.50.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.50.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.50.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.50.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 16.x to 17.x

Version 17 upgrades prometheus-operator from 0.48.x to 0.49.x. Helm does not automatically upgrade or install new CRDs on a chart upgrade, so you have to install the CRDs manually before updating:

```console
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.49.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.49.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.49.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.49.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.49.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.49.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.49.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.49.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 15.x to 16.x

Version 16 upgrades kube-state-metrics to v2.0.0. This includes changed command-line arguments and removed metrics, see this [blog post](https://kubernetes.io/blog/2021/04/13/kube-state-metrics-v-2-0/). This version also removes Grafana dashboards that supported Kubernetes 1.14 or earlier.

### From 14.x to 15.x

Version 15 upgrades prometheus-operator from 0.46.x to 0.47.x. Helm does not automatically upgrade or install new CRDs on a chart upgrade, so you have to install the CRDs manually before updating:

```console
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.47.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.47.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.47.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.47.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.47.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.47.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.47.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 13.x to 14.x

Version 14 upgrades prometheus-operator from 0.45.x to 0.46.x. Helm does not automatically upgrade or install new CRDs on a chart upgrade, so you have to install the CRDs manually before updating:

```console
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.46.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.46.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.46.0/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.46.0/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.46.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.46.0/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.46.0/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
```

### From 12.x to 13.x

Version 13 upgrades prometheus-operator from 0.44.x to 0.45.x. Helm does not automatically upgrade or install new CRDs on a chart upgrade, so you have to install the CRD manually before updating:

```console
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.45.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.45.0/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/v0.45.0/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
```

### From 11.x to 12.x

Version 12 upgrades prometheus-operator from 0.43.x to 0.44.x. Helm does not automatically upgrade or install new CRDs on a chart upgrade, so you have to install the CRD manually before updating:

```console
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.44/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
```

The chart was migrated to support only helm v3 and later.

### From 10.x to 11.x

Version 11 upgrades prometheus-operator from 0.42.x to 0.43.x. Starting with 0.43.x an additional `AlertmanagerConfigs` CRD is introduced. Helm does not automatically upgrade or install new CRDs on a chart upgrade, so you have to install the CRD manually before updating:

```console
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.43/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagerconfigs.yaml
```

Version 11 removes the deprecated tlsProxy via ghostunnel in favor of native TLS support the prometheus-operator gained with v0.39.0.

### From 9.x to 10.x

Version 10 upgrades prometheus-operator from 0.38.x to 0.42.x. Starting with 0.40.x an additional `Probes` CRD is introduced. Helm does not automatically upgrade or install new CRDs on a chart upgrade, so you have to install the CRD manually before updating:

```console
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
```

### From 8.x to 9.x

Version 9 of the helm chart removes the existing `additionalScrapeConfigsExternal` in favour of `additionalScrapeConfigsSecret`. This change lets users specify the secret name and secret key to use for the additional scrape configuration of prometheus. This is useful for users that have prometheus-operator as a subchart and also have a template that creates the additional scrape configuration.

### From 7.x to 8.x

Due to new template functions being used in the rules in version 8.x.x of the chart, an upgrade to Prometheus Operator and Prometheus is necessary in order to support them. First, upgrade to the latest version of 7.x.x

```console
helm upgrade [RELEASE_NAME] prometheus-community/kube-prometheus-stack --version 7.5.0
```

Then upgrade to 8.x.x

```console
helm upgrade [RELEASE_NAME] prometheus-community/kube-prometheus-stack --version [8.x.x]
```

Minimal recommended Prometheus version for this chart release is `2.12.x`

### From 6.x to 7.x

Due to a change in grafana subchart, version 7.x.x now requires Helm >= 2.12.0.

### From 5.x to 6.x

Due to a change in deployment labels of kube-state-metrics, the upgrade requires `helm upgrade --force` in order to re-create the deployment. If this is not done an error will occur indicating that the deployment cannot be modified:

```console
invalid: spec.selector: Invalid value: v1.LabelSelector{MatchLabels:map[string]string{"app.kubernetes.io/name":"kube-state-metrics"}, MatchExpressions:[]v1.LabelSelectorRequirement(nil)}: field is immutable
```

If this error has already been encountered, a `helm history` command can be used to determine which release has worked, then `helm rollback` to the release, then `helm upgrade --force` to this new one

## Configuration

See [Customizing the Chart Before Installing](https://helm.sh/docs/intro/using_helm/#customizing-the-chart-before-installing). To see all configurable options with detailed comments:

```console
helm show values prometheus-community/kube-prometheus-stack
```

You may also `helm show values` on this chart's [dependencies](#dependencies) for additional options.

### Multiple releases

The same chart can be used to run multiple Prometheus instances in the same cluster if required. To achieve this, it is necessary to run only one instance of prometheus-operator and a pair of alertmanager pods for an HA configuration, while all other components need to be disabled. To disable a dependency during installation, set `kubeStateMetrics.enabled`, `nodeExporter.enabled` and `grafana.enabled` to `false`.

## Work-Arounds for Known Issues

### Running on private GKE clusters

When Google configure the control plane for private clusters, they automatically configure VPC peering between your Kubernetes cluster’s network and a separate Google managed project. In order to restrict what Google are able to access within your cluster, the firewall rules configured restrict access to your Kubernetes pods. This means that in order to use the webhook component with a GKE private cluster, you must configure an additional firewall rule to allow the GKE control plane access to your webhook pod.

You can read more information on how to add firewall rules for the GKE control plane nodes in the [GKE docs](https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters#add_firewall_rules)

Alternatively, you can disable the hooks by setting `prometheusOperator.admissionWebhooks.enabled=false`.

## PrometheusRules Admission Webhooks

With Prometheus Operator version 0.30+, the core Prometheus Operator pod exposes an endpoint that will integrate with the `validatingwebhookconfiguration` Kubernetes feature to prevent malformed rules from being added to the cluster.

### How the Chart Configures the Hooks

A validating and mutating webhook configuration requires the endpoint to which the request is sent to use TLS. It is possible to set up custom certificates to do this, but in most cases, a self-signed certificate is enough. The setup of this component requires some more complex orchestration when using helm. The steps are created to be idempotent and to allow turning the feature on and off without running into helm quirks.

1. A pre-install hook provisions a certificate into the same namespace using a format compatible with provisioning using end user certificates. If the certificate already exists, the hook exits.
2. The prometheus operator pod is configured to use a TLS proxy container, which will load that certificate.
3. Validating and Mutating webhook configurations are created in the cluster, with their failure mode set to Ignore. This allows rules to be created by the same chart at the same time, even though the webhook has not yet been fully set up - it does not have the correct CA field set.
4. A post-install hook reads the CA from the secret created by step 1 and patches the Validating and Mutating webhook configurations. This process will allow a custom CA provisioned by some other process to also be patched into the webhook configurations. The chosen failure policy is also patched into the webhook configurations

### Alternatives

It should be possible to use [jetstack/cert-manager](https://github.com/jetstack/cert-manager) if a more complete solution is required, but it has not been tested.

You can enable automatic self-signed TLS certificate provisioning via cert-manager by setting the `prometheusOperator.admissionWebhooks.certManager.enabled` value to true.

### Limitations

Because the operator can only run as a single pod, there is potential for this component failure to cause rule deployment failure. Because this risk is outweighed by the benefit of having validation, the feature is enabled by default.

## Developing Prometheus Rules and Grafana Dashboards

This chart Grafana Dashboards and Prometheus Rules are just a copy from [prometheus-operator/prometheus-operator](https://github.com/prometheus-operator/prometheus-operator) and other sources, synced (with alterations) by scripts in [hack](hack) folder. In order to introduce any changes you need to first [add them to the original repository](https://github.com/prometheus-operator/kube-prometheus/blob/main/docs/customizations/developing-prometheus-rules-and-grafana-dashboards.md) and then sync there by scripts.

## Further Information

For more in-depth documentation of configuration options meanings, please see

- [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
- [Prometheus](https://prometheus.io/docs/introduction/overview/)
- [Grafana](https://github.com/grafana/helm-charts/tree/main/charts/grafana#grafana-helm-chart)

## prometheus.io/scrape

The prometheus operator does not support annotation-based discovery of services, using the `PodMonitor` or `ServiceMonitor` CRD in its place as they provide far more configuration options.
For information on how to use PodMonitors/ServiceMonitors, please see the documentation on the `prometheus-operator/prometheus-operator` documentation here:

- [ServiceMonitors](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/user-guides/getting-started.md#include-servicemonitors)
- [PodMonitors](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/user-guides/getting-started.md#include-podmonitors)
- [Running Exporters](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/user-guides/running-exporters.md)

By default, Prometheus discovers PodMonitors and ServiceMonitors within its namespace, that are labeled with the same release tag as the prometheus-operator release.
Sometimes, you may need to discover custom PodMonitors/ServiceMonitors, for example used to scrape data from third-party applications.
An easy way of doing this, without compromising the default PodMonitors/ServiceMonitors discovery, is allowing Prometheus to discover all PodMonitors/ServiceMonitors within its namespace, without applying label filtering.
To do so, you can set `prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues` and `prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues` to `false`.

## Migrating from stable/prometheus-operator chart

## Zero downtime

Since `kube-prometheus-stack` is fully compatible with the `stable/prometheus-operator` chart, a migration without downtime can be achieved.
However, the old name prefix needs to be kept. If you want the new name please follow the step by step guide below (with downtime).

You can override the name to achieve this:

```console
helm upgrade prometheus-operator prometheus-community/kube-prometheus-stack -n monitoring --reuse-values --set nameOverride=prometheus-operator
```

**Note**: It is recommended to run this first with `--dry-run --debug`.

## Redeploy with new name (downtime)

If the **prometheus-operator** values are compatible with the new **kube-prometheus-stack** chart, please follow the below steps for migration:

> The guide presumes that chart is deployed in `monitoring` namespace and the deployments are running there. If in other namespace, please replace the `monitoring` to the deployed namespace.

1. Patch the PersistenceVolume created/used by the prometheus-operator chart to `Retain` claim policy:

    ```console
    kubectl patch pv/<PersistentVolume name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    ```

    **Note:** To execute the above command, the user must have a cluster wide permission. Please refer [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

2. Uninstall the **prometheus-operator** release and delete the existing PersistentVolumeClaim, and verify PV become Released.

    ```console
    helm uninstall prometheus-operator -n monitoring
    kubectl delete pvc/<PersistenceVolumeClaim name> -n monitoring
    ```

    Additionally, you have to manually remove the remaining `prometheus-operator-kubelet` service.

    ```console
    kubectl delete service/prometheus-operator-kubelet -n kube-system
    ```

    You can choose to remove all your existing CRDs (ServiceMonitors, Podmonitors, etc.) if you want to.

3. Remove current `spec.claimRef` values to change the PV's status from Released to Available.

    ```console
    kubectl patch pv/<PersistentVolume name> --type json -p='[{"op": "remove", "path": "/spec/claimRef"}]' -n monitoring
    ```

**Note:** To execute the above command, the user must have a cluster wide permission. Please refer to [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

After these steps, proceed to a fresh **kube-prometheus-stack** installation and make sure the current release of **kube-prometheus-stack** matching the `volumeClaimTemplate` values in the `values.yaml`.

The binding is done via matching a specific amount of storage requested and with certain access modes.

For example, if you had storage specified as this with **prometheus-operator**:

```yaml
volumeClaimTemplate:
  spec:
    storageClassName: gp2
    accessModes: ["ReadWriteOnce"]
    resources:
     requests:
       storage: 50Gi
```

You have to specify matching `volumeClaimTemplate` with 50Gi storage and `ReadWriteOnce` access mode.

Additionally, you should check the current AZ of your legacy installation's PV, and configure the fresh release to use the same AZ as the old one. If the pods are in a different AZ than the PV, the release will fail to bind the existing one, hence creating a new PV.

This can be achieved either by specifying the labels through `values.yaml`, e.g. setting `prometheus.prometheusSpec.nodeSelector` to:

```yaml
nodeSelector:
  failure-domain.beta.kubernetes.io/zone: east-west-1a
```

or passing these values as `--set` overrides during installation.

The new release should now re-attach your previously released PV with its content.

## Migrating from coreos/prometheus-operator chart

The multiple charts have been combined into a single chart that installs prometheus operator, prometheus, alertmanager, grafana as well as the multitude of exporters necessary to monitor a cluster.

There is no simple and direct migration path between the charts as the changes are extensive and intended to make the chart easier to support.

The capabilities of the old chart are all available in the new chart, including the ability to run multiple prometheus instances on a single cluster - you will need to disable the parts of the chart you do not wish to deploy.

You can check out the tickets for this change [here](https://github.com/prometheus-operator/prometheus-operator/issues/592) and [here](https://github.com/helm/charts/pull/6765).

### High-level overview of Changes

#### Added dependencies

The chart has added 3 [dependencies](#dependencies).

- Node-Exporter, Kube-State-Metrics: These components are loaded as dependencies into the chart, and are relatively simple components
- Grafana: The Grafana chart is more feature-rich than this chart - it contains a sidecar that is able to load data sources and dashboards from configmaps deployed into the same cluster. For more information check out the [documentation for the chart](https://github.com/grafana/helm-charts/blob/main/charts/grafana/README.md)

#### Kubelet Service

Because the kubelet service has a new name in the chart, make sure to clean up the old kubelet service in the `kube-system` namespace to prevent counting container metrics twice.

#### Persistent Volumes

If you would like to keep the data of the current persistent volumes, it should be possible to attach existing volumes to new PVCs and PVs that are created using the conventions in the new chart. For example, in order to use an existing Azure disk for a helm release called `prometheus-migration` the following resources can be created:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pvc-prometheus-migration-prometheus-0
spec:
  accessModes:
  - ReadWriteOnce
  azureDisk:
    cachingMode: None
    diskName: pvc-prometheus-migration-prometheus-0
    diskURI: /subscriptions/f5125d82-2622-4c50-8d25-3f7ba3e9ac4b/resourceGroups/sample-migration-resource-group/providers/Microsoft.Compute/disks/pvc-prometheus-migration-prometheus-0
    fsType: ""
    kind: Managed
    readOnly: false
  capacity:
    storage: 1Gi
  persistentVolumeReclaimPolicy: Delete
  storageClassName: prometheus
  volumeMode: Filesystem
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  labels:
    app.kubernetes.io/name: prometheus
    prometheus: prometheus-migration-prometheus
  name: prometheus-prometheus-migration-prometheus-db-prometheus-prometheus-migration-prometheus-0
  namespace: monitoring
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: prometheus
  volumeMode: Filesystem
  volumeName: pvc-prometheus-migration-prometheus-0
```

The PVC will take ownership of the PV and when you create a release using a persistent volume claim template it will use the existing PVCs as they match the naming convention used by the chart. For other cloud providers similar approaches can be used.

#### KubeProxy

The metrics bind address of kube-proxy is default to `127.0.0.1:10249` that prometheus instances **cannot** access to. You should expose metrics by changing `metricsBindAddress` field value to `0.0.0.0:10249` if you want to collect them.

Depending on the cluster, the relevant part `config.conf` will be in ConfigMap `kube-system/kube-proxy` or `kube-system/kube-proxy-config`. For example:

```console
kubectl -n kube-system edit cm kube-proxy
```

```yaml
apiVersion: v1
data:
  config.conf: |-
    apiVersion: kubeproxy.config.k8s.io/v1alpha1
    kind: KubeProxyConfiguration
    # ...
    # metricsBindAddress: 127.0.0.1:10249
    metricsBindAddress: 0.0.0.0:10249
    # ...
  kubeconfig.conf: |-
    # ...
kind: ConfigMap
metadata:
  labels:
    app: kube-proxy
  name: kube-proxy
  namespace: kube-system
>>>>>>> d6b4917e180b0bc8d964785a7de3496d4ef817c0:charts/monitoring/README.md
```

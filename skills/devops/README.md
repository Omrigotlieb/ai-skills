# DevOps Skills for Claude Code

Skills and tools for CI/CD, infrastructure, deployment, and operations.

---

## GitHub Actions Skill

Debug and create GitHub Actions workflows:

```markdown
---
name: github-actions
description: Debug and create GitHub Actions workflows
---

# GitHub Actions

## When to Use
- CI/CD pipeline failures
- Creating new workflows
- Optimizing build times

## Capabilities
- Analyze failed runs
- Create workflow files
- Optimize caching
- Setup matrix builds
- Configure secrets

## Debugging Workflow
1. Fetch failed run logs: `gh run view <id> --log-failed`
2. Identify root cause
3. Propose fix
4. Test locally with act

## Example Command (/project:gha)
"Investigate the latest failed GitHub Actions run and fix it"
```

---

## Docker Skill

```markdown
---
name: docker
description: Dockerfile creation and optimization
---

# Docker

## Capabilities
- Create optimized Dockerfiles
- Multi-stage builds
- Layer caching strategies
- Security best practices
- Docker Compose setup

## Best Practices
- Use specific base image tags
- Minimize layers
- Don't run as root
- Use .dockerignore
- Multi-stage for smaller images

## Example Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
CMD ["node", "dist/index.js"]
```

---

## Kubernetes Skill

```markdown
---
name: kubernetes
description: K8s manifest generation and debugging
---

# Kubernetes

## Capabilities
- Generate manifests (Deployment, Service, ConfigMap)
- Debug pod issues
- Setup Helm charts
- Configure resources and limits
- Ingress configuration

## Debugging Commands
kubectl describe pod <name>
kubectl logs <pod> -f
kubectl get events --sort-by='.lastTimestamp'

## Example
"Create Kubernetes manifests for a Node.js API with 3 replicas"
```

---

## Terraform Skill

```markdown
---
name: terraform
description: Infrastructure as Code with Terraform
---

# Terraform

## Capabilities
- Write HCL configurations
- State management
- Module creation
- Plan analysis
- Drift detection

## Best Practices
- Use remote state
- Lock state during apply
- Use modules for reusability
- Tag all resources
- Use workspaces for environments

## Example
"Create Terraform config for AWS ECS cluster with auto-scaling"
```

---

## CI/CD Pipeline Skill

```markdown
---
name: cicd-pipeline
description: Design and optimize CI/CD pipelines
---

# CI/CD Pipeline Design

## Supported Platforms
- GitHub Actions
- GitLab CI
- CircleCI
- Jenkins
- Azure DevOps

## Pipeline Stages
1. **Lint** - Code quality checks
2. **Test** - Unit and integration tests
3. **Build** - Compile and bundle
4. **Security** - Vulnerability scanning
5. **Deploy** - Environment deployment
6. **Smoke** - Post-deployment verification

## Optimization Tips
- Parallelize independent jobs
- Cache dependencies aggressively
- Use matrix builds wisely
- Fail fast on lint/type errors
```

---

## Deployment Strategies Skill

```markdown
---
name: deployment-strategies
description: Zero-downtime deployment patterns
---

# Deployment Strategies

## Strategies
| Strategy | Risk | Rollback | Use Case |
|----------|------|----------|----------|
| **Rolling** | Low | Slow | Standard updates |
| **Blue-Green** | Low | Fast | Critical apps |
| **Canary** | Very Low | Fast | High-traffic apps |
| **Feature Flags** | Minimal | Instant | Granular control |

## Implementation
- Rolling: K8s default, gradual pod replacement
- Blue-Green: Two identical environments
- Canary: Gradual traffic shift (1% → 10% → 100%)
- Feature Flags: LaunchDarkly, Unleash, custom
```

---

## Monitoring & Observability Skill

```markdown
---
name: observability
description: Setup monitoring, logging, and tracing
---

# Observability

## Three Pillars
1. **Metrics** - Quantitative measurements
2. **Logs** - Event records
3. **Traces** - Request flow tracking

## Tools
| Pillar | Tools |
|--------|-------|
| Metrics | Prometheus, Grafana, DataDog |
| Logs | ELK, Loki, CloudWatch |
| Traces | Jaeger, Zipkin, X-Ray |

## Key Metrics
- **RED** (Request Rate, Error Rate, Duration)
- **USE** (Utilization, Saturation, Errors)
- **Four Golden Signals** (Latency, Traffic, Errors, Saturation)
```

---

## Incident Response Skill

```markdown
---
name: incident-response
description: Structured incident handling
---

# Incident Response

## Response Flow
1. **Detect** - Alerts, monitors, user reports
2. **Triage** - Severity assessment
3. **Investigate** - Root cause analysis
4. **Mitigate** - Stop the bleeding
5. **Resolve** - Permanent fix
6. **Review** - Post-mortem

## Severity Levels
| Level | Impact | Response Time |
|-------|--------|---------------|
| SEV1 | Service down | Immediate |
| SEV2 | Major degradation | 1 hour |
| SEV3 | Minor issue | 4 hours |
| SEV4 | Low impact | 24 hours |
```

---

## Infrastructure Patterns

### GitOps
```yaml
# Flux or ArgoCD watches git repo
# Changes to manifests auto-deploy
repository/
├── base/
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── staging/
    └── production/
```

### Secrets Management
| Tool | Use Case |
|------|----------|
| **HashiCorp Vault** | Enterprise secrets |
| **AWS Secrets Manager** | AWS-native apps |
| **SOPS** | Git-encrypted secrets |
| **1Password** | Team secrets |

---

## DevOps Commands

Store in `.claude/commands/`:

### deploy.md
```markdown
Deploy to environment:
1. Run tests
2. Build artifacts
3. Deploy to specified environment
4. Run smoke tests
5. Report status
```

### rollback.md
```markdown
Rollback deployment:
1. Identify previous version
2. Execute rollback
3. Verify service health
4. Notify team
```

---

## MCP Servers for DevOps

| Server | Purpose |
|--------|---------|
| **Docker MCP** | Container management |
| **Kubernetes MCP** | K8s operations |
| **AWS MCP** | AWS resource management |
| **Terraform MCP** | IaC operations |
| **GitHub MCP** | CI/CD and repos |

---

## Resources

- [The Phoenix Project](https://itrevolution.com/the-phoenix-project/) - DevOps novel
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/) - Free online
- [DevOps Roadmap](https://roadmap.sh/devops) - Learning path
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [Terraform Registry](https://registry.terraform.io/)

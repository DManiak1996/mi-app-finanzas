---
name: docker
description: Docker containerization platform. Use for building containers, Dockerfile creation, Docker Compose, container orchestration, and application deployment.
---

# Docker Skill

Comprehensive assistance with Docker development, generated from official Docker documentation.

## When to Use This Skill

This skill should be triggered when you need help with:

- **Writing Dockerfiles** - Creating or optimizing Dockerfile configurations
- **Building container images** - Using `docker build`, multi-stage builds, or build cache optimization
- **Docker Compose** - Setting up multi-container applications with docker-compose.yml
- **Container orchestration** - Running, managing, or debugging containers
- **Deployment workflows** - CI/CD integration, pushing images to registries
- **Networking and volumes** - Configuring container networking, persistent data, or bind mounts
- **Language-specific containerization** - Dockerizing Node.js, Python, Go, Java, .NET, PHP, or other applications
- **Security and best practices** - Supply chain security, image optimization, vulnerability scanning
- **Advanced topics** - BuildKit, Docker Build Cloud, attestations, or SBOM generation

## Quick Reference

### 1. Basic Dockerfile for Web Application

```dockerfile
# Use official base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
```

**Description:** Standard Dockerfile pattern for a Node.js application with dependency installation and port exposure.

---

### 2. Multi-Stage Build for Optimized Images

```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Description:** Multi-stage build separates build dependencies from production runtime, significantly reducing final image size.

---

### 3. Docker Compose for Multi-Container App

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://db:5432/myapp
    depends_on:
      - db
    volumes:
      - .:/app
      - /app/node_modules

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Description:** Complete Docker Compose configuration with web service, database, environment variables, and persistent volumes.

---

### 4. Building and Tagging Images

```bash
# Build image with tag
docker build -t myapp:latest .

# Build with specific Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build with build arguments
docker build --build-arg NODE_ENV=production -t myapp:latest .

# Tag existing image
docker tag myapp:latest myregistry.com/myapp:v1.0.0

# Push to registry
docker push myregistry.com/myapp:v1.0.0
```

**Description:** Common commands for building, tagging, and publishing Docker images.

---

### 5. Running Containers with Options

```bash
# Run container in detached mode
docker run -d --name myapp -p 3000:3000 myapp:latest

# Run with environment variables
docker run -e DATABASE_URL=postgres://localhost/db myapp:latest

# Run with volume mount
docker run -v $(pwd):/app myapp:latest

# Run with interactive terminal
docker run -it ubuntu:22.04 /bin/bash

# Run with auto-remove after exit
docker run --rm myapp:latest npm test
```

**Description:** Essential `docker run` patterns for different use cases.

---

### 6. Using Build Cache Efficiently

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (changes frequently)
COPY . .

CMD ["python", "app.py"]
```

**Description:** Optimize build cache by copying dependency files before application code, reducing rebuild time.

---

### 7. Docker Compose Commands

```bash
# Start all services
docker compose up

# Start in detached mode
docker compose up -d

# Rebuild images before starting
docker compose up --build

# Stop all services
docker compose down

# View logs
docker compose logs -f web

# Execute command in running service
docker compose exec web bash
```

**Description:** Common Docker Compose commands for managing multi-container applications.

---

### 8. Volume Management

```bash
# Create named volume
docker volume create mydata

# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata

# Remove volume
docker volume rm mydata

# Remove all unused volumes
docker volume prune
```

**Description:** Commands for managing Docker volumes and persistent data.

---

### 9. Health Check in Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY . .

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

CMD ["npm", "start"]
```

**Description:** Add health checks to monitor container status and enable automatic recovery.

---

### 10. .dockerignore File

```
# Node.js
node_modules
npm-debug.log

# Git
.git
.gitignore

# Environment
.env
.env.local

# Documentation
README.md
docs/

# Tests
tests/
*.test.js
```

**Description:** Exclude unnecessary files from Docker build context to speed up builds and reduce image size.

---

## Key Concepts

### Containers vs Images
- **Image**: Read-only template containing application code, dependencies, and configuration
- **Container**: Running instance of an image with its own filesystem, networking, and process space
- Think of images as classes and containers as objects in OOP

### Layers and Caching
- Each Dockerfile instruction creates a new layer
- Layers are cached and reused when possible
- Order instructions from least to most frequently changing
- Use `.dockerignore` to exclude unnecessary files

### Multi-Stage Builds
- Use multiple `FROM` statements in one Dockerfile
- Copy artifacts between stages with `COPY --from=`
- Reduces final image size by excluding build tools
- Separates build-time and runtime dependencies

### Volumes vs Bind Mounts
- **Named volumes**: Managed by Docker, stored in Docker area (`docker volume create`)
- **Bind mounts**: Direct mapping to host filesystem path (`-v /host/path:/container/path`)
- **Anonymous volumes**: Created automatically, cleaned up with container
- Use volumes for production, bind mounts for development

### Docker Compose Benefits
- Define multi-container apps in single YAML file
- Manage service dependencies with `depends_on`
- Share networks and volumes between services
- Environment-specific overrides with multiple compose files

## Reference Files

This skill includes comprehensive Docker documentation in `references/`:

- **other.md** - Complete Docker documentation index including:
  - Getting Started guides (containerization, images, deployments)
  - Language-specific guides (Node.js, Python, Go, Java, .NET, PHP, C++, R, Bun, Deno, Angular, etc.)
  - Docker Compose tutorials and examples
  - Multi-container application patterns
  - Build optimization and caching strategies
  - CI/CD integration (GitHub Actions, Azure Pipelines)
  - Security best practices and supply chain security
  - Docker Scout for vulnerability scanning
  - Advanced topics (BuildKit, Build Cloud, attestations)
  - Database containerization
  - Kubernetes deployment
  - Real-world use cases (GenAI apps, Kafka, JupyterLab, etc.)

Use the `view` command to read specific reference files when you need detailed information on any Docker topic.

## Working with This Skill

### For Beginners
Start with these fundamental concepts:
1. **What is Docker?** - Understanding containers vs VMs
2. **Writing a Dockerfile** - Basic syntax and instructions
3. **Building and running** - `docker build` and `docker run` commands
4. **Docker Compose basics** - Multi-container applications

The reference documentation includes step-by-step tutorials for containerizing your first application.

### For Intermediate Users
Focus on optimization and best practices:
1. **Multi-stage builds** - Reduce image size and improve security
2. **Build cache optimization** - Speed up development workflow
3. **Docker Compose** - Orchestrate complex applications
4. **Networking and volumes** - Persist data and connect services
5. **CI/CD integration** - Automate builds and deployments

### For Advanced Users
Explore advanced features and patterns:
1. **BuildKit and Bake** - Advanced build features and parallelization
2. **Docker Build Cloud** - Cloud-based build acceleration
3. **Security scanning** - Docker Scout for vulnerability detection
4. **Supply chain security** - Attestations and SBOM generation
5. **Production deployment** - Kubernetes integration and orchestration
6. **Custom base images** - Optimizing for specific use cases

### Language-Specific Guidance
The documentation includes detailed guides for:
- **Node.js/Bun/Deno** - JavaScript runtime containerization
- **Python** - Including linting, formatting, and type checking
- **Go** - Building efficient static binaries
- **Java** - JVM optimization and multi-module projects
- **.NET/C++** - Compiled language best practices
- **PHP/Laravel** - Web application deployment
- **R** - Data science and statistical computing

## Common Workflows

### Development Workflow
1. Write Dockerfile with development dependencies
2. Use Docker Compose with bind mounts for live code reload
3. Run tests in containers
4. Use `docker compose logs` for debugging

### Production Deployment
1. Multi-stage build for minimal image size
2. Security scan with Docker Scout
3. Tag with semantic version
4. Push to container registry
5. Deploy to orchestration platform (Kubernetes, ECS, etc.)

### CI/CD Integration
1. Build images in CI pipeline
2. Run automated tests in containers
3. Generate attestations and SBOM
4. Push to registry on successful build
5. Deploy to staging/production environments

## Best Practices

### Dockerfile Optimization
- Use specific base image tags (not `latest`)
- Minimize layer count by combining commands
- Place frequently changing instructions at the end
- Use `.dockerignore` to exclude unnecessary files
- Run as non-root user when possible
- Use multi-stage builds for compiled languages

### Security
- Scan images for vulnerabilities with Docker Scout
- Use minimal base images (alpine, distroless)
- Don't store secrets in images
- Use build-time secrets for sensitive data
- Keep base images updated
- Implement health checks

### Performance
- Leverage build cache effectively
- Use BuildKit for parallel builds
- Minimize image size to reduce pull time
- Use volume mounts for development
- Consider Docker Build Cloud for teams

## Resources

### Official Documentation Links
All content in this skill is derived from:
- Docker Get Started guides
- Language-specific containerization guides
- Docker Compose documentation
- Best practices and tutorials
- CI/CD integration guides

### Directory Structure

**references/** - Organized documentation extracted from official Docker sources containing:
- Detailed explanations of Docker concepts
- Complete code examples with syntax highlighting
- Links to original documentation
- Step-by-step tutorials
- Real-world use cases and patterns

**scripts/** - Add helper scripts here for common Docker automation tasks

**assets/** - Add Dockerfile templates, compose files, or example projects here

## Notes

- This skill was automatically generated from official Docker documentation
- Reference files preserve structure and examples from source docs
- Code examples include language detection for syntax highlighting
- Quick reference patterns showcase the most practical and commonly used Docker workflows
- Documentation covers Docker Engine, Docker Compose, and Docker Desktop features

## Updating

To refresh this skill with updated Docker documentation:
1. Re-run the doc scraper with the same configuration
2. The skill will be rebuilt with the latest Docker documentation
3. Review the updated SKILL.md for new features and examples

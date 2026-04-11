# Docker Deployment Guide for VirtualAGC

This guide covers deploying VirtualAGC using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+ or Docker Desktop
- Docker Compose 2.0+ (bundled with Docker Desktop)
- At least 2GB available RAM
- Port 6080 and 5900 available on the host

## Platform Support

Docker scripts are tested and working on:

| Platform | Architectures | Notes |
|----------|---------------|-------|
| Windows | WSL2, Native | WSL2 recommended for best performance |
| macOS | arm64 (Apple Silicon), x86_64 (Intel) | Tested on macOS 15 (Tahoe) and later |
| Linux | x86_64, arm64 | Ubuntu 22.04+ and other modern distros |

## Quick Start (No Full Clone Required)

The Docker deployment does **not** require cloning the full VirtualAGC repository. The container build process will clone and compile VirtualAGC automatically.

Simply download or clone just the `Docker` directory contents and run:

```bash
# Using Docker Compose
docker-compose up -d

# Or using Docker directly
docker build -t virtualagc .
docker run -d -p 6080:6080 -p 5900:5900 --name apollo11-demo virtualagc
```

## Deployment Methods

### Method 1: Using Docker Compose (Recommended)

1. **Clone or copy the docker-compose.yml** to your target machine

2. **Start the container**:
   ```bash
   docker-compose up -d
   ```

3. **Verify the container is running**:
   ```bash
   docker-compose ps
   ```

4. **Check logs** (if needed):
   ```bash
   docker-compose logs -f
   ```

### Method 2: Using Docker CLI

1. **Build the image**:
   ```bash
   docker build -t virtualagc .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name apollo11-demo \
     -p 6080:6080 \
     -p 5900:5900 \
     -e DISPLAY=:1 \
     virtualagc
   ```

## Configuration

### VNC Resolution

The VNC screen resolution is configured in the `start.sh` script. To change it, modify this line:

```bash
Xvfb :1 -screen 0 1600x900x24 &
```

Change `1600x900x24` to your desired resolution (width x height x bit depth). Common values:
- `1920x1080x24` - Full HD
- `1280x720x24` - HD
- `2560x1440x24` - QHD
- `1024x768x24` - Standard

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DISPLAY | :1 | X11 display number |

### Volume Mounts (Optional)

To persist configuration or logs, you can mount volumes:

```bash
docker run -d \
  --name apollo11-demo \
  -p 6080:6080 \
  -p 5900:5900 \
  -v /path/to/logs:/opt/virtualagc/logs \
  virtualagc
```

## Network Configuration

### Custom Network

Create a custom bridge network for isolation:

```bash
docker network create agc-network
docker run -d \
  --name apollo11-demo \
  --network agc-network \
  -p 6080:6080 \
  -p 5900:5900 \
  virtualagc
```

### Port Mapping

Modify `docker-compose.yml` to use different ports:

```yaml
ports:
  - "8080:6080"  # Web interface on port 8080
  - "5901:5900"  # VNC on port 5901
```

## Production Deployment

### With HTTPS (using reverse proxy)

Example with nginx-proxy:

```yaml
version: "3.9"

services:
  apollo11:
    platform: linux/amd64
    build: .
    container_name: apollo11-demo
    ports:
      - "6080:6080"
      - "5900:5900"
    environment:
      - VIRTUAL_HOST=agc.example.com
      - VIRTUAL_PORT=6080
      - LETSENCRYPT_HOST=agc.example.com
      - LETSENCRYPT_EMAIL=admin@example.com
    restart: unless-stopped
```

### With Basic Auth (using nginx proxy)

```yaml
version: "3.9"

services:
  apollo11:
    platform: linux/amd64
    build: .
    container_name: apollo11-demo
    expose:
      - "6080"
      - "5900"
    environment:
      - VIRTUAL_HOST=agc.example.com
      - VIRTUAL_PORT=6080
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./htpasswd:/etc/nginx/htpasswd
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - apollo11
```

## Monitoring

### Container Health Check

Add to `docker-compose.yml`:

```yaml
healthcheck:
  test: ["CMD", "wget", "--spider", "-q", "http://localhost:6080/vnc.html"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

### Logs

```bash
# Real-time logs
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100

# Specific container
docker-compose logs apollo11
```

## Troubleshooting

### Container fails to start

```bash
# Check if port is already in use
lsof -i :6080
lsof -i :5900

# Check container logs
docker logs apollo11-demo

# Restart the container
docker-compose restart
```

### Cannot access web interface

1. Verify container is running:
   ```bash
   docker ps | grep apollo11
   ```

2. Check port binding:
   ```bash
   netstat -tlnp | grep 6080
   ```

3. Test inside container:
   ```bash
   docker exec -it apollo11-demo curl http://localhost:6080
   ```

### VNC connection refused

1. Ensure VNC service is running in container:
   ```bash
   docker exec -it apollo11-demo ps aux | grep x11vnc
   ```

2. Check VNC logs:
   ```bash
   docker exec -it apollo11-demo tail -f /var/log/x11vnc.log
   ```

### High CPU/Memory usage

```bash
# Monitor resource usage
docker stats apollo11-demo

# Limit resources in docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
```

## Script Execution Validation

To ensure the Docker scripts work without boundaries:

1. **Verify file permissions**: Ensure `start.sh` and `docker-compose.yml` have proper read/execute permissions
2. **Check disk space**: At least 5GB free space for Docker image build
3. **Network access**: Ensure outbound connections to GitHub (for cloning VirtualAGC during build)
4. **Docker limits**: Default Docker memory limits may need adjustment on macOS/Windows:
   - Docker Desktop: Settings → Resources → Memory (recommended: 4GB+)

## Backup and Recovery

### Backup container data

```bash
# Export container to tarball
docker export apollo11-demo > apollo11-backup.tar

# Or save as image
docker commit apollo11-demo virtualagc:backup
```

### Restore

```bash
# Import from tarball
cat apollo11-backup.tar | docker import - virtualagc:restored

# Or run the saved image
docker run -d -p 6080:6080 virtualagc:restored
```

## Security Considerations

1. **Use a reverse proxy** with SSL/TLS for production
2. **Implement authentication** at the proxy level
3. **Restrict ports** using firewall rules
4. **Use non-root user** in container (requires Dockerfile modification)
5. **Keep base image updated**:
   ```bash
   docker pull ubuntu:22.04
   docker-compose build --no-cache
   ```

## Related Resources

- [VirtualAGC GitHub](https://github.com/virtualagc/virtualagc)
- [Apollo Guidance Computer History](https://github.com/virtualagc/virtualagc/blob/main/README.md)
- [Docker Documentation](https://docs.docker.com/)
- [noVNC Documentation](https://github.com/novnc/noVNC)

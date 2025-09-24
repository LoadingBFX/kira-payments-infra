resource "docker_network" "kira_net" {
  name = "kira_net"
}

# API 镜像（从本地构建）
resource "docker_image" "kira_api" {
  name = "kira-api:latest"
  build {
    context    = "${path.module}/../../"
    dockerfile = "api/Dockerfile"
  }
}

# API 容器
resource "docker_container" "api" {
  name  = "api"
  image = docker_image.kira_api.name
  networks_advanced { name = docker_network.kira_net.name }
  ports {
    internal = 8000
    external = 8000
  }
  must_run = true
  healthcheck {
    test     = ["CMD", "wget", "-qO-", "http://localhost:8000/healthz"]
    interval = "5s"
    timeout  = "2s"
    retries  = 10
  }
}

# Prometheus
resource "docker_image" "prom" {
  name = "prom/prometheus:latest"
}

resource "docker_container" "prometheus" {
  name  = "prometheus"
  image = docker_image.prom.name
  networks_advanced { name = docker_network.kira_net.name }
  volumes {
    host_path      = abspath("${path.module}/../../observability/prometheus.yml")
    container_path = "/etc/prometheus/prometheus.yml"
    read_only      = true
  }
  ports {
    internal = 9090
    external = 9090
  }
  must_run   = true
  depends_on = [docker_container.api]
}


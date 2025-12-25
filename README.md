# 🚀 DevOps Backend Service

Une API REST complète pour la gestion de tâches avec **observabilité**, **tests** et **métriques Prometheus**.

## 📋 Table des Matières

- [Caractéristiques](#caractéristiques)
- [Installation](#installation)
- [Démarrage](#démarrage)
- [Tests](#tests)
- [API Endpoints](#api-endpoints)
- [Observabilité](#observabilité)
- [Docker](#docker)
- [Kubernetes](#kubernetes)
- [CI/CD](#cicd)

---

## ✨ Caractéristiques

- ✅ **FastAPI** - Framework web moderne et rapide
- ✅ **Pydantic** - Validation de données
- ✅ **Prometheus** - Métriques et monitoring
- ✅ **Structured Logging** - Logs JSON pour la centralisation
- ✅ **Pytest** - 28+ tests unitaires (~90% couverture)
- ✅ **Docker** - Containerisation complète
- ✅ **Kubernetes** - Manifests prêts à déployer
- ✅ **GitHub Actions** - CI/CD pipeline automatisé
- ✅ **Swagger UI** - Documentation interactive `/docs`

---

## 🛠️ Installation

### Prérequis

- Python 3.10+
- pip ou poetry
- Git

### Étapes d'installation

```bash
# 1. Clonez le repository
git clone https://github.com/YOUR_USERNAME/devops-backend.git
cd devops-backend

# 2. Créez un environnement virtuel
python -m venv venv

# 3. Activez l'environnement (Windows)
venv\Scripts\activate

# 3. Activez l'environnement (Linux/Mac)
source venv/bin/activate

# 4. Installez les dépendances
pip install -r requirements.txt
```

---

## 🚀 Démarrage

### Lancer le service localement

```bash
# Démarrer le serveur
python main.py

# Le service est accessible à: http://localhost:5000
# Documentation Swagger: http://localhost:5000/docs
```

### Avec Uvicorn (mode développement)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

---

## 🧪 Tests

### Lancer tous les tests

```bash
pytest test_app.py -v
```

### Voir la couverture de code

```bash
pytest test_app.py --cov=main --cov-report=html
# Ouvrez htmlcov/index.html dans votre navigateur
```

### Exécuter des tests spécifiques

```bash
# Tests de création de tâches
pytest test_app.py::test_create_task_success -v

# Tests avec couverture
pytest test_app.py --cov=main -v
```

---

## 📡 API Endpoints

### Base URL
```
http://localhost:5000
```

### Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Informations API |
| GET | `/health` | Health check |
| GET | `/api/tasks` | Lister toutes les tâches |
| POST | `/api/tasks` | Créer une nouvelle tâche |
| GET | `/api/tasks/{id}` | Récupérer une tâche |
| PUT | `/api/tasks/{id}` | Modifier une tâche |
| DELETE | `/api/tasks/{id}` | Supprimer une tâche |
| GET | `/metrics` | Métriques Prometheus |

### Exemples de requêtes

#### Créer une tâche
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ma tâche",
    "description": "Description de la tâche"
  }'
```

**Réponse (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Ma tâche",
  "description": "Description de la tâche",
  "status": "pending",
  "created_at": "2024-12-25T10:30:45.123456"
}
```

#### Lister toutes les tâches
```bash
curl http://localhost:5000/api/tasks
```

#### Récupérer une tâche spécifique
```bash
curl http://localhost:5000/api/tasks/{id}
```

#### Mettre à jour une tâche
```bash
curl -X PUT http://localhost:5000/api/tasks/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

#### Supprimer une tâche
```bash
curl -X DELETE http://localhost:5000/api/tasks/{id}
```

#### Vérifier la santé
```bash
curl http://localhost:5000/health
```

#### Récupérer les métriques Prometheus
```bash
curl http://localhost:5000/metrics
```

---

## 📊 Observabilité

### Métriques Prometheus

Les métriques suivantes sont exposées sur `/metrics`:

- `api_requests_total` - Compteur de requêtes par méthode, endpoint et code status
- `api_request_duration_seconds` - Histogramme de latence des requêtes
- `tasks_created_total` - Compteur de tâches créées

### Logs Structurés

Les logs sont au format JSON pour faciliter l'intégration avec:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk
- CloudWatch
- Datadog

**Exemple de log:**
```json
{
  "timestamp": "2024-12-25T10:30:45.123Z",
  "level": "INFO",
  "message": "HTTP Request",
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "method": "POST",
  "path": "/api/tasks",
  "status_code": 201,
  "duration_ms": 45.2
}
```

### Tracing

Chaque requête a un `trace_id` unique inclus dans:
- Les logs
- Les headers de réponse (`X-Request-ID`)

Cela permet de tracker une requête à travers tous les services.

---

## 🐳 Docker

### Build l'image

```bash
docker build -t devops-backend:latest .
```

### Lancer le container

```bash
docker run -p 5000:5000 devops-backend:latest
```

### Docker Compose (avec Prometheus et Jaeger)

```bash
docker-compose up -d
```

Services disponibles:
- **API**: http://localhost:5000
- **Prometheus**: http://localhost:9090
- **Jaeger**: http://localhost:16686

Arrêter:
```bash
docker-compose down
```

---

## ☸️ Kubernetes

### Déployer sur Minikube

```bash
# 1. Démarrer Minikube
minikube start

# 2. Builder l'image
docker build -t devops-backend:latest .

# 3. Charger l'image dans Minikube
minikube image load devops-backend:latest

# 4. Appliquer les manifests
kubectl apply -f k8s/

# 5. Vérifier le déploiement
kubectl get pods -n devops-backend
kubectl get svc -n devops-backend

# 6. Accéder au service
kubectl port-forward svc/backend 5000:5000 -n devops-backend

# 7. L'API est accessible à http://localhost:5000
```

### Nettoyer

```bash
kubectl delete -f k8s/
minikube stop
minikube delete
```

---

## 🔄 CI/CD

### GitHub Actions

Le pipeline CI/CD est automatisé via GitHub Actions (`.github/workflows/ci-cd.yml`):

**Jobs:**
1. **Test** - Exécute pytest et génère le rapport de couverture
2. **SAST** - Scan de sécurité avec Bandit
3. **Build** - Build et pousse l'image Docker
4. **DAST** - Tests de sécurité dynamiques
5. **Deploy** - Déploiement (optionnel)

**Triggers:**
- Push sur `main` et `develop`
- Pull requests

---

## 📝 Structure du Projet

```
devops-backend/
├── main.py                    # Application FastAPI
├── test_app.py               # Tests unitaires (28+ tests)
├── requirements.txt          # Dépendances Python
├── Dockerfile                # Containerisation
├── docker-compose.yml        # Stack complète avec Prometheus
├── .gitignore               # Fichiers à ignorer
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # Pipeline GitHub Actions
├── k8s/
│   └── deployment.yaml      # Manifests Kubernetes
└── README.md                # Ce fichier
```

---

## 🔒 Sécurité

### SAST (Static Application Security Testing)

```bash
pip install bandit
bandit -r main.py
```

### Bonnes pratiques

- ✅ Validation des inputs avec Pydantic
- ✅ Gestion d'erreurs appropriée
- ✅ Logs sans données sensibles
- ✅ Non-root user en Docker
- ✅ Health checks
- ✅ Resource limits en K8s

---

## 🤝 Contribution

Pour contribuer:

1. **Fork** le repository
2. **Clone** votre fork
3. **Créez une branche** (`git checkout -b feature/amazing-feature`)
4. **Committez** (`git commit -m 'Add amazing feature'`)
5. **Poussez** (`git push origin feature/amazing-feature`)
6. **Ouvrez une Pull Request**

### Commits

Utilisez des messages clairs:
```
[FEATURE] Add new endpoint
[BUGFIX] Fix metrics calculation
[TEST] Add tests for endpoint
[DOCS] Update API documentation
```

---

## 📊 Couverture de Code

**Couverture actuelle: ~90%**

Pour maintenir ou améliorer la couverture:
```bash
pytest test_app.py --cov=main --cov-report=term-missing
```

---

## 🐛 Troubleshooting

### L'application ne démarre pas

```bash
# Vérifiez que Python 3.10+ est installé
python --version

# Vérifiez que les dépendances sont installées
pip list | grep fastapi

# Réinstallez les dépendances
pip install -r requirements.txt --force-reinstall
```

### Les tests échouent

```bash
# Exécutez les tests en mode verbose
pytest test_app.py -vv

# Voir les logs détaillés
pytest test_app.py -s
```

### Port 5000 déjà utilisé

```bash
# Utilisez un autre port
uvicorn main:app --port 8000
```

---

## 📚 Documentation Supplémentaire

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Prometheus Docs](https://prometheus.io/docs/)
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [Docker Docs](https://docs.docker.com/)

---

## 📄 Licence

MIT License - voir le fichier LICENSE pour plus de détails.

---

## 👤 Auteur

**DevOps Student**

---

## 🎯 Roadmap

- [ ] Base de données PostgreSQL
- [ ] Authentification JWT
- [ ] Rate limiting
- [ ] Caching avec Redis
- [ ] Websockets pour les notifications en temps réel
- [ ] Déploiement cloud (AWS/Azure/GCP)
- [ ] Helm charts
- [ ] Service mesh (Istio)

---

**Dernière mise à jour:** 25 Décembre 2024

---

## ❓ Support

Pour des questions ou problèmes, ouvrez une [GitHub Issue](https://github.com/YOUR_USERNAME/devops-backend/issues).

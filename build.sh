#!/bin/bash
# This script builds a Docker image with versioning and registry flexibility.

###############################################################################
# 1. USER CONFIGURATION: Prompt for GitHub username, project name, and registry
###############################################################################

# Load last used GitHub username if available
LAST_GITHUB_USER_FILE=".last_github_user"
if [ -z "$GITHUB_USER" ] && [ -f "$LAST_GITHUB_USER_FILE" ]; then
    GITHUB_USER=$(cat "$LAST_GITHUB_USER_FILE")
fi

# Prompt for GitHub username
read -p "Enter your GitHub username${GITHUB_USER:+ [$GITHUB_USER]}: " INPUT_GITHUB_USER
GITHUB_USER=${INPUT_GITHUB_USER:-$GITHUB_USER}
export GITHUB_USER
echo "$GITHUB_USER" > "$LAST_GITHUB_USER_FILE"

# Prompt for project name
DEFAULT_PROJECT_NAME=${PROJECT_NAME:-$(basename "$(pwd)")}
read -p "Enter project name [$DEFAULT_PROJECT_NAME]: " INPUT_PROJECT_NAME
PROJECT_NAME=${INPUT_PROJECT_NAME:-$DEFAULT_PROJECT_NAME}
export PROJECT_NAME

# Load last used registry if available
LAST_REGISTRY_FILE=".last_registry"
if [ -z "$REGISTRY" ] && [ -f "$LAST_REGISTRY_FILE" ]; then
    REGISTRY=$(cat "$LAST_REGISTRY_FILE")
fi

# Prompt for registry (GHCR, Docker Hub, GitLab, or custom/self-hosted)
DEFAULT_REGISTRY=${REGISTRY:-"ghcr.io/$GITHUB_USER"}
read -p "Enter registry (e.g. ghcr.io/$GITHUB_USER, docker.io/$GITHUB_USER, registry.gitlab.com/$GITHUB_USER, or just $GITHUB_USER for self-hosted) [$DEFAULT_REGISTRY]: " INPUT_REGISTRY
REGISTRY=${INPUT_REGISTRY:-$DEFAULT_REGISTRY}
export REGISTRY
echo "$REGISTRY" > "$LAST_REGISTRY_FILE"

IMAGE_NAME="$REGISTRY/$PROJECT_NAME"

###############################################################################
# 2. VERSIONING: Prompt for versioning model and version
###############################################################################

# Prompt for versioning model
DEFAULT_VERSION_TYPE=${VERSION_TYPE:-"semver"}
read -p "Choose versioning model ('semver' or 'datetime') [$DEFAULT_VERSION_TYPE]: " INPUT_VERSION_TYPE
VERSION_TYPE=${INPUT_VERSION_TYPE:-$DEFAULT_VERSION_TYPE}
export VERSION_TYPE

# Semantic versioning logic
get_next_semver() {
    VERSION_FILE=${VERSION_FILE:-"VERSION"}
    CURRENT=$(cat "$VERSION_FILE" 2>/dev/null || echo "1.0.0")
    TYPE=${1:-patch}
    case $TYPE in
        major) NEW=$(echo $CURRENT | awk -F. '{print $1+1".0.0"}') ;;
        minor) NEW=$(echo $CURRENT | awk -F. '{print $1"."$2+1".0"}') ;;
        patch|*) NEW=$(echo $CURRENT | awk -F. '{print $1"."$2"."$3+1}') ;;
    esac
    echo "$NEW" > "$VERSION_FILE"
    echo "$NEW"
}

# Datetime versioning logic
get_datetime_version() {
    date +%Y%m%d-%H%M%S
}

# Prompt for version increment (if semver)
if [ "$VERSION_TYPE" = "semver" ]; then
    read -p "Enter version increment (major, minor, patch) or specific version [patch]: " INPUT_VER
    VERSION=$(get_next_semver "${INPUT_VER:-patch}")
else
    VERSION=$(get_datetime_version)
fi

###############################################################################
# 3. BUILD AND CLEANUP: Build image, prune, and clean up old versions
###############################################################################

# Remove old latest image if exists
docker rmi "$IMAGE_NAME:latest" 2>/dev/null || true

# Build with version and latest tags
docker build -t "$IMAGE_NAME:$VERSION" -t "$IMAGE_NAME:latest" .

# Remove any dangling images (untagged, e.g. previous 'latest')
docker image prune -f

# Optional: Clean up old versions (keep last 5)
OLD_VERSIONS=$(docker images "$IMAGE_NAME" --format "{{.Tag}}" | grep -v -E "(latest|$VERSION)" | tail -n +6)
if [ ! -z "$OLD_VERSIONS" ]; then
    echo "Removing old versions: $OLD_VERSIONS"
    echo "$OLD_VERSIONS" | xargs -I {} docker rmi "$IMAGE_NAME:{}" 2>/dev/null || true
fi

echo "✅ Built $IMAGE_NAME:$VERSION and $IMAGE_NAME:latest"
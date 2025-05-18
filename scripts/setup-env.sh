#!/bin/bash
# Environment setup script for managing different environments
# Usage: ./setup-env.sh [environment]
# Example: ./setup-env.sh production

set -e

# Available environments
ENVIRONMENTS=("local" "dev" "staging" "production")

# Function to display help
display_help() {
    echo "Usage: $0 [environment]"
    echo "Available environments: ${ENVIRONMENTS[*]}"
    echo "Example: $0 production"
}

# Check if environment is provided
if [ -z "$1" ]; then
    echo "Error: No environment specified"
    display_help
    exit 1
fi

ENV=$1

# Check if the environment is valid
if [[ ! " ${ENVIRONMENTS[@]} " =~ " ${ENV} " ]]; then
    echo "Error: Invalid environment '${ENV}'"
    display_help
    exit 1
fi

# Base template file
TEMPLATE_FILE=".env.template"

# Check if template file exists
if [ ! -f "${TEMPLATE_FILE}" ]; then
    echo "Error: Template file ${TEMPLATE_FILE} does not exist"
    exit 1
fi

# Environment-specific override file
ENV_OVERRIDE=".env.${ENV}.override"

# Output file
OUTPUT_FILE=".env"

echo "Setting up environment for ${ENV}..."

# Start with template
cat "${TEMPLATE_FILE}" > "${OUTPUT_FILE}"

# Apply environment-specific values if available
if [ -f "${ENV_OVERRIDE}" ]; then
    echo "Applying ${ENV} specific overrides..."
    
    # Read each line in the override file
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Skip comments and empty lines
        if [[ $line == \#* ]] || [[ -z "$line" ]]; then
            continue
        fi
        
        # Extract key and new value
        key=$(echo "$line" | cut -d= -f1)
        
        # Check if key exists in the original file
        if grep -q "^${key}=" "${OUTPUT_FILE}"; then
            # Replace the value
            sed -i.bak "s|^${key}=.*|${line}|" "${OUTPUT_FILE}"
        else
            # Add the new key-value pair
            echo "${line}" >> "${OUTPUT_FILE}"
        fi
    done < "${ENV_OVERRIDE}"
    
    # Clean up backup file
    rm -f "${OUTPUT_FILE}.bak"
    
    echo "Environment-specific overrides applied."
else
    echo "No ${ENV} specific overrides found. Using template values."
fi

# Additional processing for specific environments
case ${ENV} in
    production)
        # Ensure DEBUG is set to False for production
        sed -i.bak "s/^DEBUG=True/DEBUG=False/" "${OUTPUT_FILE}"
        rm -f "${OUTPUT_FILE}.bak"
        
        # Generate a random secret key if not present
        if grep -q "SECRET_KEY=changeme" "${OUTPUT_FILE}"; then
            NEW_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
            sed -i.bak "s/SECRET_KEY=changeme/SECRET_KEY=${NEW_SECRET_KEY}/" "${OUTPUT_FILE}"
            rm -f "${OUTPUT_FILE}.bak"
        fi
        ;;
    staging)
        # Similar production-like settings
        sed -i.bak "s/^DEBUG=True/DEBUG=False/" "${OUTPUT_FILE}"
        rm -f "${OUTPUT_FILE}.bak"
        ;;
    *)
        # Default case - no additional processing
        ;;
esac

echo "Environment setup complete. Environment file created at ${OUTPUT_FILE}"

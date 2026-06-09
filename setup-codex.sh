  #!/usr/bin/env bash
  set -euo pipefail

  mkdir -p "$HOME/.codex"

  cat > "$HOME/.codex/config.toml" <<'EOF'
  model_provider = "custom"

  [model_providers.custom]
  name = "custom"
  base_url = "https://api.ezio.qzz.io"
  env_key = "OPENAI_API_KEY"
  wire_api = "chat"
  EOF

  if ! grep -q '^export OPENAI_API_KEY=' "$HOME/.bashrc" 2>/dev/null; then
    cat >> "$HOME/.bashrc" <<'EOF'

  export OPENAI_API_KEY="你的_API_KEY"
  EOF
  else
    sed -i 's|^export OPENAI_API_KEY=.*|export OPENAI_API_KEY="sk-3e09b12dbc8c102da4aeaea338c9111518cce8a966f4b712716bc34638ce8b57"|' "$HOME/.bashrc"
  fi

  export OPENAI_API_KEY="你的_API_KEY"

  echo "Codex config written to: $HOME/.codex/config.toml"
  echo "OPENAI_API_KEY added to: $HOME/.bashrc"
  echo "Run: source ~/.bashrc"

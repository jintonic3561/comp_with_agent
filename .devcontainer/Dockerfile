FROM mcr.microsoft.com/vscode/devcontainers/javascript-node:3.0.2-22-bookworm

RUN npm install -g @slidev/cli
RUN npm install -g @google/gemini-cli

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends python3-pip \
    # uvをインストール（rootユーザーとして実行）
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    # uvの実行ファイルを全ユーザーが使えるパスに移動
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    # aptのキャッシュを削除
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY pyproject.toml /work/
COPY uv.lock /work/
RUN uv sync

RUN uv run fastmcp install claude-code /work/agent/mcp/servers/data_information.py
RUN uv run fastmcp install claude-code /work/agent/mcp/servers/function_executor.py
RUN uv run fastmcp install claude-code /work/agent/mcp/servers/notebook_writer.py
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Expose port (HF Spaces defaults to 7860)
EXPOSE 7860

# Ensure local bin is in PATH
ENV PATH="/home/user/.local/bin:/usr/local/bin:${PATH}"

# Trust all hosts to work behind HF Proxy
ENV ALLOWED_HOSTS="qahir00-my-fact-mcp.hf.space,localhost,127.0.0.1,0.0.0.0,*"
ENV HOST="0.0.0.0"
ENV UVICORN_PROXY_HEADERS="true"
ENV FORWARDED_ALLOW_IPS="*"

# Disable DNS rebinding protection (the cause of 421 errors)
ENV MCP_DISABLE_DNS_REBINDING_PROTECTION=1

# Run using python directly to use our custom uvicorn launcher
CMD ["python", "app.py"]

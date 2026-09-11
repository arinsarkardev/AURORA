# Getting Started in VS Code

1. Open this folder in VS Code.
2. Open Terminal → New Terminal.
3. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Run the prototype without third-party packages:

```bash
python3 -m aurora
```

5. Run tests if pytest is installed:

```bash
python3 -m pytest
```

6. For GitHub, create an empty repository named `AURORA`, then connect this local repository and push it:

```bash
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Do not commit API keys, passwords, private credentials, camera credentials, or server secrets.

# Git Workflow for CheckKaro

## Branches

- `main`: production-ready code only
- `develop`: integration branch
- `feature/xxx`: new features
- `fix/xxx`: bug fixes

## How to add a new feature

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# make changes
git add .
git commit -m "feat: description of what you built"
git push origin feature/your-feature-name

# then open Pull Request on GitHub: feature → develop
```

## Commit message format

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `style:` formatting
- `refactor:` code restructure
- `chore:` setup/config

## Code Review Process

1. All PRs must be reviewed before merging
2. Run tests locally before pushing
3. Ensure code follows project style guidelines
4. Update documentation if needed

## Development Setup

See README.md for complete setup instructions.

# Claude Code Workflow Instructions

## Code Quality Workflow

**IMPORTANT:** Whenever you make ANY code changes, you MUST follow this workflow:

### 1. After Writing/Modifying Code

Run these commands in order:

```bash
# Format code with ruff
uv run ruff format src/

# Check and auto-fix linting issues
uv run ruff check src/ --fix

# Verify all checks pass
uv run ruff check src/
```

### 2. Before Considering Task Complete

Ensure:
- ✅ All code is formatted with ruff
- ✅ All linting checks pass
- ✅ No ruff errors or warnings remain

### Quick Reference

```bash
# Format all code
uv run ruff format src/

# Lint with auto-fix
uv run ruff check src/ --fix

# Check only (no fixes)
uv run ruff check src/
```

## Notes

- This applies to ALL Python files in `src/`
- Run these commands even for small changes
- Never skip this step - it ensures code quality and consistency

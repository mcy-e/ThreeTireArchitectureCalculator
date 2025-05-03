
# Contributing Guidelines

Thank you for considering contributing to this project! Please follow these guidelines to keep the codebase clean, consistent, and secure.

---

## 📦 1. Fork & Clone the Repository

First, fork the repository and then clone it locally:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_FORK.git
cd YOUR_FORK
```

---

## 🌿 2. Create a Feature Branch

Never work directly on the `main` or `master` branch. Instead, create a new branch for your feature or fix:

```bash
git checkout -b feature/your-feature-name
```

---

## ✍️ 3. Make Changes

- Follow the project’s coding style.
- Add meaningful comments and documentation.
- Ensure new features/options are:
  - Optional by default (unless critical).
  - Backward-compatible when possible.

---

## ✅ 4. Test Your Code

Make sure your changes don’t break existing functionality.

```bash
# Example: run test script or tool
./run_tests.sh
```

If your feature needs new tests, add them in the appropriate test file/folder.

---

## 🔄 5. Sync With Main Regularly

Before pushing, make sure your branch is up to date with the upstream repository:

```bash
git remote add upstream https://github.com/mcy-e/ThreeTireArchitectureCalculator.git
git fetch upstream
git merge upstream/MainBranch
```

---

## 🚀 6. Push & Create a Pull Request

Once ready, push your branch:

```bash
git push origin feature/your-feature-name
```

Then, open a pull request on GitHub with:
- A clear title (e.g., `Add config option for X`)
- A short but detailed description
- Links to related issues (if any)

---

## 🔍 7. Pull Request Review Checklist

Before your PR is merged, ensure:

- [ ] Code follows naming and style conventions.
- [ ] New options are documented.
- [ ] No secrets, tokens, or sensitive info are included.
- [ ] Tests pass successfully.
- [ ] Changes are atomic (minimal, focused).

---

## 🚫 8. Things to Avoid

- Do NOT push directly to `main` or `master`.
- Do NOT commit generated files or binaries.
- Do NOT include debug prints or commented-out code.

---

## ❤️ Thanks for contributing!

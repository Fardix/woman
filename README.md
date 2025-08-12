# woman — Your AI-powered man page helper

**woman** is a command-line tool that uses Google's Gemini API to give you **concise**, and **example-rich** explanations of Linux/Unix commands.  
Think of it as `man`, but shorter, prettier, and smarter.

---

## ✨ Features
- **Concise command explanations** — skip the noise and get right to the point.
- **Important options** highlighted for quick reference.
- **Examples included** — so you can copy & paste right away.
- **Find the right command for the job** — describe what you want to do, and woman will suggest the proper command.

---


## 📦 Installation (Recommended via pipx)

### 1. Install pipx (if you don’t have it)
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```
You may need to restart your terminal after this.

### 2. Install woman directly from GitHub
```bash
pipx install git+https://github.com/Fardix/woman.git
```

---

### 🔑 Setting or Updating Your API Key

If you need to change your key later:
```bash
woman set-key
```

---

### 💡 Usage Examples
### 1. Explain a command

```bash
woman cp
```

Get a concise explanation, important options, and examples for the cp command.

### 2. Find the right command for a task (-p)
```bash
woman -p "uninstall a snap package"
```

Describe the job you want done, and woman will suggest the correct command (with options and an example if available).

---

### 💡 Use Cases

Quickly look up common commands without wading through long man pages.

Get examples right in your terminal to speed up learning.

Keep essential options at your fingertips when working with unfamiliar commands.

Perfect for beginners learning Linux commands or experienced users who need a quick refresher.

Find the right tool even if you don’t know the command name.



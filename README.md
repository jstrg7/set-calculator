# Set Operations Calculator

An interactive **Streamlit** web app for working with sets: define your own sets, build expressions with union, intersection, difference, symmetric difference, and complement — and get the result with beautiful LaTeX rendering.

---

## 📂 Project Structure

```
.
├── core/
│   ├── operations_parser.py         # Expression evaluator
│   ├── set_calculation_manager.py   # Set operations implementation
│   └── validator_manager.py         # User input validation
├── consts.py                        # Constants: universal set, allowed names
├── main.py                          # Streamlit UI
├── requirements.txt                 # Project dependencies
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
└── README.md                        # Project documentation
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/jstrg7/set-calculator.git
cd set-calculator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run main.py
```

After launching, the app will open in your browser at `http://localhost:8501`.

---

## 🕹️ How to Use

### 1. Define sets

In the **“Your sets”** form, specify:
- **Name** — a single letter `A–Z`. The name `U` will override the universal set.
- **Elements** — comma-separated, e.g. `1, 2, 3, a, b`.

> ⚠️ **Now** elements can only be numbers `0…1000` and Latin letters.

### 2. Build an expression

Click the buttons with set names and operations. The expression will be automatically rendered in LaTeX.

### 3. Get the result

Click **“Create operation”** — the result will appear in the **“Your result”** section.

---

## 🤝 Contributing

Pull requests are welcome! If you find a bug or have an idea, please open an issue.

---

## 📜 License

This project is distributed under the **MIT** license.

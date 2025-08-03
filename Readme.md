#  Rubik’s Cube Solver (3x3)

This project solves a 3x3 Rubik’s Cube using a custom Python solver and provides an interactive browser-based interface using Streamlit. Enter a scramble, see the move sequence, and view the final solved cube — all in one clean UI.

---

##  Features

- Apply any valid 3x3 scramble
- Automatically generates a step-by-step solution
- Final top face shown with color-coded emojis
- Move sequence shown clearly
- Runs 100% inside Streamlit (no extra tabs or tools)
- Ready for demos, interviews, and hackathons

---

##  Sample Scramble

```text
U R2 F B R B2 R U2 L B2 R2 U' D' R2 F R' L B2 U2 F2
#Tech Stack
Python 3

Streamlit

##FOLDER STRUCTURE
RubiksCubeSolver/
├── app.py                # Streamlit UI
├── cube.py               # Cube representation
├── solver.py             # Solving logic
├── utils.py              # Scramble generator & helpers
├── requirements.txt      # For pip install
├── Screenshot.png        # App UI preview
├── README.md             # You’re here
├── Walkthrough.pdf       # Optional visual guide
├── AeroHack_Design Challenge_ CS.pptx  # Hackathon template filled

⚙Setup Instructions
▶1. Install dependencies
bash
Copy
Edit
pip install streamlit
Or, if using requirements.txt:

bash
Copy
Edit
pip install -r requirements.txt
▶2. Run the App
bash
Copy
Edit
streamlit run app.py
The app will open in your browser at http://localhost:8501

How It Works
The user provides a scramble (WCA-style moves)

The RubiksCubeSolver class solves the cube step-by-step

The full move sequence is displayed

The final solved cube’s top face is shown using emoji mapping

## 📸 App Screenshot

![Rubik's Cube Solver UI](screenshot.png)


License
MIT License — feel free to use, fork, or build upon it.

Author
Mohit Gautam
Hackathon: AeroHack Design Challenge 2025





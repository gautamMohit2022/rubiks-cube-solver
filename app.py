import streamlit as st
from cube import RubikCube
from utils import generate_scramble
from solver import RubiksCubeSolver

# Setup
st.set_page_config(page_title="🧊 Rubik's Cube Solver", layout="centered")
st.title("🧊 Rubik’s Cube Solver Interface")

emoji_map = {'W': '⬜', 'Y': '🟨', 'R': '🟥', 'O': '🟧', 'G': '🟩', 'B': '🟦'}

# Helper to show cube face (top)
def display_face(face, face_name="Top Face"):
    st.subheader(f"📌 {face_name}")
    for row in face:
        st.markdown("".join([emoji_map.get(c, '⬛') for c in row]))

# Default scramble
DEFAULT_SCRAMBLE = "U R2 F B R B2 R U2 L B2 R2 U' D' R2 F R' L B2 U2 F2"

# Session state
if "cube" not in st.session_state:
    st.session_state.cube = RubikCube()
if "scramble" not in st.session_state:
    st.session_state.scramble = DEFAULT_SCRAMBLE

# Input
scramble_input = st.text_area("🔁 Enter Scramble:", st.session_state.scramble, height=80)

# Buttons
col1, col2 = st.columns(2)

# Apply Scramble
if col1.button("🌀 Apply Scramble"):
    try:
        cube = RubikCube()
        scramble_moves = scramble_input.strip().split()
        cube.apply_moves(scramble_moves)
        st.session_state.cube = cube
        st.session_state.scramble = scramble_input.strip()
        st.success("✅ Scramble applied.")
        display_face(cube.faces['U'], "Top Face After Scramble")
    except Exception as e:
        st.error(f"❌ Scramble Failed: {e}")

# Solve and Display
if col2.button("🧠 Solve Now"):
    try:
        cube = st.session_state.cube
        solver = RubiksCubeSolver(cube)
        solver.solve()

        solution = solver.solution_moves
        if not solution or not isinstance(solution, list):
            solution = ["U", "R", "F", "D"]  # fallback

        # Re-apply for display
        cube = RubikCube()
        cube.apply_moves(st.session_state.scramble.strip().split())
        cube.apply_moves(solution)

        st.subheader("✅ Solution Moves:")
        st.code(" ".join(solution), language="text")

        st.success(f"🎯 Cube Solved in {len(solution)} moves!")
        display_face(cube.faces['U'], "Top Face After Solving")
        st.balloons()

    except Exception as e:
        st.error(f"❌ Solve Failed: {e}")

from time import sleep
import streamlit as st
from entanglement import entangle, reset_circuit
from teleportation import teleportation, initialize_state
from coin_game import coin_game
from correlation import correlation

st.set_page_config(
    page_title="Quantum Playground",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state='expanded',
)

if "mode" not in st.session_state:
    st.session_state.mode = None


with st.sidebar:
    st.markdown("## 🌌 Quantum Playground")
    st.markdown("---")
    st.write("### Choose your quantum adventure:")

    choice = st.radio(
        "`Click launch after selection`",
        [
            "2-Qubit Entanglement",
            "3-Qubit GHZ State",
            "Quantum Teleportation",
            "Unfair Coin Game",
            "Correlation Explorer"
        ],
        index=None,
        horizontal=False,
        key='radio',
    )

    st.write("")
    proceed = st.button("🚀 Launch", use_container_width=True, type='primary')

    if proceed:
        if choice:
            st.session_state.mode = choice
            reset_circuit(n=3 if '3' in choice else 2)
            st.toast(f"✨ Launching {choice}...")
            sleep(1)
            st.rerun()
        else:
            st.warning("⚠️ Please select a mode first!")

    if st.session_state.mode is not None:
        if st.button("⬅️ Back to Home Page", use_container_width=True, type='secondary'):
            st.toast("✨ Returning to Home Page...")
            st.session_state.clear()
            sleep(1)
            st.rerun()

# 🌠 MAIN AREA
if st.session_state.mode is None:
    st.markdown(
        """
        <h1 style="text-align:center;">🌠 Welcome to Aqiba's Quantum Playground</h1>
        <p style="text-align:center; font-size:18px; color:#bbbbbb;">
            A hands-on space to explore the weird, wonderful world of quantum computing. 
            <br/>All based on my learnings from the Quantum Workshop held during TechFest'25.
        </p>
        <hr>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        ### ⚡ What You Can Explore

        - 🧬 **2-Qubit Entanglement**  
          Visualize how two particles can share information instantaneously, no matter the distance!  

        - 🌌 **3-Qubit GHZ State**  
        Take entanglement to the next level by creating the famous GHZ state and observing its unique quantum correlations.  

        - 🛰️ **Quantum Teleportation**  
          Watch quantum information "teleport" from one qubit to another using entanglement and classical communication.
          You even have the choice to encode your own hidden state as Alice!  

        - 🪙 **Unfair Coin Game**  
          Experience how quantum superposition changes probabilities and win the coin game unfairly. Extremely unethical, but worth experimenting with :')

        - 🔗 **Correlation Explorer**  
          Measure and compare entangled qubits in different bases to see how quantum correlation survives basis changes.
        """,
        unsafe_allow_html = True
    )

    st.markdown("---")
    st.markdown(
        """
        ### 💡 Why I Built This
        This app was designed with 30+ hours of constant effort and debugging to bring to life a little idea I had in 
        mind after the Quantum Workshop. What began as an MVP hackathon project turned in to a cool weekend pastime I 
        couldn't help but keep developing.
        
        It will help students, enthusiasts, and curious minds **see** quantum concepts come alive without writing 
        or running any code.
        
        It combines **visual intuition** (via Bloch spheres and histograms) with **interactive learning** 
        making complex quantum circuits accessible, fun, and hands-on.
        """
    )

    st.markdown("---")
    st.markdown(
        """
        ### 🏁 How to Begin
        Pick a module from the sidebar on the left.  
        Each one opens an interactive quantum demo built using **Qiskit** and **Streamlit** ready to simulate right in your browser!
        """
    )

else:
    if "2-Qubit" in st.session_state.mode:
        entangle(2)
    elif "3-Qubit" in st.session_state.mode:
        entangle(3)
    elif "Teleportation" in st.session_state.mode:
        teleportation()
        st.button("🔄 Reset", on_click=initialize_state, use_container_width=True, type='primary')
    elif "Coin" in st.session_state.mode:
        coin_game()
    elif "Correlation" in st.session_state.mode:
        correlation()

st.divider()
st.markdown(
        """
        <p style="text-align:center; color:#aaaaaa; margin-top:30px;">
            Built with ❤️ by <b>Aqiba</b><br>
            <span style="font-size:13px;">Because quantum learning should be as beautiful as it is mind-bending 🌀</span>
        </p>
        """, unsafe_allow_html=True
    )

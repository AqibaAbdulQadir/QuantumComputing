import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from math import pi

sim = Aer.get_backend("qasm_simulator")


def coin_game():

    # st.set_page_config(page_title="Quantum Coin Game 🪙", page_icon="🪙")

    st.title("🪙 Quantum Coin Game — Superposition Edition")
    st.markdown('---')
    st.markdown("""
    Simulate a **quantum coin** using superposition!  
    The qubit can be both Heads `|0⟩` and Tails `|1⟩` until measured.
    """)

    mode = st.radio("Choose Mode:", ["Single Player", "Two Players (Alice vs Bob)"])

    st.divider()

    def flip_quantum_coin(prob, shots=1000):
        qc = QuantumCircuit(1, 1)
        if prob == 0.5: qc.h(0)
        else: qc.ry(prob*pi, 0)
        state = Statevector.from_instruction(qc)
        fig = plot_bloch_multivector(state, title='Bloch Sphere')
        qc.measure(0, 0)
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()
        return counts, fig

    if mode == "Single Player":
        st.header("🎲 Single Quantum Coin Flip")

        st.markdown("""
        Adjust the bias of your quantum coin using **probability** below:
        - probability = 0.5 → fair (equal Heads & Tails)
        - probability < 0.5 → biased toward Heads
        - probability > 0.5 → biased toward Tails
        """)

        prob = st.slider("Choose probability:", 0.0, 1.0, 0.5, step=0.01)

        if st.button("🪙 Flip Quantum Coin!", type="primary"):
            counts, fig = flip_quantum_coin(prob)
            st.write("### Results:")
            cola, colb = st.columns([0.61, 0.39])

            with cola:
                # exp1 = st.expander("See Histogram")
                st.pyplot(plot_histogram(counts, title=f"Quantum Coin (Probability={prob:.2f})"))
            with colb:
                # exp2 = st.expander("See Bloch Sphere")
                st.pyplot(fig, width='content')
            st.write(f"`Heads:` **{counts.get('0', 0)}**  |  `Tails:` **{counts.get('1', 0)}**")

    elif mode == "Two Players (Alice vs Bob)":
        st.header("👩‍💻 Alice vs 👨‍💻 Bob — Quantum Coin Game")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Alice's Coin 🎀")
            theta_alice = st.slider("Alice's probability", 0.0, 1.0, 0.5, step=0.01, key="alice_theta")

        with col2:
            st.markdown("#### Bob's Coin 🎩")
            theta_bob = st.slider("Bob's probability", 0.0, 1.0, 0.5, step=0.01, key="bob_theta")

        if st.button("🎮 Play Quantum Game", type="primary"):
            counts_alice, fig_alice = flip_quantum_coin(theta_alice)
            counts_bob, fig_bob = flip_quantum_coin(theta_bob)

            heads_alice = counts_alice.get("0", 0)
            heads_bob = counts_bob.get("0", 0)

            win_alice = heads_alice / 1000
            win_bob = heads_bob / 1000
            st.markdown('---')
            st.subheader("📊 Results")
            col3, col4 = st.columns(2)

            with col3:
                st.markdown(f"#### 🎀 Alice's Results")
                st.pyplot(plot_histogram(counts_alice, title=f"Alice (probability={theta_alice:.2f})"))
                st.pyplot(fig_alice)
                st.write(f"`Heads:` **{heads_alice}**  |  `Tails:` **{counts_alice.get('1', 0)}**")

            with col4:
                st.markdown(f"#### 🎩 Bob's Results")
                st.pyplot(plot_histogram(counts_bob, title=f"Bob (probability={theta_bob:.2f})"))
                st.pyplot(fig_bob)
                st.write(f"`Heads:` **{heads_bob}**  |  `Tails:` **{counts_bob.get('1', 0)}**")

            st.divider()
            if win_alice > win_bob:
                st.success(f"🏆 **Alice wins!** ({win_alice * 100:.1f}% Heads vs {win_bob * 100:.1f}%)")
            elif win_bob > win_alice:
                st.success(f"🏆 **Bob wins!** ({win_bob * 100:.1f}% Heads vs {win_alice * 100:.1f}%)")
            else:
                st.info("🤝 It's a tie!")

    # st.divider()


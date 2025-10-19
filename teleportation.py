import streamlit as st
from qiskit import QuantumCircuit
from qiskit_aer import StatevectorSimulator, Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt
from math import pi

def initialize_state():
    st.session_state.theta = 0.0
    st.session_state.phi = 0.0
    st.session_state.lamb = 0.0
    st.session_state.stage = 1
    st.session_state.teleport_circuit = QuantumCircuit(3, 3)
    st.session_state.original_state = None
    st.session_state.final_state = None


def advance_stage():
    st.session_state.stage += 1


def step1_ui():
    qc = st.session_state.teleport_circuit
    st.subheader("Step 1️⃣ — Encode Alice's Hidden message(q₀) using the following parameters")
    st.markdown("""
    In this step, Alice prepares her **secret qubit** |ψ⟩ using rotations. The parameters (θ, φ) define a point on the **Bloch sphere**, representing the qubit’s state
    This qubit is what Alice wants to **send to Bob**, but **without transmitting it physically**.""")
    st.latex(r'''
        |\psi\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + e^{i\varphi}\sin\left(\frac{\theta}{2}\right)|1\rangle
    ''')
    theta = st.slider("`θ` (rotation around Y-axis ranging from 0 to π)", min_value=0.0, max_value=pi, step=0.001, value=0.0)
    phi = st.slider("`φ` (phase around Z-axis ranging from 0 to 2π)", min_value=0.0, max_value=2*pi, step=0.001, value=0.0)
    # lamb = st.slider("`λ` (Added phase lambda ranging from 0 to 2π)", min_value=0.0, max_value=2*pi, step=0.001, value=0.0)
    lamb = 0
    st.session_state.theta = theta
    st.session_state.phi = phi
    st.session_state.lamb = lamb

    qc.data.clear()
    qc.u(theta, phi, lamb, 0)
    qc.barrier()

    show_circuit_and_bloch(qc, Statevector.from_instruction(qc))

    st.button("Next: Entanglement ▶️", on_click=advance_stage)


def step2_ui():
    qc = st.session_state.teleport_circuit
    st.subheader("Step 2️⃣ 👩 — Alice's Qubit is entangled with Bob's")
    st.markdown("""
    Now, Alice and Bob share an **entangled pair** (q₁ and q₂).<br/>
    Alice applies:
    - **Hadamard (H)** on q₁ → creates superposition  
    - **CNOT** between q₁ → q₂ → entangles them  

    The result is a **Bell state**, meaning measuring one instantly defines the other. This shared entanglement acts like a **quantum bridge** between Alice and Bob.
    """, unsafe_allow_html=True)
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()
    st.session_state.original_state = Statevector.from_instruction(qc)
    show_circuit_and_bloch(qc, st.session_state.original_state)
    st.button("Next: Bell Measurement ▶️", on_click=advance_stage)


def step3_ui():
    qc = st.session_state.teleport_circuit
    st.subheader("Step 3️⃣ 👩 — Alice Entangles Her Qubit with the Shared Pair")
    st.markdown("""
    Alice now entangles her **message qubit (q₀)** with her part of the **entangled pair (q₁)** using:
    1. **CNOT**: couples the message to q₁  
    2. **Hadamard**: puts q₀ into superposition
    After this, the 3-qubit system holds all information needed for teleportation.<br/>
    But the message itself is now **distributed** across the system; no single qubit “has” it anymore.
    """, unsafe_allow_html=True)
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()
    st.session_state.state_after_entangle = Statevector.from_instruction(qc)
    show_circuit_and_bloch(qc, st.session_state.state_after_entangle)
    st.button("Next: Alice Measures ▶️", on_click=advance_stage)


def step4_ui():
    st.subheader("Step 4️⃣ 👩 — Alice Measures Her Qubits (q₀ and q₁)")
    st.markdown("""
    Alice measures her two qubits q₀ and q₁.  
    These **classical bits** collapse her part of the system and carry the information Bob needs to **reconstruct** |ψ⟩.
    At this point, Bob’s qubit (q₂) is in a scrambled version of |ψ⟩, depending on Alice’s results.<br/>
    We apply measurement through 1024 shots and send these classical bit measurements to Bob as well. 
    """, unsafe_allow_html=True)

    qc = st.session_state.teleport_circuit
    qc.measure([0, 1], [0, 1])
    qc.barrier()

    backend = Aer.get_backend('aer_simulator')
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts()
    st.pyplot(plot_histogram(counts))
    show_circuit_and_bloch(qc)

    st.button("Next: Bob's Corrections ▶️", on_click=advance_stage)


def step5_ui():
    st.subheader("Step 5️⃣ 👨 — Bob Applies Corrections")
    st.markdown("""
    Bob now uses Alice’s two classical bits to decide which correction gates to apply.<br/>
     If 0th bit is 1, apply X. If 1st bit is 1, apply Z:

    | Measurement Result | Operation on Bob’s qubit |
    |--------------------:|:------------------------|
    | 00 | (do nothing) |
    | 01 | X |
    | 10 | Z |
    | 11 | XZ |

    After applying these, Bob’s qubit **becomes identical** to Alice’s original |ψ⟩, the quantum state has been **teleported!**

    `Notice:` no quantum particle traveled, only two classical bits were sent.
    """, unsafe_allow_html=True)
    qc = st.session_state.teleport_circuit

    with qc.if_test((0, 1)):
        qc.z(2)
    with qc.if_test((1, 1)):
        qc.x(2)
    qc.barrier()

    backend = StatevectorSimulator()
    st.session_state.final_state = backend.run(qc, shots=1).result().get_statevector()  # set shots = 1

    st.markdown("#### Alice's Original State")
    fig1 = plot_bloch_multivector(st.session_state.original_state)
    st.pyplot(fig1)
    plt.close(fig1)

    # with col2:
    st.markdown("#### Bob's Reconstructed State")
    fig2 = plot_bloch_multivector(st.session_state.final_state)
    st.pyplot(fig2)
    plt.close(fig2)
    st.success("✅ Bob’s final qubit (q₂) matches Alice’s original qubit (q₀)!")
    show_circuit_and_bloch(qc)
    st.button("Next: Inverse Measurement ▶️", on_click=advance_stage)


def step6_ui():
    st.subheader("Step 6️⃣ 👨 — Verification using inverse(q₂ should be `|0>`)")
    st.markdown("""
    Finally, we apply the **inverse** of Alice’s original unitary operation on Bob’s qubit.  
    If teleportation worked correctly, Bob’s qubit will return to `|0⟩`, confirming the success.

    This demonstrates the **fidelity of quantum teleportation**, the original state was perfectly transferred using entanglement and classical communication.
    """)
    qc = st.session_state.teleport_circuit

    qc.u(st.session_state.theta, st.session_state.phi, st.session_state.lamb, 2).inverse()
    qc.measure(2, 2)
    qc.barrier()

    backend = StatevectorSimulator()
    final = backend.run(qc, shots=1).result().get_statevector()  # set shots = 1

    backend = Aer.get_backend('aer_simulator')
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts()
    st.pyplot(plot_histogram(counts))
    # fig2 = plot_bloch_multivector(final)
    # st.pyplot(fig2)
    # plt.close(fig2)
    # st.success("✅ Bob’s final qubit (q₂) matches Alice’s original qubit (q₀)!")
    show_circuit_and_bloch(qc, final)
    st.success("Verified!")


def teleportation():
    st.title("📡 Quantum Teleportation Protocol")
    # st.markdown('---')

    if "stage" not in st.session_state:
        initialize_state()

    # st.divider()

    if st.session_state.stage == 1:
        step1_ui()
    elif st.session_state.stage == 2:
        step2_ui()
    elif st.session_state.stage == 3:
        step3_ui()
    elif st.session_state.stage == 4:
        step4_ui()
    elif st.session_state.stage == 5:
        step5_ui()
    elif st.session_state.stage == 6:
        step6_ui()


def show_circuit_and_bloch(qc, statevector=None):
    # st.markdown("---")
    if statevector is not None:
        expander = st.expander("See Bloch Sphere", expanded=True)
        expander.subheader("⚡ Bloch Spheres")
        expander.markdown("**Bloch Sphere Visualization**")
        try:
            fig2 = plot_bloch_multivector(statevector)
            expander.pyplot(fig2)
            plt.close(fig2)
        except Exception as e:
            expander.warning(f"Could not show Bloch sphere: {e}")
    expander1 = st.expander("See Circuit")
    expander1.subheader("⚡ Quantum Circuit Diagram")
    fig = qc.draw(output='mpl', style={'fontsize': 10, 'linecolor': '#555'}, scale=0.5)
    expander1.pyplot(fig, width='content')
    plt.close(fig)

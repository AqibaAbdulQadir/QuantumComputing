from time import sleep
import streamlit as st
from matplotlib import pyplot as plt
from qiskit_aer import Aer
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector


def reset_circuit(n=2):
    st.session_state.alice_ops = []
    st.session_state.init = 0

    qc = QuantumCircuit(n, n)
    qc.name = "Quantum State"

    qc.h(0)
    qc.cx(0, 1)
    if n == 3:
        qc.cx(1, 2)

    qc.barrier()

    st.session_state.qubits = qc
    st.session_state.statevector = Statevector.from_instruction(qc)


def run_qasm_simulation(n=2):
    st.session_state.init = 1
    qc_final = st.session_state.qubits
    qc_final.barrier()

    qc_final.measure(0, 0)
    qc_final.measure(1, 1)
    if n == 3: qc_final.measure(2, 2)
    st.session_state.qubits = qc_final

    simulator = Aer.get_backend('qasm_simulator')
    shots = 1024
    result = simulator.run(qc_final, shots=shots).result()
    counts = result.get_counts()
    q = 'q₂q₁q₀' if n == 3 else 'q₁q₀'
    fig_hist = plot_histogram(counts, title=f"Measurement Result ({q})")

    placeholder = st.empty()
    msg = f"Waiting for Bob{' and Charlie' if n == 3 else ''} to measure..."
    placeholder.info(msg)
    sleep(2)
    placeholder.empty()

    st.subheader(f"{'👨'if n == 2 else '👨👨🏻'} Bob{' & Charlie' if n == 3 else ''}'s Measurement Results")
    st.markdown("Also showing Alice's measurement for correlation.")
    st.pyplot(fig_hist)


def plot_bloch(n):
    if not st.session_state.get("init", False):
        if st.session_state.statevector is not None:
            try:
                st.subheader("🌀 Entangled Qubits Bloch Sphere State")
                st.write("Local States of entangled qubits can never be determined until measured.")
                fig_bloch = plot_bloch_multivector(st.session_state.statevector)
                st.pyplot(fig_bloch)
                plt.close(fig_bloch)
            except Exception as e:
                st.warning(f"⚠️ Could not plot Bloch sphere: {e}")

def entangle(n):
    if 'alice_ops' not in st.session_state:
        st.session_state.alice_ops = []
    if 'statevector' not in st.session_state:
        st.session_state.statevector = None
    if 'qubits' not in st.session_state:
        st.session_state.qubits = None
    if 'init' not in st.session_state:
        st.session_state.init = 0

    st.markdown("# 👩 Alice’s Quantum Controls (q₀)")
    desc = "Bob measures his qubit" if n == 2 else "Bob and Charlie measure their qubits"
    st.markdown(f"Hey Alice! Choose your quantum operations before {desc}.")
    qc = st.session_state.qubits
    col_h, col_x, col_z = st.columns(3)
    if col_h.button("H (Hadamard)", type="primary", use_container_width=True):
        qc.h(0)
        st.session_state.alice_ops.append("H")
        if st.session_state.get("init", False): reset_circuit(n)
    if col_x.button("X (Pauli-X)", type="primary", use_container_width=True):
        qc.x(0)
        st.session_state.alice_ops.append("X")
        if st.session_state.get("init", False): reset_circuit(n)
    if col_z.button("Z (Pauli-Z)", type="primary", use_container_width=True):
        qc.z(0)
        st.session_state.alice_ops.append("Z")
        if st.session_state.get("init", False): reset_circuit(n)

    st.code(f"Sequence: |Φ+> {' → '.join(st.session_state.alice_ops) if st.session_state.alice_ops else ''}")
    # st.markdown("---")
    expander = st.expander("See Circuit")
    if st.session_state.qubits is not None:
        try:
            fig = st.session_state.qubits.draw(output='mpl', style={'fontsize': 10, 'linecolor': '#555'}, scale=0.5)
            expander.pyplot(fig, width="content")
            plt.close(fig)
        except Exception as e:
            st.warning(f"⚠️ Could not draw circuit: {e}")
    else:
        reset_circuit(n)

    col_b1, col_b2 = st.columns(2)
    if col_b2.button("Reset Circuit", on_click=reset_circuit, args=[n], icon="🔄", use_container_width=True):
        st.success(f"Circuit reset to {'Bell' if n == 2 else 'GHZ'} State.")

    if col_b1.button("Run Simulation ▶️", use_container_width=True):
        run_qasm_simulation(n)

    plot_bloch(n)
    # st.markdown("---")

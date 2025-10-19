import streamlit as st
from matplotlib import pyplot as plt
from qiskit.quantum_info import Statevector
from qiskit_aer import Aer
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram, plot_bloch_multivector


def correlation():

    st.title("🔗 Quantum Correlation Explorer")
    st.divider()

    basis = st.selectbox("Choose Measurement Basis:", ["Z", "X", "Y"])
    bell_state = st.selectbox("Choose Bell State:", ["Φ⁺", "Φ⁻", "Ψ⁺", "Ψ⁻"])

    qc = QuantumCircuit(2, 2)

    # Prepare Bell state
    qc.h(0)
    qc.cx(0, 1)
    if bell_state == "Φ⁻":
        qc.z(1)
    elif bell_state == "Ψ⁺":
        qc.x(0)
    elif bell_state == "Ψ⁻":
        qc.x(0)
        qc.z(1)
    qc.barrier()

    state = Statevector.from_instruction(qc)
    bas = ["|00⟩", "|01⟩", "|10⟩", "|11⟩"]
    expander0 = st.expander("Statevector Amplitudes")
    for i, amp in enumerate(state.data):
        if abs(amp) > 1e-6:
            sign = "+" if amp.imag >= 0 else "-"
            expander0.markdown(f"`{bas[i]}`: {amp.real:.2f} {sign} {abs(amp.imag):.2f}i")

    if basis == "X":
        qc.h([0, 1])
    elif basis == "Y":
        qc.h([0, 1])
        qc.s([0, 1])

    qc.barrier()
    qc.measure([0, 1], [0, 1])

    expander1 = st.expander("See Circuit")
    fig = qc.draw(output='mpl', style={'fontsize': 10, 'linecolor': '#555'}, scale=0.5)
    expander1.pyplot(fig, width="content")
    plt.close(fig)

    backend = Aer.get_backend("aer_simulator")
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts()

    expander2 = st.expander("See Histogram")
    expander2.pyplot(plot_histogram(counts), width="content")
    total_shots = sum(counts.values())

    qc1 = QuantumCircuit(2, 2)
    qc1.x(1)
    if 'Z' in basis:
        state = Statevector.from_instruction(qc1)
    elif 'X' in basis:
        qc1.h([0, 1])
        state = Statevector.from_instruction(qc1)
    elif 'Y' in basis:
        qc1.h([0, 1])
        qc1.s([0, 1])
        state = Statevector.from_instruction(qc1)

    expander3 = st.expander("See Bloch Spheres for chosen basis")
    fig_bloch = plot_bloch_multivector(state, title=f"Basis vectors for {basis} basis")
    expander3.pyplot(fig_bloch)
    plt.close(fig_bloch)

    corr = (counts.get("00", 0) + counts.get("11", 0)
            - counts.get("01", 0) - counts.get("10", 0)) / total_shots

    st.markdown(f"`Correlation Coefficient:` {corr:.2f}")


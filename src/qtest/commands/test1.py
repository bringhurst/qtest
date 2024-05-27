import click
import numpy as np
from qiskit import QuantumCircuit  # type: ignore
from qiskit.primitives.sampler import Sampler  # type: ignore
from qiskit.primitives.sampler import PrimitiveJob, SamplerResult


@click.group()
def test1() -> None:
    pass


@test1.command()
def run() -> None:
    # A quantum circuit for preparing the quantum state |000> + i |111>
    qc_example: QuantumCircuit = QuantumCircuit(3)

    # Generate superposition
    qc_example.h(qubit=0)

    # Add quantum phase
    qc_example.p(theta=np.pi / 2, qubit=0)

    # 0th-qubit-Controlled-NOT gate on 1st qubit
    qc_example.cx(control_qubit=0, target_qubit=1)

    # 0th-qubit-Controlled-NOT gate on 2nd qubit
    qc_example.cx(control_qubit=0, target_qubit=2)

    # Add the classical output in the form of measurement of all qubits
    qc_measured: QuantumCircuit | None = qc_example.measure_all(inplace=False)

    if not qc_measured:
        click.echo(message="Failed to measure the circuit!")
    else:

        # Execute using the Sampler primitive
        sampler: Sampler = Sampler()

        job: PrimitiveJob[SamplerResult] = sampler.run(circuits=qc_measured, shots=1000)

        result: SamplerResult = job.result()

        click.echo(message=f"Quasi probability distribution: {result.quasi_dists}")

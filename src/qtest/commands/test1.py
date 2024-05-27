import click
import numpy as np
from qiskit import QuantumCircuit  # type: ignore
from qiskit.primitives import Estimator, EstimatorResult  # type: ignore
from qiskit.primitives.sampler import Sampler  # type: ignore
from qiskit.primitives.sampler import PrimitiveJob, SamplerResult
from qiskit.quantum_info import SparsePauliOp  # type: ignore


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

        sampled_job: PrimitiveJob[SamplerResult] = sampler.run(
            circuits=qc_measured, shots=1000
        )

        sampled_result: SamplerResult = sampled_job.result()

        click.echo(
            message=f"Quasi probability distribution: {sampled_result.quasi_dists}"
        )

    # Define the observable to be measured
    operator: SparsePauliOp = SparsePauliOp.from_list(
        obj=[("XXY", 1), ("XYX", 1), ("YXX", 1), ("YYY", -1)]
    )

    # Execute using the Estimator primitive
    estimator: Estimator = Estimator()

    estimated_job: PrimitiveJob[EstimatorResult] = estimator.run(
        circuits=qc_example, observables=operator, shots=1000
    )

    estimated_result: SamplerResult = estimated_job.result()

    click.echo(message=f"Expectation values: {estimated_result.values}")

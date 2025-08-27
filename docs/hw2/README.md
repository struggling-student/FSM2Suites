# UML Activity Diagrams: Sequential vs Parallel Execution

This document describes two different UML activity diagrams that model the same business process using different execution patterns. Both diagrams represent a system that processes withdrawal (Wth) and deposit (Dep) operations, but they differ fundamentally in how these operations are executed.

## FSM-flat: Sequential Execution Model

The FSM-flat diagram implements a sequential execution pattern where operations are performed one after another in a predefined order. The process flow follows these stages:

The system begins in an Activated state and immediately proceeds to prepare for withdrawal processing. During the PreparingWth phase, the system sets up the necessary conditions for executing a withdrawal test. The withTest operation is then performed to validate the withdrawal functionality.

Upon completion of the withdrawal test, the system evaluates the results through a decision point. If the withdrawal test succeeds, the process moves to the Wth Success state and continues to the next phase. However, if the test fails, the system transitions to a Wth Failed state and immediately proceeds to rollback operations before terminating the entire process.

Assuming the withdrawal test passes, the system then moves to the deposit processing phase. It enters the PreparingDep state to prepare for deposit operations, followed by executing the depTest operation. Similar to the withdrawal phase, the system evaluates the deposit test results at a decision point.

If the deposit test succeeds, the process reaches the Dep Success state and proceeds to the final Committed state, indicating successful completion of both operations. If the deposit test fails, the system enters the Dep Failed state and performs rollback operations before terminating.

## FSM-fork-join: Parallel Execution Model

The FSM-fork-join diagram implements a parallel execution pattern where operations can be performed concurrently, potentially improving system efficiency and reducing overall processing time.

The process begins identically with an Activated state, but immediately after activation, the workflow splits into two parallel branches using a fork construct. This allows both withdrawal and deposit operations to be prepared and tested simultaneously.

The first parallel branch handles withdrawal processing. It follows the same logical sequence as the sequential model: PreparingWth, withTest execution, and result evaluation. Success leads to Wth Success, while failure results in Wth Failed state and rollback termination.

The second parallel branch independently handles deposit processing. It mirrors the withdrawal branch with PreparingDep, depTest execution, and result evaluation, leading to either Dep Success or Dep Failed states with appropriate rollback handling.

The critical difference lies in the synchronization point after both parallel branches. The join construct ensures that both withdrawal and deposit operations must complete successfully before the process can advance to the Committed state. If either branch fails and triggers a rollback, the entire process terminates without reaching the final state.

## Key Differences and Implications

The fundamental distinction between these two models lies in their approach to concurrency and execution efficiency. The sequential model processes operations in a strict order, ensuring that withdrawal operations complete entirely before deposit operations begin. This approach provides predictable timing and simpler error handling but may result in longer overall execution times.

The parallel model allows simultaneous execution of both operation types, potentially reducing total processing time when operations are independent and can benefit from concurrent execution. However, this approach introduces complexity in synchronization and requires careful coordination to ensure both branches complete successfully.

From a system design perspective, the sequential model offers easier debugging and more straightforward error tracing since the execution path is linear. The parallel model provides better resource utilization and performance benefits but requires more sophisticated error handling and state management mechanisms.

The choice between these patterns depends on specific system requirements, including performance constraints, resource availability, error handling complexity, and the independence of the operations being performed. Sequential execution is preferred when operations have dependencies or when system simplicity is prioritized, while parallel execution is beneficial when operations are independent and performance optimization is critical.

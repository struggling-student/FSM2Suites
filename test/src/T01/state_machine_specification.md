# Trip State Machine - Formal Specification

## State Machine Definition

**Name:** TripLifecycle  
**Initial State:** Draft  
**Final States:** {Canceled, Deleted}

## States

| State | Description | Properties |
|-------|-------------|------------|
| **Draft** | Initial editable state | `editable = true` |
| **Published** | Read-only operational state | `editable = false` |
| **Canceled** | Terminal state (normal completion) | `editable = false` |
| **Deleted** | Terminal state (early termination) | N/A |

## State Activities

### Draft State
- **entry:** setup trip
- **do:** allow editing
- **exit:** finalize trip data

### Published State  
- **entry:** make read-only
- **do:** accept participants
- **exit:** close participation

### Canceled State
- **entry:** close trip
- **do:** no operations allowed

### Deleted State
- **entry:** remove trip
- **do:** cleanup resources

## Transitions

### External Transitions (State Changes)
| From | To | Trigger | Guard | Action |
|------|----|------------|-------|--------|
| [*] | Draft | create() | - | setup trip |
| Draft | Published | publish() | valid state | make read-only |
| Draft | Deleted | delete() | valid state | remove trip |
| Published | Canceled | cancel() | valid state | close trip |
| Canceled | [*] | - | - | - |
| Deleted | [*] | - | - | - |

### Internal Transitions (No State Change)
| State | Trigger | Action |
|-------|---------|--------|
| Draft | addActivity() | add to trip |
| Published | joinTrip() | add participant |
| Published | submitFeedback() | record rating |

## Invariants

1. **Draft:** `editable = true` ∧ `participants.empty()`
2. **Published:** `editable = false` ∧ `activities.frozen()`
3. **Canceled:** `editable = false` ∧ `no_operations_allowed()`
4. **Deleted:** `trip.exists() = false`

## Error Handling

Invalid operations (negative test cases) should:
- Not change the current state
- Return appropriate error codes
- Log the invalid operation attempt

### Invalid Operations by State

**Draft:**
- `publish()` when preconditions not met
- `cancel()` (only published trips can be canceled)

**Published:**
- `publish()` (already published)
- `delete()` (cannot delete published trips)
- `addActivity()` (trip is read-only)

**Canceled:**
- All operations except queries (terminal state)

**Deleted:**
- All operations except verification (terminal state)

## Test Coverage

The RoboMachine model covers:
- ✓ All valid state transitions
- ✓ All internal transitions  
- ✓ All invalid operations (negative testing)
- ✓ State invariant verification
- ✓ Entry/exit actions

## Formal Notation

```
TripStateMachine := (S, Σ, δ, s₀, F)

where:
S = {Draft, Published, Canceled, Deleted}        // States
Σ = {create, publish, delete, cancel, addActivity, joinTrip, submitFeedback}  // Alphabet
s₀ = Draft                                       // Initial state  
F = {Canceled, Deleted}                          // Final states

δ: S × Σ → S                                     // Transition function
δ(Draft, publish) = Published
δ(Draft, delete) = Deleted  
δ(Published, cancel) = Canceled
δ(Draft, addActivity) = Draft
δ(Published, joinTrip) = Published
δ(Published, submitFeedback) = Published
```

This formal specification ensures the state machine behavior is well-defined, testable, and follows standard software engineering practices.

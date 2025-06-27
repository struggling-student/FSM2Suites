---
title: Trip Lifecycle State Machine
---
stateDiagram-v2
    classDef activeState fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef finalState fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    [*] --> Draft : create()
    
    Draft : entry / setup trip
    Draft : do / allow editing  
    Draft : editable = true
    
    Published : entry / make read-only
    Published : do / accept participants
    Published : editable = false
    
    Canceled : entry / close trip
    Canceled : do / no operations allowed
    Canceled : editable = false
    
    Deleted : entry / remove trip
    Deleted : do / cleanup resources
    
    %% Primary state transitions
    Draft --> Published : publish() [valid]
    Draft --> Deleted : delete() [valid]
    Published --> Canceled : cancel() [valid]
    
    %% Internal transitions (operations within state)
    Draft --> Draft : addActivity() / add to trip
    Published --> Published : joinTrip() / add participant  
    Published --> Published : submitFeedback() / record rating
    
    %% Terminal transitions
    Canceled --> [*]
    Deleted --> [*]
    
    %% Apply styling
    class Draft activeState
    class Published activeState
    class Canceled finalState
    class Deleted finalState
